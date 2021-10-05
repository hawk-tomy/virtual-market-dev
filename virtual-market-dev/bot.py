#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import traceback
from io import StringIO
from logging import getLogger
from os import getenv

from discord import AllowedMentions, File, Game, Intents
from discord.ext import commands

from cogs import extension
from lib import Context, Embed, Help, split_line

logger = getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self):
        intents = Intents.all()
        intents.typing = False
        allowed_mentions = AllowedMentions.all()
        allowed_mentions.everyone = False
        allowed_mentions.replied_user = False

        super().__init__(
            allowed_mentions=allowed_mentions,
            command_prefix='/',
            description='this is a virtual market bot.',
            help_command=Help(self.default_embed_color),
            intents=intents,
        )

        self.__default_embed: Embed= Embed(color=self.default_embed_color)

        for cog in extension:
            self.load_extension(cog)

    @property
    def default_embed_color(self)-> int:
        return int(getenv('DEFAULT_EMBED_COLOR'))

    @property
    def default_embed(self)-> Embed:
        return self.__default_embed.copy()

    def run(self):
        return super().run(getenv('DISCORD_BOT_TOKEN'))

    async def on_ready(self):
        logger.info('login success')
        await self.change_presence(activity=Game('/help'))
        appinfo = await self.application_info()
        self.owner_id = appinfo.owner.id
        await self.get_user(self.owner_id).send('起動しました。')

    async def on_command_error(self, ctx: Context, exc: commands.CommandError):
        if ctx.invoked_error:
            return
        if isinstance(exc, commands.MissingRequiredArgument):
            await ctx.re_error(f'`{exc.param.name}`は必須です。')
            return
        log_msg = f'Ignoring exception in command {ctx.command}:'
        err_msg = f'{log_msg}\n{"".join(traceback.format_exception(type(exc), exc, exc.__traceback__))}'
        logger.exception(log_msg, exc_info=exc)
        if len(err_msg) < 5000:
            embed = self.default_embed
            embed.title = 'traceback (on_command_error)'
            for msg in split_line(err_msg, 1000):
                embed.add_field(name='traceback', value=f'```py\n{msg}\n```', inline=False)
            await self.get_user(self.owner_id).send(embed=embed)
        else:
            await self.get_user(self.owner_id).send(file=File(fp=StringIO(err_msg), filename='tb_command_error.py'))

    async def on_error(self, event_method, *args, **kwargs):
        log_msg = f'Ignoring exception in {event_method}:'
        err_msg = f'{log_msg}\n{traceback.format_exc()}'
        logger.exception(log_msg)
        if len(err_msg) < 5000:
            embed = self.default_embed
            embed.title = 'traceback (on_error)'
            for msg in split_line(err_msg, 1000):
                embed.add_field(name='traceback', value=f'```py\n{msg}\n```', inline=False)
            await self.get_user(self.owner_id).send(embed=embed)
        else:
            await self.get_user(self.owner_id).send(file=File(fp=StringIO(err_msg), filename='tb_error.py'))
