#-*- coding:utf-8 -*-

import asyncio
import random
import os
import pymysql

import discord
from discord.ext import commands
from discord.utils import get

TOKEN = 'NjgyNTQ1NDA1NDE4MTQzODEz.Xos_4Q.MODQBcxpngLjS0Mh5iVbmPQmnYY'
PREFIX = ';'
game = discord.Game("  귤아 도움말  ")

statcomm = ['핑', '도움말', '청소', '김태균', '감귤', '귤', '귤아', '배워', '[질문]', '데이터베이스', '금지', '웹페이지', '디스코드']

bot = commands.Bot(command_prefix = PREFIX) 

@bot.event
async def on_ready():
    print('[LOG] logged in as {}'.format(bot.user))
    await bot.change_presence(activity = game)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.split(' ')
    ctx = message.channel

    db = pymysql.connect(
        user='root',
        passwd='jejugamgyul',
        host='localhost',
        db='bot1_command',
        charset='utf8mb4'
    )
    cursor = db.cursor()

    def sql_insert(que, ans, une):
        print('[LOG] Call Function sql_insert({}, {}, {})'.format(que, ans, une))
        sql = "SELECT EXISTS (SELECT ans FROM comm2 WHERE que=\"" + que + "\")"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result == ((1,),):
            return '이미 있는 질문이에요'
        else:
            sql = "INSERT INTO comm2(que, ans, une) VALUES('" + str(que) + "', '" + str(ans) + "', '" + str(une) + "')"
            cursor.execute(sql)
            db.commit()
            return '질문을 배웠어요'

    def sql_search(que):
        print('[LOG] Call Function sql_search({})'.format(que))
        sql = "SELECT EXISTS (SELECT ans FROM comm2 WHERE que=\"" + que + "\")"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result == ((1,),):
            sql = "SELECT ans FROM comm2 WHERE que = \"" + que + "\""
            cursor.execute(sql)
            resultrt = cursor.fetchall()
            return resultrt[0][0]
        else:
            return '없는 질문이에요'
    
    def sql_delete(que):
        print('[LOG] Call Function sql_delete({})'.format(que))
        sql = "SELECT EXISTS (SELECT id FROM comm2 WHERE que=\"" + que + "\")"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result == ((1,),):
            sql = "SELECT id FROM comm2 WHERE que=\"" + que + "\""
            cursor.execute(sql)
            resultrt = cursor.fetchall()
            resultrt = resultrt[0][0]
            sql = "DELETE FROM comm2 WHERE id=\'" + str(resultrt) + "\'"
            cursor.execute(sql)
            db.commit()
            return '데이터를 삭제했어요'
        else:
            return '삭제할 데이터가 없어요'

    def sql_edit(que, ans):
        print('[LOG] Call Function sql_edit({}, {})'.format(que, ans))
        sql = "SELECT EXISTS (SELECT id FROM comm2 WHERE que=\"" + que + "\")"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result == ((1,),):
            sql = "SELECT id FROM comm2 WHERE que=\"" + que + "\""
            cursor.execute(sql)
            resultrt = cursor.fetchall()
            resultrt = resultrt[0][0]
            sql = "UPDATE comm2 SET ans=\'" + str(ans) + "\', une=\'SYSTEM\' WHERE id=\'" + str(resultrt) + "\'"
            cursor.execute(sql)
            db.commit()
            return '데이터를 수정했어요'
        else:
            return '수정할 데이터가 없어요'

    def sql_insert_ban(comm):
        print('[LOG] Call Function sql_insert_ban({})'.format(comm))
        sql = "SELECT EXISTS (SELECT id FROM comm_ban WHERE command=\"" + comm + "\")"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result == ((1,),):
            return '이미 리스트에 등록 되었어요'
        else:
            sql = "INSERT INTO comm_ban(command) VALUES('" + comm + "')"
            cursor.execute(sql)
            db.commit()
            return '리스트에 등록하였어요'

    def sql_search_ban(comm):
        print('[LOG] Call Function sql_search_ban({})'.format(comm))
        sql = "SELECT EXISTS (SELECT id FROM comm_ban WHERE command=\"" + comm + "\")"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result == ((1,),):
            return '1'
        else:
            return '0'
    
    def sql_delete_ban(comm):
        print('[LOG] Call Function sql_delete_ban({})'.format(comm))
        sql = "SELECT EXISTS (SELECT id FROM comm_ban WHERE command=\"" + comm + "\")"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result == ((1,),):
            sql = "SELECT id FROM comm_ban WHERE command=\"" + comm + "\""
            cursor.execute(sql)
            resultrt = cursor.fetchall()
            resultrt = resultrt[0][0]
            sql = "DELETE FROM comm_ban WHERE id=\'" + str(resultrt) + "\'"
            cursor.execute(sql)
            db.commit()
            return '리스트에서 데이터를 삭제했어요'
        else:
            return '삭제할 데이터가 없어요'

    if msg[0] == '귤아':
        print('[MSG] {0.channel}; {0.author}:: {0.content}'.format(message))

        if len(msg) == 1: #귤아
            answer = ['네?', '넹?!', '저 부르셨나요?', '네 주인님']
            answer_value = random.randrange(0, len(answer))
            await ctx.send(embed = discord.Embed(description = answer[answer_value]))

        else:
            if msg[1] == '도움말': #귤아 도움말
                embed = discord.Embed(title=":tangerine: 도움말 :tangerine:", description="감귤봇 V1.0.3 \n개발자: 감귤 \n문의: 감귤#1936 1jgg1020@gmail.com \n접두어: '귤아 '", color=0xffa600)
                embed.add_field(name="System", value="핑, 감귤, 데이터베이스, 금지", inline=False)
                embed.add_field(name="Connect", value="웹페이지, 디스코드", inline=False)
                embed.add_field(name="Control", value="청소", inline=False)
                embed.add_field(name="Custom", value="배워, [질문], 골라줘", inline=False)
                embed.add_field(name="[질문] 사용법", value="귤아 [질문] \n[질문]에 단어를 입력하세요", inline=False)
                await ctx.send(embed=embed)

            elif msg[1] == '핑': #귤아 핑
                await ctx.send(embed = discord.Embed(description = '퐁!'))

            elif msg[1] == '청소': #귤아 청소
                if len(msg) != 3:
                    await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 청소 <integer>'))
                else:
                    await ctx.purge(limit = int(msg[2]))
                    await ctx.send(embed = discord.Embed(description = '채널에서 {0}개의 메세지를 청소했어요'.format(msg[2])))

            elif msg[1] == '감귤': #귤아 감귤
                answer = ['감귤 좋아 (*ฅ́˘ฅ̀*)♡', '좋아!~ ( ்́ꇴ ்̀)♡', '맛있어!', '히힣 (*ˊૢᵕˋૢ*)ෆ', '마시쪙~!']
                answer_value = random.randrange(0, len(answer))
                await ctx.send(embed = discord.Embed(description = answer[answer_value]))
            
            elif msg[1] == '웹페이지': #귤아 웹페이지
                await ctx.send(embed = discord.Embed(description = 'https://gamgyul1020.github.io/GGBWebsite/'))
            
            elif msg[1] == '디스코드': #귤아 디스코드
                await ctx.send('https://discord.gg/3PVtrue')

            elif msg[1] == '김태균': #귤아 김태균
                answer = ['ㅄ', '우웩', '김태균 = 딸태균', '균사체', '소독해 버려!@']
                answer_value = random.randrange(0, len(answer))
                await ctx.send(embed = discord.Embed(description = answer[answer_value]))

            elif msg[1] == '골라':
                if len(msg) == 2:
                    await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 골라줘 [범위/리스트]'))
                else:
                    if msg[2] == '범위':
                        if len(msg) == 5:
                            answer_value = random.randrange(int(msg[3]), int(msg[4]) + 1)
                            await ctx.send(embed = discord.Embed(description = answer_value))
                        else:
                            await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 골라 범위 [시작(정수)] [끝(정수)]'))
                    elif msg[2] == '리스트':
                        if len(msg) == 3:
                            await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 골라 리스트 [리스트1] [리스트2] ... [리스트n]'))
                        else:
                            answer_value = random.randrange(3, len(msg))
                            await ctx.send(embed = discord.Embed(description = msg[answer_value]))

            elif msg[1] == '데이터베이스': #귤아 데이터베이스
                if str(message.author) == "감귤#1936":
                    if len(msg) == 2:
                        await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 데이터베이스 [수정/삭제]'))
                    else:
                        if msg[2] == '수정': #귤아 데이터베이스 수정
                            if len(msg) >= 5:
                                if msg[3] in statcomm:
                                    await ctx.send(embed = discord.Embed(description = '지정된 명령어는 수정할 수 없어요'))
                                else:
                                    ans2 = ''
                                    for i in range(4, len(msg)):
                                        ans2 = ans2 + ' ' + msg[i]
                                    result = sql_edit(msg[3], ans2)
                                    await ctx.send(embed = discord.Embed(description = result))
                            else:
                                await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 데이터베이스 수정 <질문> <대답>'))

                        elif msg[2] == '삭제': #귤아 데이터베이스 삭제
                            if len(msg) == 4:
                                if msg[3] in statcomm:
                                    await ctx.send(embed = discord.Embed(description = '지정된 명령어는 삭제할 수 없어요'))
                                else:
                                    result = sql_delete(msg[3])
                                    await ctx.send(embed = discord.Embed(description = result))
                            else:
                                await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 데이터베이스 삭제 <질문> <대답>'))
                else:
                    await ctx.send(embed = discord.Embed(description = '이 명령어는 개발자만 사용할 수 있는 명령어에요'))
            
            elif msg[1] == '금지':
                if str(message.author) == '감귤#1936':
                    if len(msg) == 4:
                        if msg[2] == '추가':
                            result = sql_insert_ban(msg[3])
                            await ctx.send(embed = discord.Embed(description = result))

                        elif msg[2] == '삭제':
                            result = sql_delete_ban(msg[3])
                            await ctx.send(embed = discord.Embed(description = result))
                    else:
                        await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 금지 [추가/삭제] <질문>'))
                else:
                    await ctx.send(embed = discord.Embed(description = '이 명령어는 개발자만 사용할 수 있는 명령어에요'))

            elif msg[1] == '배워': #귤아 배워
                if len(msg) < 4:
                    await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 배워 <질문> <대답> \n질문은 단어만 가능합니다\n대답은 문장으로 가능합니다'))
                else:
                    if msg[2] in statcomm:
                        await ctx.send(embed = discord.Embed(description = '지정된 명령어는 배울 수 없어요'))
                    else:
                        isban = sql_search_ban(msg[2])
                        if isban == '1':
                            await ctx.send(embed = discord.Embed(description = '금지된 질문은 배울 수 없어요'))
                        else:
                            ans2 = ''
                            for i in range(3, len(msg)):
                                ans2 = ans2 + ' ' + msg[i]
                            result = sql_insert(msg[2], ans2, message.author)
                            await ctx.send(embed = discord.Embed(description = result))
            
            else: #귤아 <ELSE>
                isban = sql_search_ban(msg[1])
                if isban == '1':
                    await ctx.send(embed = discord.Embed(description = '금지된 질문이에요'))
                else:
                    result = sql_search(msg[1])
                    await ctx.send(embed = discord.Embed(description = result))
            
            db.close()

bot.run(TOKEN)
