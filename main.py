import discord
from discord.ext import commands
from discord.utils import get

import random
import typing
import datetime
import logging
import requests
import googletrans

# import pymysql
import sqlite3

BOT_PREFIX:str = ";"
BOT_STATUS = discord.Game("GamGYULBotV2 For Days DEV")

LOG_FILE_DIR:str = "./logs/GFD_DEV.log"

DATABASE_FILE_DIR:str = "./sqlite3/DEV.db"

ERROR_CODE_DETAIL:dict = {
    "ERR_UNKNOWN":"알 수 없는 오류가 발생하였습니다",
    "ERR_VALUEERROR_INTEGER":"정수형 인자가 필요합니다",
    "ERR_PERMISSION_AUTHOR":"사용자의 권한이 없습니다",
    "ERR_PERMISSION_BOT":"봇에 권한이 없습니다",
    "ERR_CLIENT_NOTSERVER":"서버에서만 이용가능한 명령어 입니다",
    "ERR_COMMAND_NOTFOUND":"해당 커맨드가 없습니다",
    "ERR_COMMAND_SUBCOMMERR":"서브 커맨드에 오류가 있습니다\n도움말을 참고하세요",
    "ERR_API_SEOUL":"서울시OpenAPI API요청에 문제가 발생하였습니다",
    "ERR_RFMG_USERHASNOITEM":"강화 :: 해당 아이템을 소유하고 있지 않습니다",
    "ERR_RFMG_USERHASITEM":"강화 :: 이미 해당 아이템을 소유하고 있습니다",
    "ERR_RFMG_NOITEMSINTABLE":"강화 :: 생성된 아이템이 없습니다",
}

HELP_COMMAND:dict = {
    "시스템": ["도움말", "핑"],
    "채팅": ["청소", "안녕", "번역"],
    "게임": ["강화"],
    "도움말": [";도움말 [명령어]"],
}

HELP_COMMAND_DETAIL:dict = {
    "도움말":{
        "description":"도움말을 확인합니다",
        "gram_command":";도움말 [명령어] \n;help [명령어]",
        "sub_commands":{
            "[명령어]":"자세한 명령어의 도움말을 보고 싶다면 명령어를 입력해주세요 (선택)"
        }
    },
    "핑":{
        "description":"봇의 상태를 확인합니다",
        "gram_command":";핑"
    },
    "청소":{
        "description":"채팅방을 청소합니다",
        "gram_command":";청소 <개수> [유저]",
        "sub_commands":{
            "<개수>":"청소할 메세지 개수 (필수)",
            "[유저]":"청소할 메세지의 작성자 (선택)"
        }
    },
    "강화":{
        "description":"아이템 강화 게임 관련 명령어입니다",
        "gram_command":"---------------------------------------------------",
        "sub_commands":{
            ";강화 <아이템이름>":"아이템을 강화합니다",
            ";강화 <아이템이름> 생성":"아이템을 생성합니다",
            ";강화 <아이템이름> 삭제":"아이템을 삭제합니다",
            ";강화 <아이템이름> 정보":"해당 아이템의 정보를 불러옵니다",
            ";강화 리스트":"개인이 보유하고 있는 아이템의 리스트를 불러옵니다",
            ";강화 순위":"강화 순위를 볼 수 있습니다",
            ";강화 요약":"강화 아이템의 요약을 볼 수 있습니다"
        },
        "sub_commands_inline":False
    },
    "안녕":{
        "description":"랜덤으로 인사합니다",
        "gram_command":";안녕 \n;hi \n;hello"
    },
    "번역":{
        "description":"다른 언어를 영어 또는 한국어로 번역합니다.\n Translate other languages to English or Korean.",
        "gram_command":";번역 <언어/Language> <문장/Sentence> \n;번역기 <언어/Language> <문장/Sentence> \n;translator <언어/Language> <문장/Sentence> \n;translate <언어/Language> <문장/Sentence> \n;trans <언어/Language> <문장/Sentence>",
        "sub_commands":{
            "<언어/Language>":"영어(English) : 영어, English, english, Eng, eng, en, US, us\n한국어(Korean) : 한국어, 한국, 한글, Korea, korea, Korean, korean, kor, ko, KO\n위 목록 중 하나를 선택하여 입력해 주세요.\nEnter one from the list above.",
            "<문장/Sentence>":"번역할 문장을 입력해 주세요. \nEnter the text to be translated."
        },
        "sub_commands_inline":False
    }
}

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename = LOG_FILE_DIR, encoding = "utf-8", mode = 'w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = BOT_PREFIX, Intents = intents)

