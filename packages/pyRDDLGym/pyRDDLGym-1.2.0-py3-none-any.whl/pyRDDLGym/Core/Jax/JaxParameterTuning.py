from bayes_opt import BayesianOptimization
from bayes_opt.util import UtilityFunction
from colorama import init as colorama_init, Back, Fore, Style
colorama_init()    
import csv
import datetime
import jax
from multiprocessing import get_context
import numpy as np
import os
import time
from typing import Callable, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

from pyRDDLGym.Core.Env.RDDLEnv import RDDLEnv
from pyRDDLGym.Core.Jax.JaxRDDLBackpropPlanner import JaxRDDLBackpropPlanner
from pyRDDLGym.Core.Jax.JaxRDDLBackpropPlanner import JaxStraightLinePlan
from pyRDDLGym.Core.Jax.JaxRDDLBackpropPlanner import JaxDeepReactivePolicy

# do this after imports to prevent it from being overwritten
np.seterr(all='warn')

# ===============================================================================
# 
# GENERIC TUNING MODULE
# 
# Currently contains three implementations:
# 1. straight line plan
# 2. replanning
# 3. deep reactive policies
# 
# ===============================================================================


class JaxParameterTuning:
    '''A general-purpose class for tuning a Jax planner.'''
    
    def __init__(self, env: RDDLEnv,
                 hyperparams_dict: Dict[str, Tuple[float, float, Callable]],
                 max_train_epochs: int,
                 timeout_episode: float,
                 timeout_tuning: float=np.inf,
                 verbose: bool=True,
                 print_step: int=None,
                 planner_kwargs: Dict={},
                 plan_kwargs: Dict={},
                 pool_context: str='spawn',
                 num_workers: int=1, 
                 poll_frequency: float=0.2,
                 gp_iters: int=25,
                 acquisition=None,
                 gp_init_kwargs: Dict={},
                 gp_params: Dict={'n_restarts_optimizer': 10}) -> None:
        '''Creates a new instance for tuning hyper-parameters for Jax planners
        on the given RDDL domain and instance.
        
        :param env: the RDDLEnv describing the MDP to optimize
        :param hyperparams_dict: dictionary mapping name of each hyperparameter
        to a triple, where the first two elements are lower/upper bounds on the
        parameter value, and the last is a callable mapping the parameter to its
        RDDL equivalent
        :param max_train_epochs: the maximum number of iterations of SGD per 
        step or trial
        :param timeout_episode: the maximum amount of time to spend training per
        trial (in seconds)
        :param timeout_tuning: the maximum amount of time to spend tuning 
        hyperparameters in general (in seconds)
        :param verbose: whether to print intermediate results of tuning
        :param print_step: how often to print training callback
        :param planner_kwargs: additional arguments to feed to the planner
        :param plan_kwargs: additional arguments to feed to the plan/policy
        :param pool_context: context for multiprocessing pool (defaults to 
        "spawn")
        :param num_workers: how many points to evaluate in parallel
        :param poll_frequency: how often (in seconds) to poll for completed
        jobs, necessary if num_workers > 1
        :param gp_iters: number of iterations of optimization
        :param acquisition: acquisition function for Bayesian optimizer
        :parm gp_init_kwargs: additional parameters to feed to Bayesian 
        during initialization  
        :param gp_params: additional parameters to feed to Bayesian optimizer 
        after initialization optimization
        '''
        
        self.env = env
        self.hyperparams_dict = hyperparams_dict
        self.max_train_epochs = max_train_epochs
        self.timeout_episode = timeout_episode
        self.timeout_tuning = timeout_tuning
        self.verbose = verbose
        self.print_step = print_step
        self.planner_kwargs = planner_kwargs
        self.plan_kwargs = plan_kwargs
        self.pool_context = pool_context
        self.num_workers = num_workers
        self.poll_frequency = poll_frequency
        self.gp_iters = gp_iters
        self.gp_init_kwargs = gp_init_kwargs
        self.gp_params = gp_params
        
        # create acquisition function
        if acquisition is None:
            num_samples = self.gp_iters * self.num_workers
            acquisition = JaxParameterTuning._annealing_utility(num_samples)
        self.acquisition = acquisition
        
        # create valid color variations for multiprocess output
        self.colors = JaxParameterTuning._color_variations()
        self.num_workers = min(num_workers, len(self.colors))

    @staticmethod
    def _color_variations():
        foreground = [Fore.BLUE, Fore.CYAN, Fore.GREEN,
                      Fore.MAGENTA, Fore.RED, Fore.YELLOW]
        background = [Back.RESET, Back.BLUE, Back.CYAN, Back.GREEN,
                      Back.MAGENTA, Back.RED, Back.YELLOW]
        return [(fore, back) 
                for back in background
                for fore in foreground
                if int(back[2:-1]) - int(fore[2:-1]) != 10]  # ensure fore != back

    @staticmethod
    def _annealing_utility(n_samples, n_delay_samples=0, kappa1=10.0, kappa2=1.0):
        return UtilityFunction(
            kind='ucb',
            kappa=kappa1,
            kappa_decay=(kappa2 / kappa1) ** (1.0 / (n_samples - n_delay_samples)),
            kappa_decay_delay=n_delay_samples)
    
    def _pickleable_objective_with_kwargs(self):
        raise NotImplementedError
    
    @staticmethod
    def _wrapped_evaluate(index, params, key, color, func, kwargs):
        target = func(params=params, kwargs=kwargs, key=key, index=index, color=color)
        pid = os.getpid()
        return index, pid, params, target

    def tune(self, key: jax.random.PRNGKey, filename: str) -> Dict[str, object]:
        '''Tunes the hyper-parameters for Jax planner, returns the best found.'''
        starttime = time.time()
        
        # objective function
        objective = self._pickleable_objective_with_kwargs()
        evaluate = JaxParameterTuning._wrapped_evaluate
            
        # create optimizer
        hyperparams_bounds = {
            name: hparam[:2] 
            for (name, hparam) in self.hyperparams_dict.items()
        }
        optimizer = BayesianOptimization(
            f=None,  # probe() is not called
            pbounds=hyperparams_bounds,
            allow_duplicate_points=True,  # to avoid crash
            random_state=np.random.RandomState(key),
            **self.gp_init_kwargs
        )
        optimizer.set_gp_params(**self.gp_params)
        utility = self.acquisition
        
        # suggest initial parameters to evaluate
        num_workers = self.num_workers
        suggested, kappas = [], []
        for _ in range(num_workers):
            utility.update_params()
            probe = optimizer.suggest(utility)
            suggested.append(probe)  
            kappas.append(utility.kappa)
        
        # clear and prepare output file
        filename = self._filename(filename, 'csv')
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                ['pid', 'worker', 'iteration', 'target', 'best_target', 'kappa'] + \
                 list(hyperparams_bounds.keys())
            )
                
        # start multiprocess evaluation
        colors = self.colors[:num_workers]
        worker_ids = list(range(num_workers))
        best_params, best_target = None, -np.inf
        
        for it in range(self.gp_iters): 
            
            # check if there is enough time left for another iteration
            currtime = time.time()  
            elapsed = currtime - starttime
            if elapsed > self.timeout_tuning - self.timeout_episode:
                print(f'global time limit reached at iteration {it}, aborting')
                break
            
            # continue with next iteration
            print('\n' + '*' * 25 + 
                  '\n' + f'[{datetime.timedelta(seconds=elapsed)}] ' + 
                  f'starting iteration {it}' + 
                  '\n' + '*' * 25)
            key, *subkeys = jax.random.split(key, num=num_workers + 1)
            rows = [None] * num_workers
            
            # create worker pool: note each iteration must wait for all workers
            # to finish before moving to the next
            with get_context(self.pool_context).Pool(processes=num_workers) as pool:
                
                # assign jobs to worker pool
                # - each trains on suggested parameters from the last iteration
                # - this way, since each job finishes asynchronously, these
                # parameters usually differ across jobs
                results = [
                    pool.apply_async(evaluate, worker_args + objective)
                    for worker_args in zip(worker_ids, suggested, subkeys, colors)
                ]
            
                # wait for all workers to complete
                while results:
                    time.sleep(self.poll_frequency)
                    
                    # determine which jobs have completed
                    jobs_done = []
                    for (i, candidate) in enumerate(results):
                        if candidate.ready():
                            jobs_done.append(i)
                    
                    # get result from completed jobs
                    for i in jobs_done[::-1]:
                        
                        # extract and register the new evaluation
                        index, pid, params, target = results.pop(i).get()
                        optimizer.register(params, target)
                        
                        # update acquisition function and suggest a new point
                        utility.update_params()  
                        suggested[index] = optimizer.suggest(utility)
                        old_kappa = kappas[index]
                        kappas[index] = utility.kappa
                        
                        # transform suggestion back to natural space
                        rddl_params = {
                            name: pf(params[name])
                            for (name, (*_, pf)) in self.hyperparams_dict.items()
                        }
                        
                        # update the best suggestion so far
                        if target > best_target:
                            best_params, best_target = rddl_params, target
                        
                        # write progress to file in real time
                        rows[index] = [
                            pid, index, it, target, best_target, old_kappa
                        ] + list(rddl_params.values())
                        
            # write results of all processes in current iteration to file
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            
        self._save_plot(filename)
        return best_params

    def _filename(self, name, ext):
        domainName = self.env.model.domainName()
        instName = self.env.model.instanceName()
        domainName = ''.join(c for c in domainName if c.isalnum() or c == '_')
        instName = ''.join(c for c in instName if c.isalnum() or c == '_')
        filename = f'{name}_{domainName}_{instName}.{ext}'
        return filename
    
    def _save_plot(self, filename):
        try:
            import matplotlib.pyplot as plt
            from sklearn.manifold import MDS
        except Exception as e:
            warnings.warn(f'failed to import packages matplotlib or sklearn, '
                          f'aborting plot of search space\n'
                          f'{e}', stacklevel=2)
        else:
            data = np.loadtxt(filename, delimiter=',', dtype=object)
            data, target = data[1:, 3:], data[1:, 2]
            data = data.astype(np.float64)
            target = target.astype(np.float64)
            target = (target - np.min(target)) / (np.max(target) - np.min(target))
            embedding = MDS(n_components=2, normalized_stress='auto')
            data1 = embedding.fit_transform(data)
            sc = plt.scatter(data1[:, 0], data1[:, 1], c=target, s=4.,
                             cmap='seismic', edgecolor='gray',
                             linewidth=0.01, alpha=0.4)
            plt.colorbar(sc)
            plt.savefig(self._filename('gp_points', 'pdf'))
            plt.clf()
            plt.close()

