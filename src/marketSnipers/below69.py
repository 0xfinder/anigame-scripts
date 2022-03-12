import discord
import re

import os

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")
CHANNEL = 69696969699696
COST = 69
PREFIX = "."
ANIGAME_GLOBAL_MARKET_CHANNEL = 758956287937085450

'''
Buys any UR/SR below 69 gold
'''


class MarketSniper(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.channel.id == ANIGAME_GLOBAL_MARKET_CHANNEL:
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
                    channel = client.get_channel(CHANNEL)
                    if cost <= COST and rar in ['Ultra Rare', 'Super Rare']:
                        await channel.send(f'{PREFIX}mk cbuy {cardID}')
                except Exception as e:
                    print(e)


client = MarketSniper()
client.run(TOKEN)
