import gymnasium as gym
from gymnasium import spaces
import numpy as np

class MineMindEnv(gym.Env):
    def __init__(self):
        super().__init__()

        self.grid_size = 5 ## Size of the grid
        self.max_steps = 30 

        ## Define the action and observation spaces
        self.action_space = spaces.Discrete(4)  # Up, Down, Left, Right

        self.observation_space = spaces.Box(low=0, high=4, shape=(4,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Randomly position the agent
        self.agent_pos = self.np_random.integers(
            0, self.grid_size, size=2
        )

        # Randomly position the target
        self.target_pos = self.np_random.integers(
            0, self.grid_size, size=2
        )

        # Make sure they don't start in the same position
        while np.array_equal(self.agent_pos, self.target_pos):
            self.target_pos = self.np_random.integers(
                0, self.grid_size, size=2
            )

        # Reset step counter
        self.steps = 0

        # Return observation and information
        return self._get_observation(), {}

    def _get_observation(self):
        return np.array([self.agent_pos[0], self.agent_pos[1], self.target_pos[0], self.target_pos[1]], dtype=np.float32)

    def step(self, action):
        old_distance = np.abs(self.agent_pos - self.target_pos).sum()

        if action == 0:  # Up
            self.agent_pos[1] -= 1

        elif action == 1:  # Down
            self.agent_pos[1] += 1

        elif action == 2:  # Left
            self.agent_pos[0] -= 1

        elif action == 3:  # Right
            self.agent_pos[0] += 1

        self.agent_pos = np.clip(self.agent_pos, 0, self.grid_size - 1)

        self.steps += 1
        new_distance = np.abs(self.agent_pos - self.target_pos).sum()

        reward = -0.01

        if new_distance < old_distance:
            reward += 0.2

        elif new_distance > old_distance:
            reward -= 0.2

        terminated = np.array_equal(self.agent_pos, self.target_pos)
        truncated = self.steps >= self.max_steps

        if terminated:
            reward += 10.0

        truncated = self.steps >= self.max_steps

        return(self._get_observation(), reward, terminated, truncated, {})