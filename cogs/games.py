import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from discord_slash.cog_ext import cog_component

from cmds.uno import uno
from cmds.tic import getComputerMove, create_board

from log import log
l = log()

class Games(commands.Cog, description="Moderation tools for your server!"):
    def __init__(self, bot):
        self.bot = bot
        self.hand1 = 1
        self.hand2 = 2
    
    # commands: uno, tictactoe
    # uno:
    @commands.command(help="Play UNO with a friend!")
    async def uno(self, ctx):
        l.used(ctx)
        u = uno()
        u.deal_cards()
        content = u.show_cards(ctx.author.name, self.hand1)
        embed = discord.Embed(color=discord.Color.orange())
        embed.add_field(name=content[0], value=content[1], inline=False)
        await ctx.send(embed=embed)
    
    @cog_ext.cog_slash(name="uno")
    async def _uno(self, ctx):
        l.used(ctx)
        u = uno()
        u.deal_cards()
        content = u.show_cards(ctx.author.name, self.hand1)
        embed = discord.Embed(color=discord.Color.orange())
        embed.add_field(name=content[0], value=content[1], inline=False)
        await ctx.send(embed=embed, hidden=True)
    
    
    #tic tac toe
    @cog_ext.cog_slash(
        name="tic-tac-toe",
        description="Play Tic-Tac-Toe"
    )
    async def ttt_start(self, ctx: SlashContext):
        l.used(ctx)
        await ctx.send(content=f"{ctx.author.mention}'s Tic-Tac-Toe game!",
                       components=create_board())

    @commands.command(aliases=["ttt"])
    async def tictactoe(self, ctx):
        l.used(ctx)
        await ctx.send(content=f"{ctx.author.mention}'s Tic-Tac-Toe game!",
                       components=create_board())

    def determine_board_state(self, components: list):
        board = []
        for i in range(3):
            row = components[i]["components"]
            for button in row:
                if button["style"] == 2:
                    board.append(' ')
                elif button["style"] == 1:
                    board.append("player")
                elif button["style"] == 4:
                    board.append("enemy")

        return board

    def determine_win_state(self, board: list):
        if board[0] == board[1] == board[2] != ' ':  # row 1
            return board[0]
        if board[3] == board[4] == board[5] != ' ':  # row 2
            return board[3]
        if board[6] == board[7] == board[8] != ' ':  # row 3
            return board[6]
        if board[0] == board[3] == board[6] != ' ':  # col 1
            return board[0]
        if board[1] == board[4] == board[7] != ' ':  # col 2
            return board[1]
        if board[2] == board[5] == board[8] != ' ':  # col 3
            return board[2]
        if board[0] == board[4] == board[8] != ' ':  # diag 1
            return board[0]
        if board[2] == board[4] == board[6] != ' ':  # diag 2
            return board[2]
        return None

    @cog_component(components=create_board())
    async def process_turn(self, ctx: ComponentContext):
        await ctx.defer(edit_origin=True)
        winner_ = None
        try:
            if ctx.author.id != ctx.origin_message.mentions[0].id:
                return
        except:
            return
        button_pos = int(ctx.custom_id.split("||")[-1])
        components = ctx.origin_message.components

        board = self.determine_board_state(components)

        if board[button_pos] == ' ':
            board[button_pos] = "player"
            winner = self.determine_win_state(board)
            if winner:
                winner = ctx.author.mention if winner == "player" else self.bot.user.mention
                winner_ = True

            if not winner:
                if board.count(' ') == 0:
                    winner = "Nobody"
                    winner_ = True
            # ai pos
            move = getComputerMove(board)
            if move != None or winner_ != True:
                board[move] = "enemy"
        else:
            return

        if winner_ == None:
            winner = self.determine_win_state(board)
            if winner:
                winner = ctx.author.mention if winner == "player" else self.bot.user.mention

            if not winner:
                if board.count(' ') == 0:
                    winner = "Nobody"

        # convert the board in buttons
        for i in range(9):
            style = (ButtonStyle.grey
                     if board[i] == ' ' else ButtonStyle.blurple
                     if board[i] == "player" else ButtonStyle.red)
            label = ("X" if board[i] == "player" else "O" if board[i] == "enemy" else " ")
            board[i] = manage_components.create_button(
                style=style,
                label=label,
                custom_id=f"tic_tac_toe_button||{i}",
                disabled=True if winner else False,
            )

        await ctx.edit_origin(
            content=f"{ctx.author.mention}'s Tic-Tac-Toe game!"
            if not winner else f"{winner} has won!",
            components=manage_components.spread_to_rows(*board, max_in_row=3),
        )


def setup(bot):
    bot.add_cog(Games(bot))