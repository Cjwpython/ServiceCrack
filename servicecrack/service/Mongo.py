# coding: utf-8
from pymongo import MongoClient

from servicecrack.service.Base import BaseCrack
from servicecrack.utils.printf import highlight
import datetime
import time

service_name = "mongo"


class MongoCrack(BaseCrack):

    def __init__(self, host, port, usernames, passwords, dbs=["admin"], **kwargs):
        self.dbs = dbs
        super(MongoCrack, self).__init__(host, port, usernames, passwords, service_name, **kwargs)
        if not port:
            self.port = 27017

    def crack(self):
        self.start_time = datetime.datetime.now()
        self.producer()
        self.start_gevent_pool_skip_empty(self.comsumer)

    def producer(self):
        # 生产者
        for db in self.dbs:
            for username in self.real_usernames:
                for password in self.real_passwords:
                    self.task_queue.put_nowait((username, password, db))

    def comsumer(self):
        # 消费者
        time.sleep(self.time_interval)
        username, password, db = self.task_queue.get_nowait()
        is_success, username, password, db_name = self.auth(username, password, db)
        if is_success:
            self.result["crack_result"].append({
                "username": username,
                "password": password,
                "db": db_name
            })

    def auth(self, username, password, db_name):
        self.logging.debug("start use {} {}".format(username, password))
        success = 0
        try:
            conn = MongoClient(self.host, self.port, connectTimeoutMS=self.timeout * 1000)
            db = conn[db_name]  # 这里默认使用admin 进行爆破
            db.authenticate(username, password)
            self.logging.info(highlight("[+] found username:[{}] --- password:[{}]".format(username, password)))
            success = 1
        except Exception as e:
            self.logging.debug(e)
            self.logging.debug("brute faild:{} {}".format(username, password))
            if self.record_crack_flow:
                self.crack_flow(username=username, password=password, db_name=db_name, error_msg=str(e))
            conn.close()
        finally:
            if not success:
                return False, "", "", ""
            conn.close()
            return True, username, password, db_name

    def get_service_info(self):
        conn = MongoClient(self.host, self.port, connectTimeoutMS=self.timeout * 1000)
        service_info = conn.server_info()
        conn.close()
        return service_info

    def crack_flow(self, *args, **kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")
        db_name = kwargs.get("db_name")
        error_msg = kwargs.get("error_msg")
        data = {
            "{}_{}_{}".format(username, password, db_name): {
                "username": username,
                "password": password,
                "db": db_name,
                "error_msg": error_msg
            }
        }
        self.result["crack_flow"].append(data)
