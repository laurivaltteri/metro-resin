#!/usr/bin/python
# -*- coding: utf-8 -*-
'''Main script for polling stuff for display'''

import config
from twitter import Api
import pychromecast
import spotipy, spotipy.util
from time import sleep, strftime, strptime, gmtime, mktime
import datetime
from serial import Serial, SEVENBITS, STOPBITS_ONE, PARITY_EVEN
from random import randint
import re
import unicodedata
import telegram
import feedparser

## GLOBAL VARS
STX = chr(2); ETX = chr(3); EOT = chr(4); ENQ = chr(5); PAD = chr(127)
SLP = 1
hour = int(strftime("%H"))

## SET a TELEGRTAM BOT (metraspbot)
print("Setting up telegram bot..")
bot = telegram.Bot(token=config.TELEGRAM_TOKEN)
bot.get_updates()

## SET TWITTER API
# https://apps.twitter.com/app/14318063/keys
print("Setting up twitter api..")
api = Api(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET,
    config.TWITTER_ACCESS_KEY, config.TWITTER_ACCESS_SECRET)

## CHECK FOR CHROMECASTS
print("Setting up chromecasts acknowledged..")
cnames = pychromecast.discover_chromecasts(timeout = 10)
chromecasts = pychromecast.get_chromecasts(cnames)
shortnames = {u'YouTube': u'Tube', u'Yle Areena': u'Yle', u'HBO Nordic': u'HBO',
    u'Netflix': u'Flix',u'Katsomo Chromecast APP': u'MTV3',
    u'Katsomo Chromecast Desktop':u'MTV3'}

## SET SPOTIFY API
token = spotipy.util.prompt_for_user_token("ahonenlauri",
    "user-read-currently-playing", client_id = config.SPOTIPY_CLIENT_ID,
    client_secret = config.SPOTIPY_CLIENT_SECRET)

print("Setting up spotify api..")
sp = spotipy.Spotify(auth=token)

## SET SERIAL PORT
print("Setting up serial port..")
ser = Serial("/dev/ttyUSB0", 600, SEVENBITS, PARITY_EVEN, STOPBITS_ONE)
#ser = Serial("/dev/tty.UC-232AC", 600, SEVENBITS, PARITY_EVEN, STOPBITS_ONE)

## ----------------

## FUNCTIONS

def send_ser(linestr):
    linestr = unicode(linestr)
    padline = PAD + PAD + linestr + PAD + PAD
    padline = unicodedata.normalize('NFKD', padline).encode("ascii", "ignore")
    ser.write(bytearray(padline))

def write_line(message, seg):
    send_ser(EOT)
    sleep(SLP)
    send_ser("01" + ENQ) # address (from dip switches)
    sleep(SLP)

    if seg == 3:
        send_ser(STX + "32000blT" + clear_scands(message) + ETX + "p")
    elif seg == 2 and len(message) < 22:
        send_ser(STX + "22000nrT" + clear_scands(message) + ETX + "p")
    elif seg == 1 and len(message) < 22:
        send_ser(STX + "12000nrT" + clear_scands(message) + ETX + "p")
    elif len(message) > 21:
        spaces = [m.start(0) for m in re.finditer(u' ', message)]
        #spaces = [x - len(message) for x in spaces]
        spltidx = [i for i in spaces if i < 21]
        if len(spltidx) > 0:
            send_ser(STX + "12000nrT" + clear_scands(message[:spltidx[-1]]) + ETX + "p")
        else:
            send_ser(STX + "12000nrT" + clear_scands(message[:20]) + ETX + "p")
        send_ser(EOT)
        sleep(SLP)
        send_ser(EOT)
        sleep(SLP)
        send_ser("01" + ENQ) # address (from dip switches)
        sleep(SLP)
        if len(message) > 41 and len(spltidx) > 0:
            send_ser(STX + "22000nlT" + clear_scands(message[spltidx[-1]+1:spltidx[-1]+21]+u'..') + ETX + "p")
        elif len(spltidx) > 0:
            send_ser(STX + "22000nlT" + clear_scands(message[spltidx[-1]+1:]) + ETX + "p")
        else:
            send_ser(STX + "22000nlT" + clear_scands(message[20:]) + ETX + "p")
    else:
        print("nothing sent to serial")
    send_ser(EOT)
    sleep(SLP)

def clear_scands(message):
    message = message.replace(u'ä', chr(123))
    message = message.replace(u'ö', chr(124))
    message = message.replace(u'å', chr(125))
    message = message.replace(u'Ä', chr(91))
    message = message.replace(u'Ö', chr(92))
    message = message.replace(u'Å', chr(93))
    message = message.replace(u'ü', chr(126))
    message = message.replace(u'Ü', chr(94))
    message = message.replace(u'É', chr(64))
    message = message.replace(u'é', chr(96))
    message = message.replace(u'Ø', u'O')
    message = message.replace(u'ø', u'o')
    message = message.replace(u'[', u'(')
    message = message.replace(u']', u')')
    return message

