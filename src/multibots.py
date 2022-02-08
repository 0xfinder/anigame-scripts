import time
import threading
from discum.utils.button import Buttoner
import discum
import os
import sys
from dotenv import load_dotenv
load_dotenv()


autoReconnectOption = True
gold = 10000
consoleLog = False
fileLog = False
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tokens.txt")) as f:
    tokenlist = f.read().splitlines()


def closeAfterReadySupp(resp, bot, channelID, ownerID, gold):
    if resp.event.ready_supplemental:
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(
            user['username'], user['discriminator']))
        bot.sendMessage(channelID, "`Initialized`, starting...")
        while True:
            time.sleep(2)
            bot.sendMessage(channelID, '.bt all')
            time.sleep(2)
            bot.sendMessage(channelID, '.hourly')
            time.sleep(0.5)
            bot.sendMessage(channelID, f'.give <@{ownerID}> {gold}')
            time.sleep(3601)


def anigame(resp, bot, channelID):
    if resp.event.message or resp.event.message_updated:
        m = resp.parsed.auto()
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
                        print("Clicked button")


clients = []
for i in range(len(tokenlist)):
    if i == 0:
        clients.append(discum.Client(token=tokenlist[0], log={
                       "console": consoleLog, "file": fileLog}))
        build_num = clients[0]._Client__super_properties['client_build_number']
    else:
        clients.append(discum.Client(token=tokenlist[i], build_num=build_num, log={
                       "console": consoleLog, "file": fileLog}))
    clients[i].gateway.command({"function": closeAfterReadySupp, "params": {
                               "bot": clients[i], "channelID": os.getenv(f"CHANNEL{i % 50}"), "ownerID": os.getenv("OWNERID"), "gold": gold}})
    clients[i].gateway.command({"function": anigame, "params": {
                               "bot": clients[i], "channelID": os.getenv(f"CHANNEL{i % 50}")}})


def gatewayRunner(bot, result, index):
    bot.gateway.run(auto_reconnect=autoReconnectOption)
    result[index] = bot.gateway.session.user


num_clients = len(clients)
threads = [None] * num_clients
results = [None] * num_clients

for i in range(num_clients):
    threads[i] = threading.Thread(target=gatewayRunner, args=(
        clients[i], results, i))
    threads[i].start()
    time.sleep(5)

time.sleep(10)
sys.exit()
