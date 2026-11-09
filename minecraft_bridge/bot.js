
const mineflayer = require("mineflayer");
const WebSocket = require("ws");

// Minecraft settings
const MINECRAFT_PORT = 54321; // Your actual LAN port
const WS_PORT = 8765;

// Connect to Minecraft
const bot = mineflayer.createBot({
    host: "localhost",
    port: MINECRAFT_PORT,
    username: "MineMind",
    auth: "offline",
    version: "1.21.4"
});

// Track whether Minecraft is ready
let botReady = false;

bot.once("spawn", () => {
    botReady = true;
    console.log("MineMind entered Minecraft!");
    console.log("Position:", bot.entity.position);
});

// Create local WebSocket server
const wss = new WebSocket.Server({
    host: "127.0.0.1",
    port: WS_PORT
});

console.log(`Python bridge listening on port ${WS_PORT}`);

// Read current Minecraft state
function getObservation() {
    const pos = bot.entity.position;

    return {
        x: pos.x,
        y: pos.y,
        z: pos.z,
        yaw: bot.entity.yaw,
        health: bot.health,
        food: bot.food
    };
}

// Process commands from Python
wss.on("connection", (socket) => {
    console.log("Python connected!");

    socket.on("message", async (message) => {
        let command;

        try {
            command = JSON.parse(message.toString());

            if (!botReady || !bot.entity) {
                socket.send(JSON.stringify({
                    error: "Minecraft bot is not ready"
                }));
                return;
            }

            // Return current state
            if (command.action === "observe") {
                socket.send(JSON.stringify({
                    observation: getObservation()
                }));
                return;
            }

            // Allowed movement controls
            const controls = [
                "forward",
                "back",
                "left",
                "right",
                "jump"
            ];

            if (!controls.includes(command.action)) {
                socket.send(JSON.stringify({
                    error: "Unknown action"
                }));
                return;
            }

            // Move for a fixed number of game ticks
            bot.clearControlStates();
            bot.setControlState(command.action, true);

            await bot.waitForTicks(10);

            bot.clearControlStates();

            // Allow Minecraft to update its state
            await bot.waitForTicks(2);

            socket.send(JSON.stringify({
                action: command.action,
                observation: getObservation()
            }));

        } catch (error) {
            bot.clearControlStates();

            socket.send(JSON.stringify({
                error: error.message
            }));
        }
    });

    socket.on("close", () => {
        bot.clearControlStates();
        console.log("Python disconnected");
    });
});

bot.on("error", (error) => {
    console.error("Minecraft error:", error.message);
});

bot.on("end", (reason) => {
    botReady = false;
    console.log("Minecraft disconnected:", reason);
});

