import asyncio
import random
import typing

import discord
import discord_slash.model
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.cog_ext import cog_component
from discord_slash.utils import manage_commands, manage_components
from discord_slash.model import ButtonStyle

guild_ids = [764683397528158259]


def duplicates(lst, item):
    return [i for i, x in enumerate(lst) if x == item]


def create_board():
    """Creates the tic tac toe board"""
    buttons = []
    for i in range(9):
        buttons.append(
            manage_components.create_button(
                style=ButtonStyle.grey,
                label="‎",
                custom_id=f"tic_tac_toe_button||{i}"))
    action_rows = manage_components.spread_to_rows(*buttons, max_in_row=3)
    return action_rows


def checkWin(b, m):
    return ((b[0] == m and b[1] == m and b[2] == m) or  # H top
            (b[3] == m and b[4] == m and b[5] == m) or  # H mid
            (b[6] == m and b[7] == m and b[8] == m) or  # H bot
            (b[0] == m and b[3] == m and b[6] == m) or  # V left
            (b[1] == m and b[4] == m and b[7] == m) or  # V centre
            (b[2] == m and b[5] == m and b[8] == m) or  # V right
            (b[0] == m and b[4] == m and b[8] == m) or  # LR diag
            (b[2] == m and b[4] == m and b[6] == m))  # RL diag


def checkDraw(b):
    return ' ' not in b


def getBoardCopy(b):
    # Make a duplicate of the board. When testing moves we don't want to
    # change the actual board
    dupeBoard = []
    for j in b:
        dupeBoard.append(j)
    return dupeBoard


def testWinMove(b, mark, i):
    # b = the board
    # mark = 0 or X
    # i = the square to check if makes a win
    bCopy = getBoardCopy(b)
    bCopy[i] = mark
    return checkWin(bCopy, mark)


def testForkMove(b, mark, i):
    # Determines if a move opens up a fork
    bCopy = getBoardCopy(b)
    bCopy[i] = mark
    winningMoves = 0
    for j in range(0, 9):
        if testWinMove(bCopy, mark, j) and bCopy[j] == ' ':
            winningMoves += 1
    return winningMoves >= 2


def getComputerMove(b):
    # Check computer win moves
    for i in range(0, 9):
        if b[i] == ' ' and testWinMove(b, 'enemy', i):
            return i
    # Check player win moves
    for i in range(0, 9):
        if b[i] == ' ' and testWinMove(b, 'player', i):
            return i
    # Check computer fork opportunities
    for i in range(0, 9):
        if b[i] == ' ' and testForkMove(b, 'X', i):
            return i
    # Check player fork opportunities, incl. two forks
    playerForks = 0
    for i in range(0, 9):
        if b[i] == ' ' and testForkMove(b, '0', i):
            playerForks += 1
            tempMove = i
    if playerForks == 1:
        return tempMove
    elif playerForks == 2:
        for j in [1, 3, 5, 7]:
            if b[j] == ' ':
                return j
    # Play center
    if b[4] == ' ':
        return 4
    # Play side for special case
    norm = b[0] == "player" and b[4] == "enemy" and b[8] == "player" and len(duplicates(b, ' ')) == 6 or b[6] == "player" and b[4] == "enemy" and b[2] == "player" and len(duplicates(b, ' ')) == 6
    if norm:
        for i in [1, 3, 5, 7]:
            if b[i] == ' ':
                return i
    # Play a corner
    for i in [0, 2, 6, 8]:
        if b[i] == ' ':
            return i
    #Play a side
    for i in [1, 3, 5, 7]:
        if b[i] == ' ':
            return i