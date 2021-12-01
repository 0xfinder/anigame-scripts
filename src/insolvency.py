from dotenv import load_dotenv
load_dotenv()

import discum, os, time
bot = discum.Client(token=os.getenv("TOKEN"), log={"console":True, "file":False})

from discum.utils.button import Buttoner

@bot.gateway.command
def helloWorld(resp):
    if resp.event.ready_supplemental:
            user = bot.gateway.session.user
            print("Logged in as {}#{}".format(user['username'], user['discriminator']))
            bot.sendMessage("851379765164245032", "Initialized, starting...")
    if resp.event.message:
        m = resp.parsed.auto()
        if m['content'] == 'Initialized, starting...':
          while True: 
            bot.sendMessage(m['channel_id'], '.hourly')
            time.sleep(1)
            bot.sendMessage(m['channel_id'], '.bt all')
            time.sleep(6)

@bot.gateway.command
def anigame(resp):
    if resp.event.message or resp.event.message_updated:
        m = resp.parsed.auto()
        try:
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

bot.gateway.run(auto_reconnect=False)