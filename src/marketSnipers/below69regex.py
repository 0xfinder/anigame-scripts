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
Buys any UR/SR below 69 but with regex
'''

rarityRegex = re.compile(r'\*\*\s(.*)\s\|\sL')
costRegex = re.compile(r'\d+')


class MarketSniperRegex(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                    rarity = rarityRegex.search(
                        detailsOfEmbed['description']).group(1)
                    cost = int(costRegex.search(
                        detailsOfEmbed['title']).group())
                    cardID = re.findall(
                        r'\d+', detailsOfEmbed['footer']['text'])[0]
                    if cost <= COST and rarity in ['Ultra Rare', 'Super Rare']:
                        await client.get_channel(CHANNEL).send(f'{PREFIX}mk cbuy {cardID} regex')
                except Exception as e:
                    print(e)


client = MarketSniperRegex()
client.run(TOKEN)
