from aiogram import Bot, Dispatcher
from environs import Env


env = Env()
env.read_env()

TOKEN = env.str("BOT_TOKEN")

bot = Bot(
    token=TOKEN
)

dp = Dispatcher(bot)
