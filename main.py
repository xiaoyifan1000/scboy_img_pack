import shutil
import requests
import re
import sqlite3
import os
import sys
import io
import zipfile
import time
import logging
from bs4 import BeautifulSoup

MAIN_Version = "1.4v"

DEBUG = {"NOT_DOWN_IMG": False, "NOT_DOWN_HOME": False, "RUNNING_TIME": 1}
HTML_URL = "https://www.scboy.cc/"
DB_LITE = "scboy_href_img.db"
DEFAULT = {"MIN_LIST_IMG": 3}
SAVE_FILE = '/www/wwwroot/zfile-4.0.0'
os.environ['NO_PROXY'] = 'https://www.scboy.cc/'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
logging.basicConfig(filename='RUNNING.log', level=logging.DEBUG)

cookies = {"cookie_test": "XA15uePgyGWSUXgvXaxnOn2xsKtoCmpJYDB_2B03BT5P0Dy7c2fxvPRl3vVAK7GuY6",
           "bbs_token": "psplofa8vpWIVQuNSLYR_2BPHRmcFZswPHwOSXER2fB1NZXeV2XjDNhKDB4aN7rzyFavJDkLL6WTmXXztj0HAjqQ_3D_3D",
           "bbs_sid": "ea6181ebec15b9c997a07665e76e8071",
           "CNZZDATA1277689586": "145085965-1668180101-https%253A%252F%252Fwww.scboy.cc%252F%7C1669689128",
           "UM_distinctid": "184677d0f09443-0138e82e96a4b9-26021e51-1fa400-184677d0f0a1575"}


def log_record(func):
    """
    1.3v add logging
    """

    def running(*args, **kwargs):
        try:
            _return = func(*args, **kwargs)
            logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} {func.__name__}: success")
            return _return
        except Exception as out:
            logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} function {func.__name__}: {out}")
    return running


class SQlScboy:
    def __init__(self):
        self.sql_data = sqlite3.connect(DB_LITE)

    def get_cursor(self):
        return self.sql_data.cursor()

    def execute(self, script: str):
        return self.sql_data.execute(script)

    def commit(self):
        self.sql_data.commit()

    def close(self):
        self.sql_data.close()

    def exe_insert(self, id_: int, data_href: str,  data_user: str, data_head: str, data_name="data"):
        self.execute(f"INSERT INTO {data_name}(id, data_href, data_user, data_head) values({id_}, \"{data_href}\", \"{data_user}\", \"{data_head}\");")

        self.commit()

    """
    2022/12/3  database table change
    id int, data_href string, data_tid int, data_head string
    ->
    id int, data_href string, data_user string, data_head string
    """

    def new_tabel(self, name: str):
        self.execute(f"create table {name}(id int, data_href string, data_user string, data_head string)")
        self.commit()

    """
    2022/12/3 database init table change
    id int, data_href string, data_tid int, data_head string
    ->
    id int, data_href string, data_user string, data_head string

    """

    def select_id(self, id_: int, name="data"):
        cur = self.execute(f"select * from {name} where id={id_}")
        self.commit()
        return cur.fetchall()

    def del_id(self, _id):
        self.execute(f'DELETE FROM data WHERE id={_id};')
        self.commit()

    def select_all(self, name="data"):
        cur = self.execute(f"select * from {name}")
        self.commit()
        return cur.fetchall()

    def alter_new_row(self, row_name="data_head", table_name="data"):
        self.execute(f"ALTER TABLE {table_name} ADD COLUMN {row_name} string;")
        self.commit()

    def pragma_name(self, table_name="data"):
        cur = self.execute(f"pragma table_info('{table_name}');")
        return cur.fetchall()


