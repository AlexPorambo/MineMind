from environment import MineMindEnv

env = MineMindEnv()

observation, info = env.reset()

print("Starting observation:", observation)

observation, reward, terminated, truncated, info = env.step(0)

print("New observation:", observation)
print("Reward:", reward)
print("Terminated:", terminated)
print("Truncated:", truncated)

env.close()