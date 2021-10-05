from __future__ import annotations


from logging import getLogger


from discord.ext import commands


logger = getLogger(__name__)


class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Market(bot))