# ===============================================================================
# 
# STRAIGHT LINE PLANNING
#
# ===============================================================================


def train_epoch(key, model_params, policy_hyperparams, subs, planner, timeout,
                 max_train_epochs, verbose, print_step, index, color, guess=None): 
    colorstr = f'{color[0]}{color[1]}'
    starttime = None
    for (it, callback) in enumerate(planner.optimize(
        key=key,
        epochs=max_train_epochs,
        step=1,
        model_params=model_params,
        policy_hyperparams=policy_hyperparams,
        subs=subs,
        guess=guess
    )):
        if starttime is None:
            starttime = time.time()
        currtime = time.time()  
        elapsed = currtime - starttime    
        if verbose and print_step is not None and print_step > 0 \
        and it > 0 and it % print_step == 0:
            print(f'|------ [{index}] {colorstr}' 
                  '[{:.4f} s] step={} train_return={:.6f} test_return={:.6f} best_return={:.6f}'.format(
                      index,
                      elapsed,
                      str(callback['iteration']).rjust(4),
                      callback['train_return'],
                      callback['test_return'],
                      callback['best_return']) + 
                  f'{Style.RESET_ALL}')
        if not np.isfinite(callback['train_return']):
            if verbose:
                print(f'|------ [{index}] {colorstr}'
                      f'warning: training aborted due to NaN or inf value'
                      f'{Style.RESET_ALL}')
            break
        if elapsed >= timeout:
            break
    return callback


