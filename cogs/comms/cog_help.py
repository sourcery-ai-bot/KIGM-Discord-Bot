"""
This file is part of KIGM-Discord-Bot.

KIGM-Discord-Bot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

KIGM-Discord-Bot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with KIGM-Discord-Bot.  If not, see <https://www.gnu.org/licenses/>.
"""

from difflib import get_close_matches
from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from discord.utils import get

from core import KIGMHelp
from the_universe import syntax


class HelpCommands(commands.Cog, name=":bookmark_tabs: Help"):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = KIGMHelp()
        bot.help_command.cog = self
        self.bot = bot

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    # @commands.command(
    #     name="help",
    #     description="Shows this message!",
    #     aliases=["commands", "comms", "command"],
    # )
    # async def help(self, ctx, *, optional_command: Optional[str] = None):

    #     cogs = [c for c in self.bot.cogs.keys()]

    #     SB_COGS = [
    #         "Events",
    #         "Asyncfuncs",
    #         "Tests",
    #         ":desktop: Server Managing",
    #         "SlashCommands",
    #         "TopGG",
    #         "Jishaku",
    #     ]

    #     for hidden_cog in SB_COGS:
    #         cogs.remove(hidden_cog)

    #     if optional_command == None:
    #         HelpList = []

    #         for rl_cog in cogs:
    #             commandList = ""
    #             for command in self.bot.get_cog(rl_cog).walk_commands():
    #                 if command.hidden:
    #                     continue

    #                 elif command.parent != None:
    #                     continue

    #                 commandList += f"\n`{command.name}` - *{command.description}*\n"

    #             else:
    #                 prefix = await self.bot.config.find(ctx.guild.id)
    #                 try:
    #                     prefix = prefix["Bot Prefix"]
    #                 except TypeError:
    #                     prefix = "&"
    #                 helpEmbed = discord.Embed(
    #                     title="All Commands!",
    #                     description=":pushpin: My Prefix in this server is **`{}`**".format(
    #                         prefix
    #                     ),
    #                     color=self.bot.main_color,
    #                 )
    #                 helpEmbed.set_footer(
    #                     text=f"Created by Makiyu#4707 | Page {len(HelpList) + 1} of {len(cogs)}",
    #                     icon_url="https://cdn.discordapp.com/avatars/526616688091987968/fc88ac5bd50ddabe601fb655e2ba72e0.webp?size=32",
    #                 )
    #                 helpEmbed.add_field(name=rl_cog, value=commandList, inline=True)
    #                 HelpList.append(helpEmbed)

    #         else:
    #             await ctx.paginate(HelpList, timeout=50)

    #     else:
    #         if (command := self.bot.get_command(optional_command)) is not None:
    #             if command.cog_name in SB_COGS:
    #                 return await ctx.error("Content after help must be a command.")

    #             await ctx.cmd_help(command)

    #         else:

    #             cmds_list_str = []
    #             nono_cmds = []

    #             for _hidden in SB_COGS:
    #                 for nono_cmd in self.bot.get_cog(_hidden).walk_commands():
    #                     nono_cmds.append(nono_cmd)

    #             for (
    #                 cmd_name
    #             ) in self.bot.commands:  # for converting all the cmds to a str

    #                 if cmd_name in nono_cmds or cmd_name.hidden:
    #                     continue
    #                 else:
    #                     cmds_list_str.append(cmd_name.qualified_name)

    #             matches = get_close_matches(str(optional_command), cmds_list_str)
    #             if len(matches) == 1:
    #                 confirm = await ctx.confirmation(
    #                     msg="**Did you mean** `{}`?".format(matches[0]),
    #                     confirmed_msg="`{}` it is then!".format(matches[0]),
    #                     failed_msg="Oh, well... Good luck finding that command then! :)",
    #                 )
    #                 if confirm:
    #                     await ctx.cmd_help(get(self.bot.commands, name=matches[0]))

    #             elif len(matches) > 1:

    #                 confemb = discord.Embed(
    #                     title="Did you mean...",
    #                     description="\n".join(
    #                         [
    #                             "**({})** {}".format(i + 1, matches[i])
    #                             for i in range(len(matches))
    #                         ]
    #                     ),
    #                     color=self.bot.main_color,
    #                 )
    #                 confemb.set_footer(text="Type the number of what you meant.")

    #                 em = await ctx.send(embed=confemb)

    #                 got_msg = await ctx.input(dr=True, timeout=20.0)
    #                 await em.delete()

    #                 if got_msg in "".join([str(i) for i in range(len(matches) + 1)]):
    #                     try:
    #                         intp = int(got_msg)
    #                     except ValueError:
    #                         await ctx.error(
    #                             "The number that you gave is not applicable."
    #                         )
    #                     else:
    #                         if intp == 0:
    #                             await ctx.error(
    #                                 "The number that you gave is not applicable."
    #                             )
    #                             return

    #                         try:
    #                             await ctx.cmd_help(
    #                                 get(self.bot.commands, name=matches[intp - 1])
    #                             )
    #                         except IndexError:
    #                             await ctx.error(
    #                                 "The number that you gave is not applicable."
    #                             )

    #             else:
    #                 await ctx.error("Content after help must be a valid command.")

    @commands.command(
        description="Suggest something to improve this bot!", aliases=["bot_suggest"]
    )
    @cooldown(1, 21600, BucketType.user)
    async def suggest(self, ctx, *, your_suggestion):

        suggestion_request_received = discord.Embed(
            color=self.bot.main_color,
            title="Thanks for the suggestion! Your suggestion has now been sent to the developers!",
            description="You may find your suggestion in [the official support server](https://discord.gg/jz4WxkB) in the text channel, #suggestions-area!",
        )
        await ctx.send(embed=suggestion_request_received)

        embed = discord.Embed(
            color=0x222222,
            title="New Suggestion for KIGM: ",
            description=your_suggestion,
        )

        embed.set_author(name=f"From {ctx.guild.name}", icon_url=ctx.guild.icon_url)
        embed.set_footer(
            text=f"Suggested by: {ctx.author}", icon_url=ctx.author.avatar_url
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        suggestions_channel = self.bot.get_channel(770633934827683923)
        suggestmsg = await suggestions_channel.send(embed=embed)

        await suggestmsg.add_reaction("💁‍♂️")
        await suggestmsg.add_reaction("🤷‍♀️")
        await suggestmsg.add_reaction("🙅")

    @commands.command(description="Invite this bot to your server!", aliases=["inv"])
    async def invite(self, ctx):
        await ctx.channel.send(
            "<a:weeeee:771309755427061770>**Invite Me**<a:weeeee:771309755427061770>\nhttps://discord.com/api/oauth2/authorize?client_id=763626077292724264&permissions=273115158&scope=bot%20applications.commands"
        )

    @commands.command(
        description="You have a bug to report? Use this command!", aliases=["bugreport"]
    )
    @cooldown(2, 600, BucketType.user)
    async def reportbug(self, ctx, *, bug: str):
        bug_channel = self.bot.get_channel(777684586003431435)

        embed = discord.Embed(
            title=f"Bug Report:", description=bug, color=self.bot.main_color
        )

        embed.set_author(name=f"From {ctx.author}", icon_url=ctx.author.avatar_url)

        await bug_channel.send(embed=embed)

        bug_received = discord.Embed(
            color=self.bot.main_color,
            title="Thanks for the bug-catching! Your bug has now been sent to the developers!",
            description="You may find your bug in [the official support server](https://discord.gg/jz4WxkB) in the text channel, #bug-report!",
        )
        await ctx.send(embed=bug_received)


def setup(bot):
    bot.add_cog(HelpCommands(bot))
