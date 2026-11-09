from stable_baselines3 import PPO
from environment import MineMindEnv

# Load the trained model
model = PPO.load("minemind_model")

env = MineMindEnv()

successes = 0
total_steps = 0
episodes = 100

for episode in range(episodes):
    observation, info = env.reset()
    
    done = False
    steps = 0

    while not done:
        action, _ = model.predict(observation, deterministic=True)
        observation, reward, terminated, truncated, info = env.step(action)
        steps += 1

        done = terminated or truncated

    if terminated:
        successes += 1

    total_steps += steps

print(f"Success rate: {successes / episodes * 100:.1f}%")
print(f"Average steps: {total_steps / episodes:.1f}")

env.close()