import discord
from typing import List

# TODO(tamton-aquib): disable buttons if only one item
class BotEmbedPaginator(discord.ui.View):

    def __init__(self, embeds: List[discord.Embed]):
        super().__init__(timeout=30)
        self.index = 0
        self.embeds = embeds

    @discord.ui.button(label='back', style=discord.ButtonStyle.blurple)
    async def back(self, interaction: discord.Interaction, _):
        self.index = len(self.embeds) - 1 if self.index == 0 else self.index - 1

        await interaction.response.edit_message(embed=self.embeds[self.index])

    @discord.ui.button(label='forth', style=discord.ButtonStyle.blurple)
    async def forth(self, interaction: discord.Interaction, _):
        self.index = 0 if self.index == len(self.embeds)-1 else self.index + 1

        await interaction.response.edit_message(embed=self.embeds[self.index])
