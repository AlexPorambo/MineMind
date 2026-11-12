
from stable_baselines3 import PPO

from minecraft_env import MinecraftEnv


env = MinecraftEnv()

try:
    model = PPO.load(
        "models/minemind_minecraft_ppo",
        env=env
    )

    successes = 0
    total_steps = 0
    episodes = 10

    for episode in range(episodes):
        observation, info = env.reset()
        terminated = False
        truncated = False
        steps = 0

        while not (terminated or truncated):
            action, _ = model.predict(
                observation,
                deterministic=True
            )

            observation, reward, terminated, truncated, info = (
                env.step(action)
            )

            steps += 1

        if terminated:
            successes += 1

        total_steps += steps

        print(
            f"Episode {episode + 1}: "
            f"Success={terminated}, "
            f"Steps={steps}, "
            f"Final distance={info['distance']:.2f}"
        )

    print("\nEvaluation Results")
    print(f"Success rate: {successes / episodes * 100:.1f}%")
    print(f"Average steps: {total_steps / episodes:.1f}")

finally:
    env.close()