def log_con(message:typing.Optional[str] = None) -> None:
    print("[LOG] {} ({})".format(message, (datetime.datetime.now()).strftime("%Y%m%d%H%M%S%f")))

def sqlite3_select(table_name:str, file_dir:str = DATABASE_FILE_DIR, col:typing.Union[list, str] = '*', condition:typing.Optional[str] = None):
    conn = sqlite3.connect(file_dir)
    cur = conn.cursor()
    sql = "SELECT "
    if str(type(col)) == "<class \'str\'>":
        sql = sql + str(col) + ' '
    else:
        for col_sel in col:
            sql = sql + str(col_sel) + ' '
    sql += "FROM {}".format(str(table_name))
    if not condition == None:
        sql += " WHERE {}".format(str(condition))
    sql += ';'
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    return data

def sqlite3_exist(table_name:str, file_dir:str = DATABASE_FILE_DIR, col:typing.Union[list, str] = '*', condition:typing.Optional[str] = None) -> bool:
    conn = sqlite3.connect(file_dir)
    cur = conn.cursor()
    sql = "SELECT EXISTS (SELECT "
    if str(type(col)) == "<class \'str\'>":
        sql = sql + str(col) + ' '
    else:
        for col_sel in col:
            sql = sql + str(col_sel) + ' '
    sql += "FROM {}".format(str(table_name))
    if type(condition) == "<class \'str\'>":
        sql += " WHERE {}".format(str(condition))
    sql += ');'
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    if data[0][0] == 1:
        return True
    else:
        return False

def sqlite3_insert(table_name:str, data:dict, file_dir:str = DATABASE_FILE_DIR) -> None:
    '''
        data = {
            field_name[string] : field_data[string|integer],
        }
    '''
    conn = sqlite3.connect(file_dir)
    cur = conn.cursor()
    sql = f"INSERT INTO {table_name}"
    field_str = data.keys()[0]
    value_str = data[data.keys()[0]]
    for field in data.keys()[1:]:
        field_str += f", {field}"
        value_str += f", {data[field]}"
    sql = f"{sql} ({field_str}) VALUES ({value_str});"
    cur.execute(sql)
    conn.commit()
    conn.close()

def sqlite3_update(table_name:str, field:str, value, file_dir:str = DATABASE_FILE_DIR) -> None:
    conn = sqlite3.connect(file_dir)
    cur = conn.cursor()
    sql = f"UPDATE {table_name} SET {field} = "
    if type(value) == "<class \'str\'>":
        sql += f"\'{value}\';"
    else:
        sql += f"{value};"
    cur.execute(sql)
    conn.commit()
    conn.close()

def sqlite3_delete(table_name:str, condition:typing.Optional[str] = None, file_dir:str = DATABASE_FILE_DIR) -> None:
    conn = sqlite3.connect(file_dir)
    cur = conn.cursor()
    sql = f"DELETE FROM {table_name}"
    if type(condition) == "<class \'str\'>":
        sql = f"{sql} WHERE {condition};"
    else:
        sql += ";"
    cur.execute(sql)
    conn.commit()
    conn.close()
    
def embedgen(title:typing.Optional[str] = None, title_desc:typing.Optional[str] = None, fields:typing.Optional[dict] = None, footer:bool = True, error:bool = False) -> list:
    '''
        title: Embed Title [string|None]
        title_desc: Embed Title Description [string|None]
        fields: Embed Fields List [Dictionary|None]
            {
                "Field1"[string]: {"value":"Lorem Ipsum"[string], "inline":True|False[boolean|None]}, 
            } 
        footer: footer Copyright Message [boolean|None]
        error: Whether it's an error embed or not. [boolean|None]
    '''
    if title == None:
        title = ''
    else:
        title = ":tangerine:  {}".format(title)
    if title_desc == None:
        title_desc = ''
    embed_color = 0xffa200
    if error == True:
        embed_color = 0xff0000
    embed = discord.Embed(title = title, description = title_desc, color = embed_color)
    if not fields == None:
        for key in list(fields.keys()):
            temp_field_value:str = ""
            temp_field_inline:bool = False
            if "value" in fields[key].keys():
                temp_field_value = fields[key]["value"]
            if "inline" in fields[key].keys():
                temp_field_inline = fields[key]["inline"]
            embed.add_field(name = key, value = temp_field_value, inline = temp_field_inline)
    if footer == True:
        embed.set_footer(text = "ⓒ 2021. JGamGYUL")
    return embed