class Run:

    dict_data = dict()

    @log_record
    def __init__(self):
        self.sql_data = SQlScboy()

    @log_record
    def first_run(self):
        if not self.sql_data.pragma_name():
            self.sql_data.new_tabel("data")

    @log_record
    def down_scboy_biaoche(self):
        if not DEBUG["NOT_DOWN_HOME"]:
            for a in range(3):
                response = requests.get(f"{HTML_URL}?forum-2-1.htm&tagids=16___", cookies=cookies)
                if response.status_code == 200:
                    with open("scboy.html", "+w", encoding='utf-8') as f:
                        f.write(response.text)
                    continue
                else:
                    time.sleep(3)  # sleep 1s again
            """ 
            2022/12/3 add status code
            2022/12/14 modify code logic
            """

    @log_record
    def save_img_html(self):
        with open("scboy.html", "r", encoding='utf-8') as f:
            file = f.read()
            list_tap = re.findall('<li class="media thread tap  " data-href=[\s\S]*?>([\s\S]*?)</li>', file)

        for a in list_tap:
            list_0 = re.findall('<a class="xs-thread-a" onclick="atarget\(this\)".*</a>', a)
            data_href = re.findall('href="(.*)"', list_0[0])[0]
            data_tid = re.findall('\?thread-(\d*)\.htm', list_0[0])[0]
            data_head = re.findall('>(.*)</a>', list_0[0])[0]
            list_user = re.findall('<span class="username text-grey mr-1  hidden-sm" uid="\d*">(.*)</span>', a)
            data_user = list_user[0]
            """
            2022/12/3 source change
            <a class="xs-thread-a">
            ->
            <li class="media thread tap  ">
            """
            self.dict_data.update({data_tid: {"data_href": data_href, "data_user": data_user, "data_head": data_head}})
            """
            2022/12/3 Synchronize changes
            data_tid, data_href, data_tid, data_head
            ->
            data_tid, data_href, data_user, data_head
            """

        for key, values in self.dict_data.items():
            if self.sql_data.select_id(int(key)):
                continue

            self.sql_data.exe_insert(int(key), values["data_href"], values["data_user"], values["data_head"])
            """
            2022/12/3 Synchronize changes
            int(values["data_tid"])
            ->
            values["data_user"]
            """
            self.sql_data.commit()
            if not DEBUG["NOT_DOWN_IMG"]:
                self._down_img_from_href(values["data_href"])
            time.sleep(DEBUG["RUNNING_TIME"])

        self.sql_data.close()

    @log_record
    def _down_img_from_href(self, data_href):
        response_t = requests.get(f'https://www.scboy.cc/{data_href}', cookies=cookies)
        if not response_t.status_code == 200:
            return
        """
        2022/12/3 add status code
        """
        if not os.path.exists("Temp"):
            os.mkdir("Temp")

        with open(f"./Temp/{data_href[1:]}", "+w", encoding='utf-8') as f:
            f.write(response_t.text)

        self._down_img(data_href)

    @log_record
    def _down_img(self, data_href):

        with open(f"./Temp/{data_href[1:]}", "r", encoding='utf-8') as f:
            file = f.read()

        soup = BeautifulSoup(file, 'html.parser')
        file = str(soup.find(class_="message break-all"))
        """
        $new
        file: all html ->
        <div class="message break-all>
        $new 1.4v
        import new pack BeautifulSoup
        re find <div class="message break-all> ->
        BeautifulSoup find message break-all
        """
        list_jpg = re.findall(f'{HTML_URL}upload/attach/\d*/\d*_[a-zA-Z0-9]*\.jpg', file)
        list_png = re.findall(f'{HTML_URL}upload/attach/\d*/\d*_[a-zA-Z0-9]*\.png', file)
        list_gif = re.findall(f'{HTML_URL}upload/attach/\d*/\d*_[a-zA-Z0-9]*\.gif', file)
        list_jpeg = re.findall(f'{HTML_URL}upload/attach/\d*/\d*_[a-zA-Z0-9]*\.jpeg', file)

        def zip_file(src_dir):
            zip_name = src_dir + '.zip'
            z = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
            for dirpath, dirnames, filenames in os.walk(src_dir):
                fpath = dirpath.replace(src_dir, '')
                fpath = fpath and fpath + os.sep or ''
                for filename in filenames:
                    z.write(os.path.join(dirpath, filename), fpath + filename)
            z.close()
            logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}: zip generate success")

        def down_img(_list: list, _data_href):
            if _list and len(_list) >= DEFAULT["MIN_LIST_IMG"]:
                if not os.path.exists(f"{SAVE_FILE}/img"):
                    os.mkdir(f"{SAVE_FILE}/img")
                if not os.path.exists(f"{SAVE_FILE}/img/{_data_href[1:]}"):
                    os.mkdir(f"{SAVE_FILE}/img/{_data_href[1:]}")

                for a in _list:
                    response_t = requests.get(a)
                    if response_t.status_code == 200:
                        if a[-3:] == "jpg":
                            with open(f"{SAVE_FILE}/img/{_data_href[1:]}/" + re.findall('\d*_[a-zA-Z0-9]*\.jpg', a)[0], "+wb") as f_0:
                                f_0.write(response_t.content)
                        if a[-3:] == "png":
                            with open(f"{SAVE_FILE}/img/{_data_href[1:]}/" + re.findall('\d*_[a-zA-Z0-9]*\.png', a)[0], "+wb") as f_1:
                                f_1.write(response_t.content)
                        if a[-3:] == "gif":
                            with open(f"{SAVE_FILE}/img/{_data_href[1:]}/" + re.findall('\d*_[a-zA-Z0-9]*\.gif', a)[0], "+wb") as f_2:
                                f_2.write(response_t.content)
                        if a[-4:] == "jpeg":
                            with open(f"{SAVE_FILE}/img/{_data_href[1:]}/" + re.findall('\d*_[a-zA-Z0-9]*\.jpeg', a)[0], "+wb") as f_2:
                                f_2.write(response_t.content)

                logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}: down img from {_data_href} success")

                zip_file(f"{SAVE_FILE}/img/{_data_href[1:]}")
                shutil.move(f"{SAVE_FILE}/img/{_data_href[1:]}.zip", f"{SAVE_FILE}/img/{_data_href[1:]}/{_data_href[1:]}.zip")

        down_img(list_gif, data_href)
        down_img(list_jpg, data_href)
        down_img(list_png, data_href)
        down_img(list_jpeg, data_href)

    def _add_new_tabel(self):
        self.sql_data.new_tabel("data")




