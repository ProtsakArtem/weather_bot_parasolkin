from aiogram import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.planer import sub_alert, sub_everyday, parse_start
from src.config import dp
from apscheduler.triggers import cron
from src.handlers import users
from src.services.weather_sql import check_weather_data_table
from src.services.user_sql import check_create_database, check_user_table
scheduler = AsyncIOScheduler()
scheduler.add_job(sub_everyday, trigger=cron.CronTrigger(hour=8))
scheduler.add_job(sub_alert, trigger=cron.CronTrigger(hour=8, minute=2))
scheduler.add_job(parse_start, trigger=cron.CronTrigger(hour=0, minute=2))
scheduler.start()

check_create_database()
check_user_table()
check_weather_data_table()
executor.start_polling(dp, skip_updates=True)