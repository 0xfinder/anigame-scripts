import os
from pathlib import Path
import json
import discum
from discum.utils.button import Buttoner
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

bot = discum.Client(token=os.getenv("TOKEN"), log={
                    "console": False, "file": False})

here = Path(__file__).resolve()
with open(here.parents[0] / 'config.json') as f:
    config = json.load(f)

channelID = int(config["channelID"])


@bot.gateway.command
def helloWorld(resp):
    if resp.event.ready_supplemental:
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(
            user['username'], user['discriminator']))
    if resp.event.message:
        m = resp.parsed.auto()
        if m["channel_id"] == channelID and m["author"]["id"] == '723416058945601546':
            if '107390189353103360' in m['content'] and 'your Raid Energy is at your set Energy Cap' in m['content']:
                bot.sendMessage(m['channel_id'], '.rd bt all')


@bot.gateway.command
def anigame(resp):
    if resp.event.message or resp.event.message_updated:
        m = resp.parsed.auto()
        try:
            if m['author']['id'] == '571027211407196161' and m['channel_id'] == channelID:
                if len(m["components"]) > 0:
                    embeds = m['embeds'][0]
                    if len(embeds) > 0:
                        target_str = "__Raid Boss Battle__"
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
                            print('started raid')
        except:
            pass


bot.gateway.run(auto_reconnect=True)