def objective_slp(params, kwargs, key, index, color=(Fore.RESET, Back.RESET)):
                    
    # transform hyper-parameters to natural space
    param_values = [
        pmap(params[name])
        for (name, (*_, pmap)) in kwargs['hyperparams_dict'].items()
    ]
    
    # unpack hyper-parameters
    if kwargs['wrapped_bool_actions']:
        std, lr, w, wa = param_values
    else:
        std, lr, w = param_values
        wa = None
                      
    if kwargs['verbose']:
        print(f'| [{index}] {color[0]}{color[1]}'
                f'optimizing SLP with PRNG key={key}, ' 
                f'std={std}, lr={lr}, w={w}, wa={wa}...{Style.RESET_ALL}')
        
    # initialize planner
    planner = JaxRDDLBackpropPlanner(
        rddl=kwargs['rddl'],
        plan=JaxStraightLinePlan(
            initializer=jax.nn.initializers.normal(std),
            **kwargs['plan_kwargs']),
        optimizer_kwargs={'learning_rate': lr},
        **kwargs['planner_kwargs'])
                    
    # perform training
    callback = train_epoch(
        key=key,
        model_params={name: w for name in planner.compiled.model_params},
        policy_hyperparams={name: wa for name in kwargs['wrapped_bool_actions']},
        subs=None,
        planner=planner,
        timeout=kwargs['timeout_episode'],
        max_train_epochs=kwargs['max_train_epochs'],
        verbose=kwargs['verbose'],
        print_step=kwargs['print_step'],
        index=index,
        color=color,
        guess=None)
    total_reward = float(callback['best_return'])
            
    if kwargs['verbose']:
        print(f'| [{index}] {color[0]}{color[1]}'
                f'done optimizing SLP, '
                f'total reward={total_reward}{Style.RESET_ALL}')
    return total_reward

        
