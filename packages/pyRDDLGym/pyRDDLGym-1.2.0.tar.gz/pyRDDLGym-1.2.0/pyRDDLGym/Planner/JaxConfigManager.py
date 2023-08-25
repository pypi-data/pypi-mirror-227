from ast import literal_eval
import configparser
import jax
import jax.nn.initializers as initializers
import optax
import os
from typing import Dict
import warnings

from pyRDDLGym.Core.Env.RDDLEnv import RDDLEnv
from pyRDDLGym.Core.Jax import JaxRDDLBackpropPlanner
from pyRDDLGym.Core.Jax import JaxRDDLLogic
from pyRDDLGym.Examples.ExampleManager import ExampleManager


def load_config_file(path: str):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    if not os.path.isfile(path):
        raise FileNotFoundError(f'File {path} does not exist.')
    config = configparser.RawConfigParser()
    config.optionxform = str 
    config.read(path)
    args = {k: literal_eval(v) 
            for section in config.sections()
            for (k, v) in config.items(section)}
    return config, args


def read_config_sections(config, args):
    env_args = {k: args[k] for (k, _) in config.items('Environment')} 
    model_args = {k: args[k] for (k, _) in config.items('Model')}
    planner_args = {k: args[k] for (k, _) in config.items('Optimizer')}
    train_args = {k: args[k] for (k, _) in config.items('Training')}
    return env_args, model_args, planner_args, train_args


def load_rddl_files(check_external, domain_name, inst_name):
    try: 
        # try to read from external rddlrepository  
        if not check_external:
            raise Exception
        warnings.warn(f'reading {domain_name} from rddlrepository...', stacklevel=2)
        from rddlrepository.Manager.RDDLRepoManager import RDDLRepoManager
        manager = RDDLRepoManager()
        EnvInfo = manager.get_problem(domain_name)
    except: 
        # default to embedded RDDL manager
        warnings.warn(f'failed to read from rddlrepository, '
                      f'reading {domain_name} from Examples...', stacklevel=2)
        EnvInfo = ExampleManager.GetEnvInfo(domain_name)        
    domain = EnvInfo.get_domain()
    instance = EnvInfo.get_instance(inst_name)
    return domain, instance


def get(path: str, inst: str=None) -> Dict[str, object]:
    
    # load the config file
    config, args = load_config_file(path)
    env_args, model_args, planner_args, train_args = read_config_sections(config, args)
    
    # read the environment settings
    if inst is not None:
        env_args['instance'] = inst
    check_external = env_args.pop('check_rddlrepository', False)
    domain_name = env_args['domain']
    inst_name = env_args['instance']
    env_args['domain'], env_args['instance'] = load_rddl_files(
        check_external, domain_name, inst_name)
    myEnv = RDDLEnv(**env_args)
    planner_args['rddl'] = myEnv.model
    
    # read the model settings
    tnorm_name = model_args['tnorm']
    tnorm_kwargs = model_args['tnorm_kwargs']
    logic_name = model_args['logic']
    logic_kwargs = model_args['logic_kwargs']
    logic_kwargs['tnorm'] = getattr(JaxRDDLLogic, tnorm_name)(**tnorm_kwargs)
    planner_args['logic'] = getattr(JaxRDDLLogic, logic_name)(**logic_kwargs)
    
    # read the optimizer settings
    plan_method = planner_args.pop('method')
    plan_kwargs = planner_args.pop('method_kwargs', {})  
    
    if 'initializer' in plan_kwargs:  # weight initialization
        init_name = plan_kwargs['initializer']
        init_class = getattr(initializers, init_name)
        init_kwargs = plan_kwargs.pop('initializer_kwargs', {})
        try: 
            plan_kwargs['initializer'] = init_class(**init_kwargs)
        except:
            warnings.warn(f'ignoring arguments for initializer <{init_name}>',
                          stacklevel=2)
            plan_kwargs['initializer'] = init_class
               
    if 'activation' in plan_kwargs:  # activation function
        plan_kwargs['activation'] = getattr(jax.nn, plan_kwargs['activation'])
    
    planner_args['plan'] = getattr(JaxRDDLBackpropPlanner, plan_method)(**plan_kwargs)
    planner_args['optimizer'] = getattr(optax, planner_args['optimizer'])
    planner = JaxRDDLBackpropPlanner.JaxRDDLBackpropPlanner(**planner_args)
    
    # read the training settings
    train_args['key'] = jax.random.PRNGKey(train_args['key'])
    
    return myEnv, planner, planner_args, plan_kwargs, train_args, \
        (domain_name, inst_name)
    
