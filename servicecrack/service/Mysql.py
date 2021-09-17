# coding: utf-8
import pymysql
from servicecrack.service.Base import BaseCrack
from servicecrack.utils.printf import highlight

service_name = "mysql"


class MysqlCrack(BaseCrack):
    def __init__(self, host, port, usernames, passwords, **kwargs):
        super(MysqlCrack, self).__init__(host, port, usernames, passwords, service_name, **kwargs)
        if not port:
            self.port = 3306

    def crack(self):
        self.producer()
        self.start_gevent_pool_skip_empty(self.comsumer)

    def producer(self):
        # 生产者
        for username in self.real_usernames:
            for password in self.real_passwords:
                self.task_queue.put_nowait((username, password))

    def comsumer(self):
        # 消费者
        username, password = self.task_queue.get_nowait()

        is_success, username, password = self.auth(username, password)
        if is_success:
            self.result["crack_result"].append({
                "username": username,
                "password": password
            })

    def auth(self, username, password):
        self.logging.debug("start use {} {}".format(username, password))
        success = 0
        try:
            conn = pymysql.connect(host=self.host, port=self.port, user=username, password=password, connect_timeout=self.timeout)
            self.logging.info(highlight("[+] found username:[{}] --- password:[{}]".format(username, password)))
            success = 1
        except Exception as e:
            self.logging.debug(e)
            self.logging.debug("brute faild:{} {}".format(username, password))
            if self.record_crack_flow:
                self.crack_flow(username=username, password=password, error_msg=str(e))
            conn.close()
        finally:
            if not success:
                return False, "", ""
            conn.close()
            return True, username, password

    def get_service_info(self):
        conn = pymysql.connect(host=self.host, port=self.port, user="admin", password="admin", connect_timeout=self.timeout)
        service_info = {"version": conn.get_server_info()}
        conn.close()
        return service_info

    def crack_flow(self, *args, **kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")
        error_msg = kwargs.get("error_msg")
        data = {
            "{}_{}".format(username, password): {
                "username": username,
                "password": password,
                "error_msg": error_msg
            }
        }
        self.result["crack_flow"].append(data)