def get_error_msg(error_code:str = "ERR_UNKNOWN") -> dict:
    error_field = {
        "내용": {"value":ERROR_CODE_DETAIL[error_code]}, 
        "오류 코드": {"value":error_code}
    }
    return error_field

BOT_VERSION:str = str(sqlite3_select(table_name = "information", col = "value", condition = "field = \"bot_version\"")[0][0])
BOT_TOKEN:str = str(sqlite3_select(table_name = "information", col = "value", condition = "field = \"bot_token\"")[0][0])

@bot.event
async def on_ready():
    log_con("Bot Activated Version:{}".format(BOT_VERSION))
    await bot.change_presence(activity = BOT_STATUS)

@bot.command(name = "help", aliases = ["도움말"])
async def _help(ctx):
    msg = ctx.message.content.split(' ')
    if len(msg) == 1:
        field_dict = {}
        for field_name in HELP_COMMAND.keys():
            field = HELP_COMMAND[field_name][0]
            for field_desc in HELP_COMMAND[field_name][1:]:
                field = field + ", " + field_desc
            field_ = {
                "value":field,
                "inline":False
            }
            field_dict[field_name] = field_
        title_desc = ""
        title_desc += "버전: {}\n".format(BOT_VERSION)
        title_desc += "개발자: 감귤#1020 1jgg1020@gmail.com"
        help_embed = embedgen(title = "도움말  :notepad_spiral:", title_desc = title_desc, fields = field_dict)
        help_embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/747866503021461594/910925617913024513/bot.png")
        await ctx.reply(embed = help_embed, mention_author = False)
    elif len(msg) == 2:
        if msg[1] in HELP_COMMAND_DETAIL.keys():
            sub_comm_inline = True
            if "sub_commands_inline" in HELP_COMMAND_DETAIL[msg[1]].keys():
                sub_comm_inline = HELP_COMMAND_DETAIL[msg[1]]["sub_commands_inline"]
            field_dict = {
                "명령어":{"value":msg[1], "inline":True},
                "설명":{"value":HELP_COMMAND_DETAIL[msg[1]]["description"], "inline":True},
                "사용방법":{"value":HELP_COMMAND_DETAIL[msg[1]]["gram_command"], "inline":False},
            }
            if "sub_commands" in HELP_COMMAND_DETAIL[msg[1]]:
                for sub_comm in HELP_COMMAND_DETAIL[msg[1]]["sub_commands"].keys():
                    field_ = {
                        "value":HELP_COMMAND_DETAIL[msg[1]]["sub_commands"][sub_comm],
                        "inline":sub_comm_inline,
                    }
                    field_dict[sub_comm] = field_
            await ctx.reply(embed = embedgen(title = "상세 도움말  :notepad_spiral:", fields = field_dict), mention_author = False)
        else:
            field_dict = {}
            for field_name in HELP_COMMAND.keys():
                field = HELP_COMMAND[field_name][0]
                for field_desc in HELP_COMMAND[field_name][1:]:
                    field = field + ", " + field_desc
                field_ = {
                    "value":field,
                    "inline":False
                }
                field_dict[field_name] = field_     
            title_desc = ""
            title_desc += "버전: {}\n".format(BOT_VERSION)
            title_desc += "개발자: 감귤#1020 1jgg1020@gmail.com"
            await ctx.reply(embed = embedgen(title = "도움말  :notepad_spiral:", title_desc = title_desc, fields = field_dict), mention_author = False)
    else:
        error_field = get_error_msg("ERR_COMMAND_SUBCOMMERR")
        await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)

