from src.app import bot, init_app

if __name__ == '__main__':
    init_app()
    bot.run_until_disconnected()