def power_ten(x):
    return 10.0 ** x

    
class JaxParameterTuningSLP(JaxParameterTuning):
    
    def __init__(self, *args,
                 hyperparams_dict: Dict[str, Tuple[float, float, Callable]]={
                    'std': (-5., 0., power_ten),
                    'lr': (-5., 0., power_ten),
                    'w': (0., 5., power_ten),
                    'wa': (0., 5., power_ten)
                 },
                 **kwargs) -> None:
        '''Creates a new tuning class for straight line planners.
        
        :param *args: arguments to pass to parent class
        :param hyperparams_dict: same as parent class, but here must contain
        weight initialization (std), learning rate (lr), model weight (w), and
        action weight (wa) if wrap_sigmoid and boolean action fluents exist
        :param **kwargs: keyword arguments to pass to parent class
        '''
        
        super(JaxParameterTuningSLP, self).__init__(
            *args, hyperparams_dict=hyperparams_dict, **kwargs)
        
        # action parameters required if wrap_sigmoid and boolean action exists
        self.wrapped_bool_actions = []
        if self.plan_kwargs.get('wrap_sigmoid', True):
            for var in self.env.model.actions:
                if self.env.model.variable_ranges[var] == 'bool':
                    self.wrapped_bool_actions.append(var)
        if not self.wrapped_bool_actions:
            self.hyperparams_dict.pop('wa', None)
        
    def _pickleable_objective_with_kwargs(self):
        objective_fn = objective_slp
        
        # duplicate planner and plan keyword arguments must be removed
        plan_kwargs = self.plan_kwargs.copy()
        plan_kwargs.pop('initializer', None) 
               
        planner_kwargs = self.planner_kwargs.copy()
        planner_kwargs.pop('rddl', None)
        planner_kwargs.pop('plan', None)
        planner_kwargs.pop('optimizer_kwargs', None)
                    
        kwargs = {
            'rddl': self.env.model,
            'hyperparams_dict': self.hyperparams_dict,
            'timeout_episode': self.timeout_episode,
            'max_train_epochs': self.max_train_epochs,
            'planner_kwargs': planner_kwargs,
            'plan_kwargs': plan_kwargs,
            'verbose': self.verbose,
            'print_step': self.print_step,
            'wrapped_bool_actions': self.wrapped_bool_actions
        }
        return objective_fn, kwargs

# ===============================================================================
# 
# REPLANNING
#
# ===============================================================================


