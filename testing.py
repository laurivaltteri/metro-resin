import telegram
import config
import datetime
import sys
import feedparser
print (sys.version)
import pychromecast


cnames = pychromecast.discover_chromecasts(timeout = 10)
chromecasts = pychromecast.get_chromecasts(cnames)



bot = telegram.Bot(token=config.TELEGRAM_TOKEN)
bot.get_updates()

len(bot.get_updates())
bot.get_updates()[-1].message.text
bot.get_updates()[-1].message.chat.username

mdel = datetime.datetime.now() - bot.get_updates()[-1].message.date
mdel.seconds
