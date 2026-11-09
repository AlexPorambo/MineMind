from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor

from environment import MineMindEnv

# Create the environment
env = MineMindEnv()

model = PPO("MlpPolicy", 
            env=env, 
            learning_rate=0.0003,
            n_steps=256,
            batch_size=64,
            verbose=1,
            tensorboard_log="./runs/")

#train the neural network
model.learn(total_timesteps=100000)

# Save the trained model
model.save("minemind_model")

env.close()

print("training model complete")