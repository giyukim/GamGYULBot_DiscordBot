#-*- coding:utf-8 -*-

import asyncio
import random
import os
import pymysql

import discord
from discord.ext import commands
from discord.utils import get

TOKEN = 'NzE4MDk1ODg5NzYzMjcwNzM4.XtnXfQ.zQxVBYg5H7sASVrHnGFsETbvrGw'
PREFIX = ';'
game = discord.Game("  마법의감귤고둥님 도움말  ")

statcomm = ['도움말', '마법의감귤고둥님']
answer = ['Maybe someday', 'Nothing', 'Neither', 'I don\'t think so', 'Yes', 'Try asking again', 'No', '언젠가는 하겠죠', '가만있어요', '다 안 돼요', '그것도 안 돼요', '좋아요', '다시 한 번 물어봐요', '안 돼요', '언젠가는', '가만히 있어', '둘 다 먹지 마', '그것도 안 돼', '그럼', '다시 한 번 물어봐', '안 돼', '응 몰라', '모른다니까?', '돌아가', '어 안돼 돌아가', '싫어요', '그러게?', 'Zzz...', '싫어요 안돼요 하지마세요', '싫어요', '하자마요', '해요', '하세요', '해', '대답해주기 싫은데요']

bot = commands.Bot(command_prefix = PREFIX)

@bot.event
async def on_ready():
    print('[LOG] logged in as {}'.format(bot.user))
    await bot.change_presence(activity = game)

@bot.event
async def on_message(message):
    msg = message.content.split(' ')
    ctx = message.channel
    
    if message.author == bot.user:
        return

    if msg[0] != '마법의감귤고둥님':
        return

    else: #마법의감귤고둥님
        print('[MSG] {0.channel}; {0.author}:: {0.content}'.format(message))
        if len(msg) == 1:
            await ctx.send(embed = discord.Embed(description = '도움말 :: 마법의감귤고둥님 도움말', color=0xffa600))
        else:
            if msg[1] == '도움말': #마법의감귤고둥님 도움말
                embed = discord.Embed(title=":tangerine: 도움말 :tangerine:", description="마법의 감귤고둥 V1.0R \n개발자: 감귤 \n문의: 감귤#1936 1jgg1020@gmail.com \n접두어: '마법의감귤고둥님 '", color=0xffa600)
                embed.add_field(name="시스템", value="핑", inline=True)
                embed.add_field(name="연결", value="웹페이지, 디스코드", inline=True)
                embed.add_field(name="사용법", value="마법의감귤고둥님 <질문>", inline=False)
                embed.set_footer(text="ⓒ 2020. GamGYUL all rights reserved.")
                await ctx.send(embed=embed)

            elif msg[1] == '핑': #마법의감귤고둥님 핑
                await ctx.send(embed = discord.Embed(description = '퐁!', color=0xffa600))

            elif msg[1] == '웹페이지': #귤아 웹페이지
                await ctx.send(embed = discord.Embed(description = 'https://gamgyul1020.github.io/GGBWebsite/'))
            
            elif msg[1] == '디스코드': #귤아 디스코드
                await ctx.send('https://discord.gg/3PVtrue')

            else:
                que = ''
                for i in range(1, len(msg)):
                    que = que + ' ' + msg[i]
                avle = random.randrange(0, len(answer))
                embed = discord.Embed(title="마법의 감귤고둥", color=0xffa600)
                embed.add_field(name="질문", value=que, inline=False)
                embed.add_field(name="대답", value=answer[avle], inline=False)
                await ctx.send(embed=embed)

bot.run(TOKEN) 