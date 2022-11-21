#-*- coding:utf-8 -*-

import asyncio
import random
import os
import pymysql

import discord
from discord.ext import commands
from discord.utils import get

TOKEN = 'NjgyNTQ1NDA1NDE4MTQzODEz.XxkABg.fWAGJTdfYrgSG-_nvw2FTsxar30'
PREFIX = ';'
game = discord.Game("GamGYULBotV2 :: Debug Activated")

bot = commands.Bot(command_prefix = PREFIX)

@bot.event
async def on_ready():
    print('[SVR] logged in as {}'.format(bot.user))
    await bot.change_presence(activity = game)

@bot.command()
async def ban(ctx, member: discord.Member, *, reason = None):
    if ctx.author.guild_permission.ban_members == True:
        try:
            embed = discord.Embed(title = "Ban Completed")
            

bot.run(TOKEN)