def default_disp():
    # WRITE INFO
    tstr = "%s:%s" % (strftime("%H"), strftime("%M"))
    info = u'Tweet'.ljust(5)+tstr.rjust(5)
    write_line(info, 3)

    # TWITTER TRENDS
    # WOE_ID for Finland not existing
    # api.GetTrendsWoeid(23424954) # Sweden
    ctrnd = api.GetTrendsCurrent()
    ctrnd = list(iter(cc for cc in ctrnd if all(ord(c) < 128 for c in cc.name)))
    twtrln = ctrnd[randint(0,9)].name
    write_line(twtrln, 1)

    # DATE
    dayn = int(strftime("%d"))
    dayn = "%d%s" % (dayn, "tsnrhtdd"[(dayn/10%10!=1) * (dayn%10<4) * dayn%10::4])

    dateln = strftime("%a ") + dayn + strftime(" of %b, %Y")
    write_line(dateln, 2)

def news_disp():
    feed = feedparser.parse("http://feeds.feedburner.com/ampparit-uutiset")
    feedln = feed.entries[randint(0,9)]
    uutinen = feedln.title
    lahde = "\ \(" + feedln.author + "\)"
    uutinen = re.sub(lahde,"",uutinen)
    write_line(u'News', 3)
    write_line(uutinen, 1)

def cast_info(cc,mc,dname):
    if dname in shortnames:
        msource = shortnames[dname]
    else:
        msource = dname

    if mc.duration is not None:
        dur = mc.current_time/mc.duration
        dur = int(round(dur*5))*chr(127)
        ms_dur = msource.ljust(5)+dur
        write_line(ms_dur, 3)
        sleep(SLP)
    else:
        write_line(msource, 3)

    if dname == u'Netflix' or dname == u'Ruutu':
        write_line(cc.status.status_text, 1)
        return
    else:
        write_line(mc.title, 1)

    if mc.artist:
        write_line(mc.artist, 2)
    elif 'item' in mc.media_custom_data:
        write_line(mc.media_custom_data['item']['title'], 2)
    elif u'subtitle' in mc.media_metadata:
        write_line(mc.media_metadata[u'subtitle'], 2)
    else:
        # DATE
        dayn = int(strftime("%d"))
        dayn = "%d%s" % (dayn, "tsnrhtdd"[(dayn/10%10!=1) * (dayn%10<4) * dayn%10::4])

        dateln = strftime("%a ") + dayn + strftime(" of %b, %Y")
        write_line(dateln, 2)


def spotify_info(sitem):
    artist = sitem['item']['artists'][0]['name']
    song = sitem['item']['name']

    tstr = "%s:%s" % (strftime("%H"), strftime("%M"))
    info = u'Sptfy'.ljust(5)+tstr.rjust(5)
    write_line(info, 3)

    write_line(song, 1)
    write_line(artist, 2)

def disp_message(message, fromid):
    write_line(fromid, 3)
    write_line(message, 1)


while 1:
    #print(u'ok')


    metweet = api.GetSearch(u'#metronäyttö',since = strftime("%Y-%m-%d",gmtime()))
    if len(metweet) > 0:
        mtime = strptime(metweet[0].created_at, '%a %b %d %H:%M:%S +0000 %Y')
        if mktime(gmtime()) - mktime(mtime) < 3600:
            metweet = metweet[0].text.replace(u'#metronäyttö',u'')
            disp_message(metweet, u'Tweet')

    if len(bot.get_updates()) > 0:
        mdel = datetime.datetime.now() - bot.get_updates()[-1].message.date
        if  mdel.seconds < 3600:
            fromuser = "telegram from " + bot.get_updates()[-1].message.chat.username
            disp_message(fromuser, u'Teleg')
            write_line(u' ', 2)
            disp_message(bot.get_updates()[-1].message.text, u'Teleg')


    if sp.currently_playing() != None:
        if sp.currently_playing()['is_playing']==True:
            spotify_info(sp.currently_playing())
        else:
            for cc in chromecasts:
                cc.wait()
                cc.media_controller._fire_status_changed()
                mc = cc.media_controller.status
                if mc.player_state == u'PLAYING' or cc.status.display_name == u'Ruutu':
                    cast_info(cc, mc, cc.status.display_name)
                else:
                    default_disp()
                    #news_disp()
    else:
        for cc in chromecasts:
            cc.wait()
            cc.media_controller._fire_status_changed()
            mc = cc.media_controller.status
            if mc.player_state == u'PLAYING' or cc.status.display_name == u'Ruutu':
                cast_info(cc, mc, cc.status.display_name)
            else:
                default_disp()
                #news_disp()
    sleep(SLP)
