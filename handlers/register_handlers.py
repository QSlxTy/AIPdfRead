from handlers.user.register_user_handlers import register_user_handler



async def register_handlers(dp):
    register_user_handler(dp)

