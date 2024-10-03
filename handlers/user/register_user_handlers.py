from handlers.user import start, get_file


def register_user_handler(dp):
    start.register_start_handler(dp)
    get_file.register_handler(dp)
