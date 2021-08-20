# coding: utf-8
import telnetlib

from servicecrack.service.Base import BaseCrack
from servicecrack.utils.logg import Logging

logging = Logging("telnet")

service_name = "telnet"


class TelnetCrack(BaseCrack):
    def __init__(self, host, port, usernames, passwords):
        super(TelnetCrack, self).__init__(host, port, usernames, passwords, service_name)
        if not port:
            self.port = 23

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
            tn = telnetlib.Telnet(host=self.host, port=self.port, timeout=self.timeout)
            tn.set_debuglevel(0)
            tn.read_until("login: ")
            tn.write(username + '\r\n')
            tn.read_until("assword: ")
            tn.write(password + '\r\n')
            result = tn.read_some()
            result = result + tn.read_some()
            if result.find('Login Fail') > 0 or result.find('incorrect') > 0:
                pass
            else:
                logging.info("brute success :{} {}".format(username, password))
            success = 1
        except Exception as e:
            logging.debug(e)
            logging.debug("brute faild:{} {}".format(username, password))
            tn.close()
        finally:
            if not success:
                return
            tn.close()
            self.result.append({"username": username, "password": password})



