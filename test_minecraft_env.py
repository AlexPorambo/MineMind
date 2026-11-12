
from minecraft_env import MinecraftEnv

env = MinecraftEnv()

try:
    observation, info = env.reset()

    print("Starting observation:", observation)
    print("Target:", observation[2:4])

    for i in range(10):
        action = env.action_space.sample()

        observation, reward, terminated, truncated, info = (
            env.step(action)
        )

        print(
            f"Step {i + 1}: "
            f"Action={env.actions[action]}, "
            f"Distance={info['distance']:.2f}, "
            f"Reward={reward:.3f}"
        )

        if terminated or truncated:
            print("Episode finished!")
            break

finally:
    env.close()
