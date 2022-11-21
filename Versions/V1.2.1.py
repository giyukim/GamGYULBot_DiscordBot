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
game = discord.Game("귤아 도움말")
statcomm = ['핑', '도움말', '청소', '김태균', '감귤', '귤', '귤아', '배워', '[질문]', '데이터베이스', '금지', '웹페이지', '디스코드', '주사위', '골라줘', '찾아', '온라인', '마법의감귤고둥님', '마법의감귤고동님']
mgc_answer = ['Maybe someday', 'Nothing', 'Neither', 'I don\'t think so', 'Yes', 'Try asking again', 'No', '언젠가는 하겠죠', '가만있어요', '다 안 돼요', '그것도 안 돼요', '좋아요', '다시 한 번 물어봐요', '안 돼요', '언젠가는', '가만히 있어', '둘 다 먹지 마', '그것도 안 돼', '그럼', '다시 한 번 물어봐', '안 돼', '응 몰라', '모른다니까?', '돌아가', '어 안돼 돌아가', '싫어요', '그러게?', 'Zzz...', '싫어요 안돼요 하지마세요', '싫어요', '하지마요', '해요', '하세요', '해', '대답해주기 싫은데요']

bot = commands.Bot(command_prefix = PREFIX) 

@bot.event
async def on_ready():
    print('[SVR] logged in as {}'.format(bot.user))
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

    def sql_search(que):
        print('[LOG] Call Function sql_search({})'.format(que))
        sql = "SELECT EXISTS (SELECT ans FROM comm2 WHERE que=\"" + que + "\")"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result == ((1,),):
            sql = "SELECT ans FROM comm2 WHERE que = \"" + que + "\""
            cursor.execute(sql)
            resultrt = cursor.fetchall()
            return str(resultrt[0][0]).split('[|&-&|]')
        else:
            return '0'

    def sql_insert(que, ans, une):
        print('[LOG] Call Function sql_insert({}, {}, {})'.format(que, ans, une))
        sql = "SELECT EXISTS (SELECT ans FROM comm2 WHERE que=\"" + que + "\")"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result == ((0,),):
            sql = "INSERT INTO comm2(que, ans, une) VALUES('" + str(que) + "', '" + str(ans) + "', '" + str(une) + "')"
            cursor.execute(sql)
            db.commit()
            return '질문을 배웠어요'
        else:
            sql = "SELECT ans FROM comm2 WHERE que=\"" + que + "\""
            cursor.execute(sql)
            resultp = cursor.fetchall()
            resultp = resultp[0][0]
            sql = "SELECT id FROM comm2 WHERE que=\"" + que + "\""
            cursor.execute(sql)
            resultrt = cursor.fetchall()
            resultrt = resultrt[0][0]
            sql = "UPDATE comm2 SET ans=\'" + str(resultp) + "[|&-&|]" + str(ans) + "\' WHERE id=\'" + str(resultrt) + "\'"
            cursor.execute(sql)
            db.commit()
            return '질문에 대답을 추가하였어요'

    def sql_print(que):
        print('[LOG] Call Function sql_print({})'.format(que))
        sql = "SELECT EXISTS (SELECT ans FROM comm2 WHERE que=\"" + que + "\")"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result == ((1,),):
            sql = "SELECT ans FROM comm2 WHERE que = \"" + que + "\""
            cursor.execute(sql)
            resultrt = cursor.fetchall()
            rstrt = str(resultrt[0][0]).split('[|&-&|]')
            rdvalue = random.randrange(0, len(rstrt))
            return rstrt[rdvalue]
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
            await ctx.send(embed = discord.Embed(description = answer[answer_value], color=0xffa600))

        else:
            if msg[1] == '도움말': #귤아 도움말
                embed = discord.Embed(title=":tangerine: 도움말 :tangerine:", description="감귤봇 V1.2.1 \n개발자: 감귤 \n문의: 감귤#1936 1jgg1020@gmail.com \n접두어: '귤아 '", color=0xffa600)
                embed.add_field(name="시스템", value="핑, 감귤", inline=True)
                embed.add_field(name="연결", value="웹페이지, 디스코드", inline=True)
                embed.add_field(name="개발자 전용", value="데이터베이스, 금지", inline=True)
                embed.add_field(name="채팅", value="청소", inline=True)
                embed.add_field(name="명령어", value="골라줘, 주사위", inline=True)
                embed.add_field(name="대화", value="배워, 찾아, [질문], 마법의감귤고둥", inline=True)
                embed.add_field(name="[질문] 사용법", value="귤아 [질문] \n[질문]에 단어를 입력하세요", inline=False)
                embed.set_footer(text="ⓒ 2020. GamGYUL all rights reserved.")
                await ctx.send(embed=embed)

            elif msg[1] == '핑': #귤아 핑
                await ctx.send(embed = discord.Embed(description = '퐁!', color=0xffa600))

            elif msg[1] == '청소': #귤아 청소
                if len(msg) != 3:
                    await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 청소 <integer>', color=0xffa600))
                else:
                    await ctx.purge(limit = int(msg[2]))
                    await ctx.send(embed = discord.Embed(description = '채널에서 {0}개의 메세지를 청소했어요'.format(msg[2]), color=0xffa600))

            elif msg[1] == '감귤': #귤아 감귤
                answer = ['감귤 좋아 (*ฅ́˘ฅ̀*)♡', '좋아!~ ( ்́ꇴ ்̀)♡', '맛있어!', '히힣 (*ˊૢᵕˋૢ*)ෆ', '마시쪙~!', '먹지마요!ヽ(*´□`)ﾉﾞ', '왜용( •᷄ὤ•᷅)?', '뭐야 왜 불러 (≖ᴗ≖  )', 'ꉂꉂ(ᵔᗜᵔ*) 푸하항']
                answer_value = random.randrange(0, len(answer))
                await ctx.send(embed = discord.Embed(description = answer[answer_value], color=0xffa600))
            
            elif msg[1] == '웹페이지': #귤아 웹페이지
                await ctx.send(embed = discord.Embed(description = 'https://gamgyul1020.github.io/GGBWebsite/'))
            
            elif msg[1] == '디스코드': #귤아 디스코드
                await ctx.send('https://discord.gg/3PVtrue')

            elif msg[1] == '김태균': #귤아 김태균
                answer = ['ㅄ', '우웩', '김태균 = 딸태균', '균사체', '소독해 버려!@']
                answer_value = random.randrange(0, len(answer))
                await ctx.send(embed = discord.Embed(description = answer[answer_value], color=0xffa600))

            elif msg[1] == '골라줘': #귤아 골라줘
                if len(msg) == 2:
                    await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 골라줘 <리스트1> <리스트2> ... <리스트n>', color=0xffa600))
                else:
                    answer_value = random.randrange(2, len(msg))
                    await ctx.send(embed = discord.Embed(description = msg[answer_value], color=0xffa600))

            elif msg[1] == '주사위': #귤아 주사위
                if len(msg) == 4:
                    if int(msg[2]) < int(msg[3]):
                        answer_value = random.randrange(int(msg[2]), int(msg[3]) + 1)
                        await ctx.send(embed = discord.Embed(description = '주사위[{} ~ {}] :: {}'.format(msg[2], msg[3], str(answer_value)), color=0xffa600))
                    elif int(msg[2]) > int(msg[3]):
                        answer_value = random.randrange(int(msg[3]), int(msg[2]) + 1)
                        await ctx.send(embed = discord.Embed(description = '주사위[{} ~ {}] :: {}'.format(msg[3], msg[2], str(answer_value)), color=0xffa600))
                    elif int(msg[2]) == int(msg[3]):
                        await ctx.send(embed = discord.Embed(description = '주사위[{}] :: {}'.format(msg[2], msg[2]), color=0xffa600))
                else:
                    await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 주사위 <정수> <정수>', color=0xffa600))

            elif msg[1] == '데이터베이스': #귤아 데이터베이스
                if str(message.author) == "감귤#1936":
                    if len(msg) == 2:
                        await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 데이터베이스 [수정/삭제]', color=0xffa600))
                    else:
                        if msg[2] == '수정': #귤아 데이터베이스 수정
                            if len(msg) >= 5:
                                if msg[3] in statcomm:
                                    await ctx.send(embed = discord.Embed(description = '지정된 명령어는 수정할 수 없어요', color=0xffa600))
                                else:
                                    ans2 = ''
                                    for i in range(4, len(msg)):
                                        ans2 = ans2 + ' ' + msg[i]
                                    result = sql_edit(msg[3], ans2)
                                    await ctx.send(embed = discord.Embed(description = result, color=0xffa600))
                            else:
                                await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 데이터베이스 수정 <질문> <대답>', color=0xffa600))
                        elif msg[2] == '삭제': #귤아 데이터베이스 삭제
                            if len(msg) == 4:
                                if msg[3] in statcomm:
                                    await ctx.send(embed = discord.Embed(description = '지정된 명령어는 삭제할 수 없어요', color=0xffa600))
                                else:
                                    result = sql_delete(msg[3])
                                    await ctx.send(embed = discord.Embed(description = result, color=0xffa600))
                            else:
                                await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 데이터베이스 삭제 <질문> <대답>', color=0xffa600))
                else:
                    await ctx.send(embed = discord.Embed(description = '이 명령어는 개발자만 사용할 수 있는 명령어에요', color=0xffa600))
            
            elif msg[1] == '금지': #귤아 금지
                if str(message.author) == '감귤#1936':
                    if len(msg) == 4:
                        if msg[2] == '추가':
                            result = sql_insert_ban(msg[3])
                            await ctx.send(embed = discord.Embed(description = result, color=0xffa600))
                        elif msg[2] == '삭제':
                            result = sql_delete_ban(msg[3])
                            await ctx.send(embed = discord.Embed(description = result, color=0xffa600))
                    else:
                        await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 금지 [추가/삭제] <질문>', color=0xffa600))
                else:
                    await ctx.send(embed = discord.Embed(description = '이 명령어는 개발자만 사용할 수 있는 명령어에요', color=0xffa600))

            elif msg[1] == '찾아': #귤아 찾아
                if len(msg) == 3:
                    if msg[2] in statcomm:
                        await ctx.send(embed = discord.Embed(description = '지정된 명령어는 찾기 기능을 사용할 수 없어요', color=0xffa600))
                    else:
                        result = sql_search(msg[2])
                        if result == '0':
                            await ctx.send(embed = discord.Embed(description = "질문을 찾을 찾을 수 없어요", color=0xffa600))
                        else:
                            embed = discord.Embed(title="질문 찾기", color=0xffa600)
                            embed.add_field(name="질문", value=msg[2], inline=False)
                            asw = ''
                            for i in range(0, len(result)):
                                asw = asw + str(i + 1) + ". " + result[i] + "\n"
                            embed.add_field(name="대답", value=asw, inline=False)
                            await ctx.send(embed=embed)
                else:
                    await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 찾아 <질문> \n질문은 단어만 가능합니다', color=0xffa600))

            elif msg[1] == '배워': #귤아 배워
                if len(msg) < 4:
                    await ctx.send(embed = discord.Embed(description = '도움말:: 귤아 배워 <질문> <대답> \n질문은 단어만 가능합니다\n대답은 문장으로 가능합니다', color=0xffa600))
                else:
                    if msg[2] in statcomm:
                        await ctx.send(embed = discord.Embed(description = '지정된 명령어는 배울 수 없어요', color=0xffa600))
                    else:
                        isban = sql_search_ban(msg[2])
                        if isban == '1':
                            await ctx.send(embed = discord.Embed(description = '금지된 질문은 배울 수 없어요', color=0xffa600))
                        else:
                            ans2 = ''
                            for i in range(3, len(msg)):
                                ans2 = ans2 + ' ' + msg[i]
                            result = sql_insert(msg[2], ans2, message.author)
                            await ctx.send(embed = discord.Embed(description = result, color=0xffa600))

            elif msg[1] == '마법의감귤고둥' or msg[1] == '마법의감귤고동':
                embed = discord.Embed(title="마법의 감귤고둥", color=0xffa600)
                embed.add_field(name="도움말", value='마법의감귤고둥님 <질문>', inline=False)
                await ctx.send(embed = embed)
            
            else: #귤아 <ELSE>
                isban = sql_search_ban(msg[1])
                if isban == '1':
                    await ctx.send(embed = discord.Embed(description = '금지된 질문이에요', color=0xffa600))
                else:
                    result = sql_print(msg[1])
                    await ctx.send(embed = discord.Embed(description = result, color=0xffa600))

            db.close()

    elif msg[0] == '마법의감귤고둥님' or msg[0] == '마법의감귤고동님':
        print('[MGC] {0.channel}; {0.author}:: {0.content}'.format(message))
        if len(msg) == 1:
            await ctx.send(embed = discord.Embed(description = '도움말 :: 귤아 마법의감귤고둥', color=0xffa600))
        else:
            mgc_que = ''
            for i in range(1, len(msg)):
                mgc_que = mgc_que + ' ' + msg[i]
            avle = random.randrange(0, len(mgc_answer))
            embed = discord.Embed(title="마법의 감귤고둥", color=0xffa600)
            embed.add_field(name="질문", value=mgc_que, inline=False)
            embed.add_field(name="대답", value=mgc_answer[avle], inline=False)
            await ctx.send(embed = embed)


bot.run(TOKEN)
