import re
import time
import os
import discum
from discum.utils.button import Buttoner
from dotenv import load_dotenv
load_dotenv()

bot = discum.Client(token=os.getenv("TOKEN"), log={
                    "console": False, "file": False})

channelID = '915817078898962493'
counter = 0


@bot.gateway.command
def helloWorld(resp):
    if resp.event.ready_supplemental:
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(
            user['username'], user['discriminator']))
        bot.sendMessage(channelID, "`Initialized`, starting...")
    if resp.event.message:
        m = resp.parsed.auto()
        if m["channel_id"] == channelID and m["author"]["id"] == '723416058945601546':
            if 'your Hourly cooldown is over' in m['content'] and '107390189353103360' in m['content']:
                bot.sendMessage(channelID, ".hourly")
                print('hourly')
            if 'your Lottery cooldown is over' in m['content'] and '107390189353103360' in m['content']:
                bot.sendMessage(channelID, ".lottery")
                print('lottery')
        if m['content'] == '.hourly' and m['author']['id'] == '107390189353103360':
            bot.sendMessage(m['channel_id'], '.fl n')
            time.sleep(1)
            bot.sendMessage(m['channel_id'], '.bt')


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
                elif len(m['embeds'][0]) > 0:
                    if "Congratulations!" in m['embeds'][0].get('title', ''):
                        locationRegex = re.compile(r'\d+')
                        mo = locationRegex.search(
                            m['embeds'][0].get('description', ''))
                        bot.sendMessage(m['channel_id'],
                                        f'.loc {int(mo.group()) + 1}')
                    if "Victory" in m['embeds'][0].get('title', ''):
                        bot.sendMessage(m['channel_id'], '.fl n')
                        time.sleep(1)
                        bot.sendMessage(m['channel_id'], '.bt')
                    if "Defeated" in m['embeds'][0].get('title', ''):
                        time.sleep(1)
                        bot.sendMessage(m['channel_id'], '.bt')
        except:
            pass


bot.gateway.run(auto_reconnect=True)
