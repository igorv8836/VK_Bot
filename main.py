import datetime
import traceback

import Bot


bot = Bot.Bot()
while True:
    try:
        bot.start()
    except Exception:
        traceback.print_exc()
        print('Error')

