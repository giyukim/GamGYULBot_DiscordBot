from flask import Flask
from flask_restx import Resource, Api, reqparse
import pymysql
import requests

db = pymysql.connect(
    user = "root",
    passwd = "<root password>", #password
    host = "127.0.0.1",
    db = "GamGYULBotV2_DEV",
    charset = "utf8mb4"
) #pymysql.cursors.DictCursor

#Call API Auth token -> api_token
api_token:str = ""
with db:
    with db.cursor() as cursor:
        sql = "SELECT `value` FROM `information` WHERE `name`=`api_auth_token`"
        cursor.execute()
        api_token = str(cursor.fetchone()[0][0])

# Call Seoul API Key -> api_key_seoul
api_key_seoul:str = ""
with db:
    with db.cursor() as cursor:
        sql = "SELECT `value` FROM `information` WHERE `name`=`api_key_seoul`"
        cursor.execute(sql)
        api_key_seoul = str(cursor.fetchone()[0][0])

# Call Bot Version -> bot_version:str
bot_version:str = ""
with db:
    with db.cursor() as cursor:
        sql = "SELECT `value` FROM `information` WHERE `name`=`bot_version`"
        cursor.execute(sql)
        bot_version = str(cursor.fetchone()[0][0])
        
app = Flask(__name__)
api = Api(app)

@api.route("/v1/hangang")
class Hangang(Resource):
    def get(self):
        request_url = "http://openapi.seoul.go.kr:8088/{}/json/WPOSInformationTime/4/4".format(api_key_seoul)
        request_response = requests.get(request_url)
        if request_response.status_code == 200:
            request_body = request_response.json()
            date:str = str(request_body["WPOSInformationTime"]["row"][0]["MSR_DATE"])
            time:str = str(request_body["WPOSInformationTime"]["row"][0]["MSR_TIME"])
            site:str = str(request_body["WPOSInformationTime"]["row"][0]["SITE_ID"])
            temperature:str = str(request_body["WPOSInformationTime"]["row"][0]["W_TEMP"])
            return {"date": date, "time": time, "site": site, "temperature": temperature}, 200
        else:
            return {"message": "Occured Unknown Errors"}, 404
        
@api.route("/v1/reinforce/<int:user_id>/<str:item_name>")
class Reinforce(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("token", type = str, required = True, location = "headers")
    parser.add_argument("id_guild", type = str, required = True, location = "form")
    parser.add_argument("item_level", type = int, required = False, location = "form")
    parser.add_argument("item_level_high", type = int, required = False, location = "form")
    parser.add_argument("item_level_up", type = int, required = False, location = "form")
    parser.add_argument("item_level_down", type = int, required = False, location = "form")
    parser.add_argument("item_rein_num", type = int, required = False, location = "form")
    parser.add_argument("item_rein_saved", type = int, required = False, location = "form")
    parser.add_argument("item_rein_broken", type = int, required = False, location = "form")
    parser.add_argument("item_rein_succ", type = int, required = False, location = "form")
    parser.add_argument("item_rein_failed", type = int, required = False, location = "form")
    parser.add_argument("time_stamp", type = str, required = True, location = "form")
    def post(self, user_id, item_name):
        req_body = Reinforce.parser.parse_args()
        if not req_body["token"] == api_token:
            return {"message": "Unauthorized"}, 401
        else:
            with db:
                with db.cursor(pymysql.cursors.DictCursor):
                    sql = "INSERT INTO `data_reinforcement` (`id_user`, `id_guild`, `item_name`, `) VALUES (%s, %s)"


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 8888)