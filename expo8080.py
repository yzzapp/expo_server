import MySQLdb.converters
import os.path
import re
import datetime
import os,sys

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata

import tornado.database

from tornado.escape import json_encode
from tornado.options import define, options

define("mysql_host", default="127.0.0.1:3306", help="db host")
define("mysql_database", default="xxxx", help="db name")
define("mysql_user", default="xxxx", help="db user")
define("mysql_password", default="xxxxxx", help="db password")

def YZZ_GET_DB():
    db = tornado.database.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)
    return db
    
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("2013-05-05 16:20 UPDATED");

class UpdateHotelHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("2013-05-05 16:20 UPDATED.");
    def post(self):
        corr_pwd = "xxxxxx"
        mntn_pwd = self.get_argument("mntn_pwd")
        date_off = self.get_argument("date_off")
        date_bck = self.get_argument("date_bck")
        city_src = self.get_argument("city_src")
        city_dst = self.get_argument("city_dst")
        expo_hll = self.get_argument("expo_hll")
        if corr_pwd == mntn_pwd:
            self.db = YZZ_GET_DB()
            entries = self.db.query("SELECT * FROM HOTEL050610 WHERE HALL = '" + expo_hll +"' ")
            self.write(json_encode(entries))
        else:
            self.write("REQUEST LOST")

class UpdateAirHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("2013-05-09 02:30 UPDATED.");
    def post(self):
        corr_pwd = "xxxxxx"
        mntn_pwd = self.get_argument("mntn_pwd")
        date_off = self.get_argument("date_off")
        date_bck = self.get_argument("date_bck")
        city_src = self.get_argument("city_src")
        city_dst = self.get_argument("city_dst")
        expo_hll = self.get_argument("expo_hll")
        if corr_pwd == mntn_pwd:
            self.db = YZZ_GET_DB()
            entries1 = self.db.query("SELECT CITYPAIR,"+ date_off +" FROM AIRPLAN0509 WHERE CITYPAIR = '" + city_src +"_"+ city_dst +"' ")
            entries2 = self.db.query("SELECT CITYPAIR,"+ date_bck +" FROM AIRPLAN0509 WHERE CITYPAIR = '" + city_dst +"_"+ city_src +"' ")
            self.write(json_encode(entries1))
            self.write("<AND>")
            self.write(json_encode(entries2))
        else:
            self.write("REQUEST LOST")

class CreatingHotelHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("2013-05-05 16:20 UPDATED.");
    def post(self):
        corr_pwd = "xxxxxx"
        mntn_pwd = self.get_argument("mntn_pwd")
        sql = self.get_argument("create_sqls")
        self.db = YZZ_GET_DB()
        if corr_pwd == mntn_pwd:
            self.db.execute(sql)
            self.write("!")
        else:
            self.write("REQUEST LOST")

class HotelWhereHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("HOTEL050610");

class AirWhereHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("AIRPLAN0509");

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/maintain/update/hotels/?", UpdateHotelHandler),
    (r"/maintain/update/airs/?", UpdateAirHandler),
    (r"/disscuss/?", CreatingHotelHandler),
    (r"/maintain/hotel/where/?", HotelWhereHandler),
    (r"/maintain/air/where/?", AirWhereHandler),
])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()


