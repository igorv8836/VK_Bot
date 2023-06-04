import datetime
import time
import traceback

import Bot

t1 = time.time()
bot = Bot.Bot()
t2 = time.time()
print('Время запуска: ', t2 - t1)
while True:
    try:
        print("Bot is ready")
        bot.start()
    except Exception:
        traceback.print_exc()
        print('Error')

