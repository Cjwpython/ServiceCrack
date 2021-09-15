# coding: utf-8
import datetime
import traceback
from functools import partial
from gevent import queue, pool

from servicecrack.utils.logg import Logging


class BaseCrack():
    def __init__(self, host, port, usernames, passwords, service_name, timeout=30, **kwargs):
        self.host = host
        self.port = int(port)
        self.usernames = usernames
        self.passwords = passwords
        self.service_name = service_name
        self.timeout = timeout
        self.task_queue = queue.Queue()
        self.prepara_result()
        self.password_tmp = ["%user%"]
        self.init_config(**kwargs)

    def init_config(self, **kwargs):
        self.logging_level = kwargs.get("logging_level", "INFO").upper()
        self.logging = Logging(self.service_name, level=self.logging_level)

        self.ignore_noauth = kwargs.get("ignore_noauth", False)  # 是否开启不鉴权
        self.ignore_username_check = kwargs.get("ignore_username_check", False)  # 是否忽略账号检查  针对redis
        self.record_crack_flow = kwargs.get("record_crack_flow", False)  # 是否开启爆破记录
        self.need_service_info = kwargs.get("need_service_info", False)  # 是否需要获取服务信息
        self.time_interval = kwargs.get("time_interval", 0)  # 每次的爆破时间间隔

    def start(self):
        "开启组件爆破"
        self.start_time = datetime.datetime.now()
        self.prepara_crack_dict()
        self.logging.info("[+] start crack {}--{}:{}".format(self.service_name, self.host, self.port))
        if not self.ignore_noauth:
            self.noauth()  # 组件内部实现
        if not self.ignore_noauth and self.result["no_auth"]:
            return  # 当服务开启了未鉴权，跳过爆破
        self.crack()

    def prepara_result(self):
        "为结果准备"
        self.result = {
            "service_name": self.service_name,
            "service_ip": self.host,
            "service_port": self.port,
            "crack_result": [],
            "service_info": "",
            "no_auth": False,
            "no_auth_result": [],
            "crack_flow": []
        }

    def prepara_crack_dict(self):
        # 准备爆破字典
        self.real_usernames = []
        self.real_passwords = []
        crack_usernames = self.usernames
        crack_passwords = self.passwords
        for username in crack_usernames:
            for password in crack_passwords:
                for tmp in self.password_tmp:
                    if tmp in password:
                        self.real_passwords.append(password.replace(tmp, username))
                    else:
                        self.real_passwords.append(password)
            self.real_usernames.append(username)

        self.real_usernames = list(set(self.real_usernames))
        self.real_passwords = list(set(self.real_passwords))
        self.result["usernames_len"] = len(self.real_usernames)
        self.result["passwords_len"] = len(self.real_passwords)
        self.result["real_crack_num"] = len(self.real_usernames) * len(self.real_passwords)

    def get_result(self, *args, **kwargs):
        # 获取检测的结果
        if self.need_service_info:
            self.result["service_info"] = self.get_service_info() if hasattr(self, "get_service_info") else {}
        self.end_time = datetime.datetime.now()
        self.result["runtime"] = (self.end_time - self.start_time).total_seconds()
        self.logging.info("[+] brute {} ending".format(self.service_name))
        return self.result

    def noauth(self):
        # 占位
        pass

    def crack(self):
        # 占位
        pass

    def start_gevent_pool_skip_empty(self, func, *args, **kwargs):
        thread_num = kwargs.pop('thread_num', 1)
        self.gevent_pool = pool.Pool(thread_num)
        for i in range(thread_num):
            self.gevent_pool.spawn(partial(self.gevent_skip_empty_func, func, *args, **kwargs))
        self.gevent_pool.join()

    def gevent_skip_empty_func(self, func, *args, **kwargs):
        while True:
            try:
                func(*args, **kwargs)
            except queue.Empty:
                break
            except Exception:
                self.logging.error(traceback.format_exc())
                continue
