# coding: utf-8
from servicecrack.utils.logg import Logging

logging = Logging("base")
import sys


class BaseCrack():
    def __init__(self, host, port, usernames, passwords, service_name, timeout=30):
        self.host = host
        self.port = int(port)
        self.usernames = usernames
        self.passwords = passwords
        self.service_name = service_name
        self.timeout = timeout
        self.result = []
        self.validata_input()
        self.service_exist()
        logging.info("[+]CRACK {} {}:{} start ".format(self.service_name, self.host, self.port))

    def validata_input(self):
        self.validata_host()
        self.validata_u_p()

    def validata_host(self):
        # 校验host 是否为准确的ip
        pass

    def validata_u_p(self):
        # 校验用户名密码列表是否真实存在
        if self.service_name == "redis":
            return
        if not all([self.usernames, self.passwords]):
            logging.error("input error")
            sys.exit(2)

    def service_exist(self):
        # 判断ip的服务端口是否真实
        pass
