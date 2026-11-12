import os

from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from minecraft_env import MinecraftEnv

def main():
    os.makedirs('models', exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    #Connect Gym environment to Minecraft
    env = Monitor(MinecraftEnv(), filename="logs/minecraft_env.log")

    #Create a new PPO model 
    model = PPO(
        "MlpPolicy",
        env,
        learning_rate=0.0003,
        n_steps=256,
        batch_size=64,
        gamma=0.99,
        verbose=1,
        tensorboard_log=None
    )

    print("Starting Minecraft PPO training...")

    try:
        model.learn(
            total_timesteps=2000,
            progress_bar=True
        )

        model.save("models/minemind_minecraft_ppo")

        print("Training complete!")
        print("Model saved successfully!")

    finally:
        env.close()

if __name__ == "__main__":
    main()