@bot.command(name = "핑")
async def _ping(ctx):
    try:
        await ctx.reply(embed = embedgen(title = "퐁!  :ping_pong:", title_desc = "{}ms".format(round(bot.latency * 1000)), footer = False), mention_author = False)
    except:
        error_field = get_error_msg("ERR_UNKNOWN")
        await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)

@bot.command(name = "청소")
async def _clean(ctx):
    if ctx.guild:
        if ctx.message.author.guild_permissions.manage_messages or ctx.message.author.id == int(sqlite3_select(table_name = "information", col = "value", condition = "field = \"developer_id\"")[0][0]):
            msg = ctx.message.content.split(' ')
            try:
                if len(msg) == 2:
                    await ctx.channel.purge(limit = int(msg[1]) + 1)
                    await ctx.send(embed = embedgen(title = "청소  :broom:", title_desc = str((msg[1] + "개의 메세지를 삭제 하였습니다"))))
                elif len(msg) == 3:
                    await ctx.reply(embed = embedgen(title = "청소  :broom:", title_desc = str(("추후 추가 예정 기능입니다"))), mention_author = False)
                else:
                    error_field = get_error_msg("ERR_COMMAND_SUBCOMMERR")
                    await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)
            except ValueError:
                error_field = get_error_msg("ERR_VALUEERROR_INTEGER")
                await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)
        else:
            error_field = get_error_msg("ERR_PERMISSION_AUTHOR")
            await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)
    else:
        error_field = get_error_msg("ERR_CLIENT_NOTSERVER")
        await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)

@bot.command(name = "한강수온")
async def _hanriver(ctx):
    try:
        api_key_seoul = sqlite3_select(table_name = "information", col = "value", condition = "field = \"api_key_seoul\"")[0][0]
        request_url = "http://openapi.seoul.go.kr:8088/{}/json/WPOSInformationTime/4/4".format(api_key_seoul)
        request_response = requests.get(request_url)
        if request_response.status_code == 200:
            request_body = request_response.json()
            date:str = str(request_body["WPOSInformationTime"]["row"][0]["MSR_DATE"])
            time:str = str(request_body["WPOSInformationTime"]["row"][0]["MSR_TIME"])
            site:str = str(request_body["WPOSInformationTime"]["row"][0]["SITE_ID"])
            temperature:str = str(request_body["WPOSInformationTime"]["row"][0]["W_TEMP"])
            fields = {
                "온도":{
                    "value": temperature + "°C",
                    "inline":False
                },
                "기준 시간":{
                    "value": date[0:4] + "년 " + date[4:6] + "월 " + date[6:] + "일 " + time,
                    "inline":True
                },
                "기준 측정소":{
                    "value": site,
                    "inline":True
                }
            }
            await ctx.reply(embed = embedgen(title = "한강 수온  :diving_mask:", fields = fields, footer = True), mention_author = False)
        else:
            error_field = get_error_msg("ERR_API_SEOUL")
            await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)
    except:
        error_field = get_error_msg("ERR_UNKNOWN")
        await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)

@bot.command(name = "hi", aliases = ["안녕", "hello"])
async def _hello(ctx):
    reply_list = ["ㅎㅇ", "하이", "헬로", "안녕", "Bonjour", "Hello", "Hi", "你好", "こんにちは", "Chào", "Привет", "أهلا", "I am Groot", "Meow~"]
    await ctx.reply(random.choice(reply_list))

