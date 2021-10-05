from __future__ import annotations

import traceback
from contextlib import redirect_stdout
from io import StringIO
from logging import getLogger
from pprint import pformat
from textwrap import indent
from typing import TYPE_CHECKING

from bot_util.util import split_line
from discord.ext import commands
from discord.file import File

if TYPE_CHECKING:
    from bot import Bot
    from bot_util import Context, Embed


logger = getLogger(__name__)


class Owner(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self._last_result = None

        logger.info('load extention is success')

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    def cleanup_code(self, code):
        if code.startswith('```') and code.endswith('```'):
            return '\n'.join(code.split('\n')[1:-1])
        return code.strip('` \n')

    @commands.command()
    async def reload(self, ctx: 'Context', *args: str):
        """reload extensions.
        """
        exts: list[str]= list(self.bot.extensions.keys())
        exts_dict = {k.split('.')[-1]: k for k in exts}
        args_ = []
        for arg in args:
            if arg in exts_dict:
                args_.append(exts_dict[arg])
        else:
            if not args_:
                args_ = exts
            args_.sort()
            for ext in args_:
                self.bot.reload_extension(ext)
        args_string = ', '.join(args_)
        logger.info(f'reload success {args_string}')
        await ctx.success(title='reload success', description=args_string, delete_after=10.0)

    @commands.command(name='eval')
    async def eval_(self, ctx: 'Context', *, code: str):
        """run any python code, and return.
        Args:
            code (str): code block or normal string.
        """
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result,
        }
        env.update(globals())
        code = self.cleanup_code(code)
        func_code = f'async def func():\n{indent(code,"    ")}'
        embed: Embed = self.bot.default_embed
        stdout = StringIO()
        files = []
        try:
            exec(func_code, env)
            func = env['func']
            with redirect_stdout(stdout):
                returned = await func()
        except Exception:
            string = traceback.format_exc()
            if len(string) < 2000:
                for msg in split_line(string, 1000):
                    embed.add_field(name='traceback', value=f'```py\n{msg}\n```', inline=False)
            else:
                files.append(File(fp=StringIO(string), filename='traceback.py'))
        else:
            try:
                await ctx.message.add_reaction('\u2705')
            except Exception:
                pass
            if returned is not None:
                self._last_result = returned
                if not isinstance(returned, str):
                    returned = pformat(returned, indent=1, compact=True)
                if len(returned) < 2000:
                    for msg in split_line(returned, 1000):
                        embed.add_field(name='return', value=f'```py\n{msg}```', inline=False)
                else:
                    files.append(File(fp=StringIO(returned), filename='returned.py'))
        finally:
            stdouted = stdout.getvalue()
            if stdouted:
                if len(stdouted) < 2000:
                    for msg in split_line(stdouted, 1000):
                        embed.add_field(name='stdout', value=f'```py\n{msg}```', inline=False)
                elif stdouted:
                    files.append(File(fp=StringIO(stdout), filename='stdout.py'))
            elif not embed:
                if not files:
                    embed.add_field(name='anything', value='No data', inline=False)
                else:
                    embed.description = 'see files'
            await ctx.reply(embed=embed, files=files)

    @commands.command(aliases=['ext'])
    async def extensions(self, ctx: 'Context'):
        """get extensions name."""
        await ctx.info(
            title='extensions',
            description='\n'.join(sorted([f'`{s}`' for s in self.bot.extensions.keys()]))
        )


def setup(bot: Bot):
    bot.add_cog(Owner(bot))
