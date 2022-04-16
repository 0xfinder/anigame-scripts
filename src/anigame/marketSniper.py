import discord
import re
import os

from discord.ext import tasks

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")
myChannel = 901349981343064104


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SRcost = 250
        self.URcost = 30000

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.channel.id == 758956287937085450:
            embeds = message.embeds
            for embed in embeds:
                try:
                    detailsOfEmbed = embed.to_dict()
                    desc = detailsOfEmbed['description']
                    details = desc.split('\n')[1]
                    rarity = details.split(' | ')
                    rar = rarity[0]
                    cost = int(detailsOfEmbed['title'].split("__")[1])
                    cardID = re.findall(
                        r'\d+', detailsOfEmbed['footer']['text'])[0]
                    channel = client.get_channel(myChannel)
                    if cost <= 50:
                        await channel.send(f'.mk cbuy {cardID}')
                    elif cost > 50:
                        if cost <= self.URcost and rar == 'Ultra Rare':
                            await channel.send(f'.mk cbuy {cardID}')
                        elif cost <= self.SRcost and rar == 'Super Rare':
                            await channel.send(f'.mk cbuy {cardID}')
                except Exception as e:
                    print(e)


client = MyClient()
client.run(TOKEN)