@bot.command(name = "강화")
async def _reinforcement(ctx):
    msg = ctx.message.content.split(' ')
    if len(msg) == 2:
        if msg[1] == "순위":
            if sqlite3_exist(table_name = "data_reinforcement"):
                # Await Rank
            else:
                error_field = get_error_msg("ERR_RFMG_NOITEMSINTABLE")
                await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)  
        elif msg[1] == "요약":
            # 순위 요약
        elif msg[1] == "목록":
            if sqlite3_exist(table_name = "data_reinforcement", condition = f"id_user = {ctx.author.id}"):
                # Await Item Lists
            else:
                error_field = get_error_msg("ERR_RFMG_USERHASNOITEM")
                await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)  
        elif msg[1] == "초기화":
            sqlite3_delete(table_name = "data_reinforcement")
        else:
            if sqlite3_exist(table_name = "data_reinforcement", condition = f"item_name = \'{msg[1]}\', id_user = {ctx.author.id}"):
                # Item Consolidation
            else:
                error_field = get_error_msg("ERR_RFMG_USERHASNOITEM")
                await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)  
    elif len(msg) == 3:
        if msg[2] == "생성":
            if sqlite3_exist(table_name = "data_reinforcement", condition = f"item_name = \'{msg[1]}\', id_user = {ctx.author.id}"):
                error_field = get_error_msg("ERR_RFMG_USERHASITEM")
                await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False) 
            else:
                # Create Item
        elif msg[2] == "삭제":
            if sqlite3_exist(table_name = "data_reinforcement", condition = f"item_name = \'{msg[1]}\', id_user = {ctx.author.id}"):
                sqlite3_delete(table_name = "data_reinforcement", condition = f"item_name = \'{msg[1]}\', id_user = {ctx.author.id}")
                field = {
                    "처리 내용": "아이템 삭제",
                    "아이템 이름": str(msg[1]),
                }
                await ctx.reply(embed = embedgen(title = "강화  :hammer:", fields = field, footer = True), mention_author = False)
            else:
                error_field = get_error_msg("ERR_RFMG_USERHASNOITEM")
                await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)  
        elif msg[2] == "정보":
            if sqlite3_exist(table_name = "data_reinforcement", condition = f"item_name = \'{msg[1]}\', id_user = {ctx.author.id}"):
                # Return Item Information
            else:
                error_field = get_error_msg("ERR_RFMG_USERHASNOITEM")
                await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)  

        else:
            error_field = get_error_msg("ERR_COMMAND_SUBCOMMERR")
            await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)  
    else:
        error_field = get_error_msg("ERR_COMMAND_SUBCOMMERR")
        await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)

@bot.command(name = "번역", aliases = ["번역기", "translator", "trans", "translate"])
async def _translator(ctx):
    msg = ctx.message.content.split(' ')
    if len(msg) > 2:
        try:
            lang_list:dict = {
                "eng":["영어", "English", "english", "Eng", "eng", "en", "US", "us"],
                "kor":["한국어", "한글", "한국", "Korea", "korea", "Korean", "korean", "kor", "ko", "KO", "Kor"]
            }
            if msg[1] in lang_list["eng"]:
                translator = googletrans.Translator()
                text = msg[2] + ""
                for t in msg[3:]:
                    text = f"{text} {t}"
                trans_rest = translator.translate(text, dest = "en", src = 'auto')
                fields = {
                    "번역 (Translation)":{
                        "value": trans_rest.text,
                        "inline": False
                    }
                }  
                await ctx.reply(embed = embedgen(title = "번역기(Translator)  :speech_balloon:", title_desc = f"{googletrans.LANGUAGES[trans_rest.src]} -> {googletrans.LANGUAGES[trans_rest.dest]}", fields = fields, footer = True), mention_author = False)
            elif msg[1] in lang_list["kor"]:
                translator = googletrans.Translator()
                text = msg[2] + ""
                for t in msg[3:]:
                    text = f"{text} {t}"
                trans_rest = translator.translate(text, dest = "ko", src = 'auto')
                fields = {
                    "번역 (Translation)":{
                        "value": trans_rest.text,
                        "inline": False
                    }
                }  
                await ctx.reply(embed = embedgen(title = "번역기(Translator)  :speech_balloon:", title_desc = f"{googletrans.LANGUAGES[trans_rest.src]} -> {googletrans.LANGUAGES[trans_rest.dest]}", fields = fields, footer = True), mention_author = False)
            else:
                error_field = get_error_msg("ERR_COMMAND_SUBCOMMERR")
                await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)
        except:
            error_field = get_error_msg("ERR_UNKNOWN")
            await ctx.reply(embed = embedgen(title = "오류  :no_entry_sign:", fields = error_field, footer = True, error = True), mention_author = False)
    else:
        await ctx.reply()

@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)
    if ctx.author == bot.user:
        return
    log_con(f"{ctx.author}:{ctx.channel}:{ctx.content}")

bot.run(BOT_TOKEN)