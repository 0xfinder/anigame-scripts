import time
import os
import discum
from discum.utils.button import Buttoner
from dotenv import load_dotenv
load_dotenv()

bot = discum.Client(token=os.getenv("TOKEN"), log={
                    "console": False, "file": False})

channelID = '915817078898962493'


@bot.gateway.command
def helloWorld(resp):
    if resp.event.ready_supplemental:
        user = bot.gateway.session.user
        counter = 0
        print("Logged in as {}#{}".format(
            user['username'], user['discriminator']))
        bot.sendMessage(channelID, "`Initialized`, starting...")
        while True:
            if counter % 6 == 0:
                bot.sendMessage(channelID, '.hourly')
            time.sleep(2)
            bot.sendMessage(channelID, '.bt all')
            time.sleep(2)
            bot.sendMessage(channelID, '.lottery')
            time.sleep(600)
            counter += 1


@bot.gateway.command
def anigame(resp):
    if resp.event.message or resp.event.message_updated:
        m = resp.parsed.auto()
        try:
            if m['author']['id'] == '571027211407196161' and m['channel_id'] == channelID:
                if len(m["components"]) > 0:
                    embeds = m['embeds'][0]
                    if len(embeds) > 0:
                        target_str = "Challenging Area"
                        if target_str in embeds.get('title', ''):
                            buts = Buttoner(m['components'])
                            bot.click(
                                m["author"]["id"],
                                channelID=m["channel_id"],
                                guildID=m.get('guild_id'),
                                messageID=m["id"],
                                messageFlags=m["flags"],
                                data=buts.getButton(row=0, column=0)
                            )
        except:
            pass


bot.gateway.run(auto_reconnect=True)
