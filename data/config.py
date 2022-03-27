from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
REQUIRED_CHANNELS = env.list("REQUIRED_CHANNELS")
CHANNELS_NAMES = env.list("CHANNELS_NAMES")
CHANNELS = env.list("CHANNELS")
DATABASE_CHANNEL = env.int("DATABASE_CHANNEL")
SERVER = env.str("SERVER")
