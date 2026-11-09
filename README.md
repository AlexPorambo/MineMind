# MineMind — Reinforcement Learning Minecraft Agent

MineMind is a reinforcement learning project exploring how an AI agent can learn to navigate and interact with Minecraft. The project began with a custom grid-world environment and now includes a Python-to-Minecraft communication bridge.

## Project Overview

The initial environment is a 5×5 grid where an agent learns to reach randomized targets using Proximal Policy Optimization (PPO). The next stage connects Python to Minecraft Java Edition through a Node.js Mineflayer bot and WebSockets.

## Current Features

### Grid-World Reinforcement Learning
- Custom 5×5 Gymnasium environment
- PPO training using Stable-Baselines3
- Four movement actions and distance-based rewards
- Randomized agent and target positions
- Matplotlib movement visualization
- 100% success rate and 3.1 average steps over 100 evaluation episodes

### Minecraft Integration
- Mineflayer bot connected to Minecraft Java Edition 1.21.4
- Node.js WebSocket server communicating with Python
- Python-issued forward, back, left, right, and jump commands
- Observation of bot position, yaw, health, and food
- Tested movement through a Python controller

## Technologies

| Technology | Purpose |
|---|---|
| Python | Training, evaluation, and control |
| Gymnasium | Custom RL environment |
| Stable-Baselines3 | PPO algorithm |
| Matplotlib | Visualization |
| Node.js | Minecraft bridge |
| Mineflayer | Minecraft bot |
| WebSockets (`ws`, `websocket-client`) | Python–Node.js messaging |
| Minecraft Java Edition 1.21.4 | Game environment |

## Project Structure

```text
MineMind/
├── environment.py
├── train.py
├── evaluate.py
├── visualize.py
├── minecraft_test.py
├── minecraft_bridge/
│   ├── bot.js
│   ├── package.json
│   └── package-lock.json
└── README.md
```

## Getting Started

### 1. Install Python dependencies

With your Python virtual environment activated:

```powershell
python -m pip install gymnasium stable-baselines3 matplotlib websocket-client
```

### 2. Install Node.js dependencies

```powershell
cd minecraft_bridge
npm install
```

### 3. Launch Minecraft

Launch **Minecraft Java Edition 1.21.4**. Create a Creative Superflat world and open it to LAN. Update `MINECRAFT_PORT` in `minecraft_bridge/bot.js` to match the LAN port displayed in Minecraft.

### 4. Start the bridge

From `minecraft_bridge/`:

```powershell
node bot.js
```

Leave this process running.

### 5. Test Python control

In a second terminal, from the project root:

```powershell
python minecraft_test.py
```

The Python script sends movement commands and prints updated Minecraft observations.

## Architecture

1. Python sends an action over a local WebSocket connection.
2. The Node.js bridge receives the command.
3. Mineflayer performs the movement in Minecraft.
4. The bridge reads the updated bot state.
5. Python receives the observation.

The WebSocket server listens on `127.0.0.1:8765` by default. This is separate from Minecraft's LAN port.

## Next Steps

- Wrap Minecraft interactions in a Gymnasium environment
- Add reliable episode resets and randomized targets
- Train a new PPO agent directly on Minecraft observations
- Introduce obstacles and more challenging navigation
- Explore environmental sensing and visual perception

## Status

**In development — Minecraft communication bridge working.** The original grid-world model has been trained and evaluated, and the Minecraft bot can be controlled through Python. A new Minecraft-specific reinforcement learning environment and model are planned; the grid-world model has not yet been trained in Minecraft.