def objective_replan(params, kwargs, key, index, color=(Fore.RESET, Back.RESET)):

    # transform hyper-parameters to natural space
    param_values = [
        pmap(params[name])
        for (name, (*_, pmap)) in kwargs['hyperparams_dict'].items()
    ]
    
    # unpack hyper-parameters
    if kwargs['wrapped_bool_actions']:
        std, lr, w, wa, T = param_values
    else:
        std, lr, w, T = param_values
        wa = None
        
    if kwargs['verbose']:
        print(f'| [{index}] {color[0]}{color[1]}'
              f'optimizing MPC with PRNG key={key}, ' 
              f'std={std}, lr={lr}, w={w}, wa={wa}, T={T}...'
              f'{Style.RESET_ALL}')

    # initialize planner
    planner = JaxRDDLBackpropPlanner(
        rddl=kwargs['rddl'],
        plan=JaxStraightLinePlan(
            initializer=jax.nn.initializers.normal(std),
            **kwargs['plan_kwargs']),
        rollout_horizon=T,
        optimizer_kwargs={'learning_rate': lr},
        **kwargs['planner_kwargs'])
    policy_hyperparams = {name: wa for name in kwargs['wrapped_bool_actions']}
    model_params = {name: w for name in planner.compiled.model_params}
    
    # initialize env for evaluation (need fresh copy to avoid concurrency)
    env = RDDLEnv(domain=kwargs['domain'],
                  instance=kwargs['instance'],
                  enforce_action_constraints=True)

    # perform training
    average_reward = 0.0
    for trial in range(kwargs['eval_trials']):
        
        # start the next trial
        if kwargs['verbose']:
            print(f'|--- [{index}] {color[0]}{color[1]}'
                  f'starting trial {trial + 1} '
                  f'with PRNG key={key}...{Style.RESET_ALL}')
            
        total_reward = 0.0
        guess = None
        env.reset() 
        starttime = time.time()
        for _ in range(kwargs['eval_horizon']):
            currtime = time.time()
            elapsed = currtime - starttime            
            if elapsed < kwargs['timeout_episode']:
                subs = env.sampler.subs
                timeout = min(kwargs['timeout_episode'] - elapsed,
                              kwargs['timeout_epoch'])
                key, subkey1, subkey2 = jax.random.split(key, num=3)
                callback = train_epoch(
                    key=subkey1,
                    model_params=model_params,
                    policy_hyperparams=policy_hyperparams,
                    subs=subs,
                    planner=planner,
                    timeout=timeout,
                    max_train_epochs=kwargs['max_train_epochs'],
                    verbose=kwargs['verbose'],
                    print_step=None,
                    index=index,
                    color=color,
                    guess=guess)
                params = callback['best_params']
                action = planner.get_action(subkey2, params, 0, subs)
                if kwargs['use_guess_last_epoch']:
                    guess = planner.plan.guess_next_epoch(params)
            else:
                action = {}            
            _, reward, done, _ = env.step(action)
            total_reward += reward 
            if done: 
                break  
            
        # update average reward across trials
        if kwargs['verbose']:
            print(f'|--- [{index}] {color[0]}{color[1]}'
                  f'done trial {trial + 1}, '
                  f'total reward={total_reward}{Style.RESET_ALL}')
        average_reward += total_reward / kwargs['eval_trials']
        
    if kwargs['verbose']:
        print(f'| [{index}] {color[0]}{color[1]}'
              f'done optimizing MPC, '
              f'average reward={average_reward}{Style.RESET_ALL}')
    return average_reward

    
class JaxParameterTuningSLPReplan(JaxParameterTuningSLP):
    
    def __init__(self, timeout_epoch: float,
                 *args,
                 hyperparams_dict: Dict[str, Tuple[float, float, Callable]]={
                    'std': (-5., 0., power_ten),
                    'lr': (-5., 0., power_ten),
                    'w': (0., 5., power_ten),
                    'wa': (0., 5., power_ten),
                    'T': (1, 100, int)
                 },
                 eval_trials: int=5,
                 use_guess_last_epoch: bool=True,
                 **kwargs) -> None:
        '''Creates a new tuning class for straight line planners.
        
        :param timeout_epoch: the maximum amount of time to spend training per
        decision time step
        :param *args: arguments to pass to parent class
        :param hyperparams_dict: same as parent class, but here must contain
        weight initialization (std), learning rate (lr), model weight (w), 
        action weight (wa) if wrap_sigmoid and boolean action fluents exist, and
        lookahead horizon (T)
        :param eval_trials: how many trials to perform independent training
        in order to estimate the return for each set of hyper-parameters
        :param use_guess_last_epoch: use the trained parameters from previous 
        decision to warm-start next decision
        :param **kwargs: keyword arguments to pass to parent class
        '''
        
        super(JaxParameterTuningSLPReplan, self).__init__(
            *args, hyperparams_dict=hyperparams_dict, **kwargs)
        
        self.timeout_epoch = timeout_epoch
        self.eval_trials = eval_trials
        self.use_guess_last_epoch = use_guess_last_epoch
        
    def _pickleable_objective_with_kwargs(self):
        objective_fn = objective_replan
            
        # duplicate planner and plan keyword arguments must be removed
        plan_kwargs = self.plan_kwargs.copy()
        plan_kwargs.pop('initializer', None)
        
        planner_kwargs = self.planner_kwargs.copy()
        planner_kwargs.pop('rddl', None)
        planner_kwargs.pop('plan', None)
        planner_kwargs.pop('rollout_horizon', None)
        planner_kwargs.pop('optimizer_kwargs', None)
                        
        kwargs = {
            'rddl': self.env.model,
            'domain': self.env.domain_text,
            'instance': self.env.instance_text,
            'hyperparams_dict': self.hyperparams_dict,
            'timeout_episode': self.timeout_episode,
            'max_train_epochs': self.max_train_epochs,
            'planner_kwargs': planner_kwargs,
            'plan_kwargs': plan_kwargs,
            'verbose': self.verbose,
            'print_step': self.print_step,
            'wrapped_bool_actions': self.wrapped_bool_actions,
            'timeout_epoch': self.timeout_epoch,
            'eval_trials': self.eval_trials,
            'eval_horizon': self.env.horizon,
            'use_guess_last_epoch': self.use_guess_last_epoch
        }
        return objective_fn, kwargs

