import json
import math
import random

import gymnasium as gym
import numpy as np
import websocket
from gymnasium import spaces

class MinecraftEnv(gym.Env):
    def __init__(self):
        super().__init__()

        #Connect to Minecraft
        self.ws = websocket.create_connection("ws://127.0.0.1:8765", timeout=15)

        #Available actions
        self.actions = [
            "forward",
            "back",
            "left",
            "right"
        ]

        self.action_space = spaces.Discrete(4)


        #Observation
        #[x,y, target_x, target_z, distance]
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(5,),
            dtype=np.float32
        )

        self.start_x = 0.5
        self.start_y = -59
        self.start_z = 0.5

        self.target_x = 0
        self.target_z = 0

        self.steps = 0
        self.max_steps = 50

    def send_command(self, command):
        self.ws.send(json.dumps(command))

        response = json.loads(self.ws.recv())

        if "error" in response:
            raise RuntimeError(response["error"])

        return response["observation"]

    def get_observation(self, state):
        x = state["x"]
        z = state["z"]

        distance = math.dist(
            (x, z),
            (self.target_x, self.target_z)
        )

        return np.array([
            x,
            z,
            self.target_x,
            self.target_z,
            distance
        ], dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.steps = 0

        # Random target near the starting position
        self.target_x = self.start_x + int(
            self.np_random.integers(-5, 6)
        )
        self.target_z = self.start_z + int(
            self.np_random.integers(-5, 6)
        )

        # Avoid spawning the target at the start
        while (
            self.target_x == self.start_x
            and self.target_z == self.start_z
        ):
            self.target_x = self.start_x + int(
                self.np_random.integers(-5, 6)
            )
            self.target_z = self.start_z + int(
                self.np_random.integers(-5, 6)
            )

        state = self.send_command({
            "action": "reset",
            "x": self.start_x,
            "y": self.start_y,
            "z": self.start_z
        })

        # Verify the reset actually worked
        if math.dist(
            (state["x"], state["z"]),
            (self.start_x, self.start_z)
        ) > 0.5:
            raise RuntimeError(
                "Minecraft reset failed: bot is not at start"
            )

        observation = self.get_observation(state)

        return observation, {}

    def step(self, action):
        self.steps += 1

        # Observe distance before moving
        before = self.send_command({
            "action": "observe"
        })

        old_distance = math.dist(
            (before["x"], before["z"]),
            (self.target_x, self.target_z)
        )

        # Execute action in Minecraft
        state = self.send_command({
            "action": self.actions[int(action)]
        })

        observation = self.get_observation(state)
        new_distance = float(observation[4])

        # Reward based on actual progress
        reward = (old_distance - new_distance) * 1.0

        # Small penalty to encourage efficiency
        reward -= 0.01

        terminated = new_distance < 1.0
        truncated = self.steps >= self.max_steps

        if terminated:
            reward += 10.0

        info = {
            "distance": new_distance,
            "success": terminated,
            "steps": self.steps
        }

        return (
            observation,
            reward,
            terminated,
            truncated,
            info
        )

    def close(self):
        if self.ws:
            self.ws.close()
            self.ws = None
