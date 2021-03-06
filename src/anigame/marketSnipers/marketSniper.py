from dotenv import load_dotenv, find_dotenv
import json
from pathlib import Path
import os
import re
import discord

load_dotenv(find_dotenv())


TOKEN = os.getenv("TOKEN")
here = Path(__file__).resolve()
with open(here.parents[0] / 'config.json') as f:
    config = json.load(f)

channelID = int(config["channelID"])


class MarketSniper(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set up the UR and SR costs
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
                    channel = client.get_channel(channelID)
                    if cost <= 50:
                        await channel.send(f'.mk cbuy {cardID}')
                    elif cost > 50:
                        if cost <= self.URcost and rar == 'Ultra Rare':
                            await channel.send(f'.mk cbuy {cardID}')
                        elif cost <= self.SRcost and rar == 'Super Rare':
                            await channel.send(f'.mk cbuy {cardID}')
                except Exception as e:
                    print(e)


client = MarketSniper()
client.run(TOKEN)
