import sys
import os

from pyRDDLGym import RDDLEnv
from pyRDDLGym import ExampleManager
from pyRDDLGym.Policies.Agents import RandomAgent
from pyRDDLGym.Visualizer.MovieGenerator import MovieGenerator
from pyRDDLGym.Visualizer.TextViz import TextVisualizer

def main(env, inst, method_name=None, episodes=1):
    print(f'preparing to launch instance {inst} of domain {env}...')
    
    # get the environment info
    # ExampleManager.RebuildExamples()
    EnvInfo = ExampleManager.GetEnvInfo(env)
    
    # set up the environment class, choose instance 0 because every example has at least one example instance
    log = False if method_name is None else True
    myEnv = RDDLEnv.RDDLEnv(domain=EnvInfo.get_domain(), 
                            instance=EnvInfo.get_instance(inst),
                            enforce_action_constraints=False,
                            debug=False,
                            log=log,
                            simlogname=method_name)
    myEnv.seed(42)
    
    # set up the environment visualizer
    # frames_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Visualizer', 'Frames')
    myEnv.set_visualizer(EnvInfo.get_visualizer())#, movie_gen=MovieGenerator(frames_path, env, 200), movie_per_episode=True)
    # myEnv.set_visualizer(None, movie_gen=MovieGenerator(frames_path, env, 200),
    #                      movie_per_episode=True)
    
    # set up an example aget
    agent = RandomAgent(action_space=myEnv.action_space, 
                        num_actions=myEnv.numConcurrentActions,
                        seed=42)

    for episode in range(episodes):
        total_reward = 0
        state = myEnv.reset()
        for step in range(myEnv.horizon):
            myEnv.render()
            action = agent.sample_action()
            next_state, reward, done, info = myEnv.step(action)
            total_reward += reward
            print()
            print(f'step       = {step}')
            print(f'state      = {state}')
            print(f'action     = {action}')
            print(f'next state = {next_state}')
            print(f'reward     = {reward}')
            state = next_state
            if done:
                break
        print(f'episode {episode} ended with reward {total_reward}')
    
    myEnv.close()


if __name__ == "__main__":
    args = sys.argv
    method_name = None
    episodes = 1
    if len(args) < 3:
        env, inst = 'HVAC', '0'
    elif len(args) < 4:
        env, inst = args[1:3]
    elif len(args) < 5:
        env, inst, method_name = args[1:4]
    else:
        env, inst, method_name, episodes = args[1:5]
        try:
            episodes = int(episodes)
        except:
            raise ValueError('episodes argument must be an integer, received:' + episodes)
    main(env, inst, method_name, episodes)
