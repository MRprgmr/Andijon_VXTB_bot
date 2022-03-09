from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
REQUIRED_CHANNELS = env.list("REQUIRED_CHANNELS")
CHANNELS_NAMES = env.list("CHANNELS_NAMES")
CHANNELS = env.list("CHANNELS")
SERVER = env.str("SERVER")