# ===============================================================================
# 
# DEEP REACTIVE POLICIES
#
# ===============================================================================


def objective_drp(params, kwargs, key, index, color=(Fore.RESET, Back.RESET)):
                    
    # transform hyper-parameters to natural space
    param_values = [
        pmap(params[name])
        for (name, (*_, pmap)) in kwargs['hyperparams_dict'].items()
    ]
    
    # unpack hyper-parameters
    lr, w, layers, neurons = param_values
                      
    if kwargs['verbose']:
        print(f'| [{index}] {color[0]}{color[1]}'
                f'optimizing DRP with PRNG key={key}, ' 
                f'lr={lr}, w={w}, layers={layers}, neurons={neurons}...{Style.RESET_ALL}')
           
    # initialize planner
    planner = JaxRDDLBackpropPlanner(
        rddl=kwargs['rddl'],
        plan=JaxDeepReactivePolicy(
            topology=[neurons] * layers,
            **kwargs['plan_kwargs']),
        optimizer_kwargs={'learning_rate': lr},
        **kwargs['planner_kwargs'])
    
    # perform training
    callback = train_epoch(
        key=key,
        model_params={name: w for name in planner.compiled.model_params},
        policy_hyperparams={name: None for name in planner._action_bounds},
        subs=None,
        planner=planner,
        timeout=kwargs['timeout_episode'],
        max_train_epochs=kwargs['max_train_epochs'],
        verbose=kwargs['verbose'],
        print_step=kwargs['print_step'],
        index=index,
        color=color,
        guess=None)
    total_reward = float(callback['best_return'])
            
    if kwargs['verbose']:
        print(f'| [{index}] {color[0]}{color[1]}'
                f'done optimizing DRP, '
                f'total reward={total_reward}{Style.RESET_ALL}')
    return total_reward


def power_two_int(x):
    return 2 ** int(x)


class JaxParameterTuningDRP(JaxParameterTuning):
    
    def __init__(self, *args,
                 hyperparams_dict: Dict[str, Tuple[float, float, Callable]]={
                    'lr': (-6., 0., power_ten),
                    'w': (0., 5., power_ten),
                    'layers': (1., 3., int),
                    'neurons': (1., 9., power_two_int)
                 },
                 **kwargs) -> None:
        '''Creates a new tuning class for deep reactive policies.
        
        :param *args: arguments to pass to parent class
        :param hyperparams_dict: same as parent class, but here must contain
        learning rate (lr), model weight (w), number of hidden layers (layers) 
        and number of neurons per hidden layer (neurons)
        :param **kwargs: keyword arguments to pass to parent class
        '''
        
        super(JaxParameterTuningDRP, self).__init__(
            *args, hyperparams_dict=hyperparams_dict, **kwargs)
    
    def _pickleable_objective_with_kwargs(self):
        objective_fn = objective_drp
        
        # duplicate planner and plan keyword arguments must be removed
        plan_kwargs = self.plan_kwargs.copy()
        plan_kwargs.pop('topology', None)
        
        planner_kwargs = self.planner_kwargs.copy()
        planner_kwargs.pop('rddl', None)
        planner_kwargs.pop('plan', None)
        planner_kwargs.pop('optimizer_kwargs', None)
                     
        kwargs = {
            'rddl': self.env.model,
            'hyperparams_dict': self.hyperparams_dict,
            'timeout_episode': self.timeout_episode,
            'max_train_epochs': self.max_train_epochs,
            'planner_kwargs': planner_kwargs,
            'plan_kwargs': plan_kwargs,
            'verbose': self.verbose,
            'print_step': self.print_step
        }
        return objective_fn, kwargs
