import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from stable_baselines3 import PPO

from environment import MineMindEnv

# Load our trained neural network
model = PPO.load("minemind_model")

# Create the environment
env = MineMindEnv()
observation, info = env.reset()

# Create the visualization
fig, ax = plt.subplots(figsize=(6, 6))


def update(frame):
    global observation

    ax.clear()

    # Ask the neural network to choose an action
    action, _ = model.predict(
        observation,
        deterministic=True
    )

    # Perform the action
    observation, reward, terminated, truncated, info = (
        env.step(int(action))
    )

    # Draw the environment
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(4.5, -0.5)

    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    ax.grid(True)

    # Draw the agent
    ax.scatter(
        env.agent_pos[0],
        env.agent_pos[1],
        color="blue",
        s=400,
        label="AI Agent"
    )

    # Draw the target
    ax.scatter(
        env.target_pos[0],
        env.target_pos[1],
        color="green",
        s=400,
        marker="*",
        label="Target"
    )

    ax.set_title(f"MineMind | Step {env.steps}")
    ax.legend(loc="upper right")

    # Start another episode when finished
    if terminated or truncated:
        observation, info = env.reset()


animation = FuncAnimation(
    fig,
    update,
    interval=500,
    cache_frame_data=False
)

plt.show()

env.close()