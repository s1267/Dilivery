import django

from utils.set_bot_commands import set_default_command
import os


async def on_startup(dp):
    from utils.notify_admins import on_startup_notify

    await set_default_command(dp=dp)
    await on_startup_notify(dp=dp)


def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproject.djangoproject.settings')
    os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
    django.setup()


if __name__ == '__main__':
    setup_django()
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
