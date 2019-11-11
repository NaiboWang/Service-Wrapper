import os
import ntpath
from datetime import datetime
import json
import numpy as np
import shutil
import time

class Timer:
    def __init__(self,name=""):
        self.name = name
        self.time_interval = -1
        t = datetime.now()
        self.time_start = t.hour * 3600 * 1000.0 + t.minute * 60 * 1000.0 + t.second * 1000.0 + t.microsecond / 1000.0
        print("time_start:"+str(self.time_start))

    def end(self):
        t = datetime.now()
        time_end = t.hour * 3600 * 1000.0 + t.minute * 60 * 1000.0 + t.second * 1000.0 + t.microsecond / 1000.0
        print("time_end:"+str(time_end))
        self.time_interval = float(time_end - self.time_start)
        print('Total time of '+self.name + ':', self.time_interval)

    def getInterval(self):
        return str(round(self.time_interval,0))

def load_csv(path):
    f = open(path)
    lines = f.readlines()  # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
    f.close()
    lines = [line.replace("\n", "") for line in lines]
    return [line.split(",") for line in lines]


def load_lines(file):
    f = open(file)
    lines = f.readlines()  # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
    f.close()
    return [a.replace("\n", "") for a in lines]


def prepare_clean_dir(directory):
    clean_folder(directory)
    prepare_dir(directory)


def prepare_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_filename_and_postfix_from_path(path):
    name = ntpath.basename(path)
    if os.path.isdir(path):
        return name, ""
    else:
        if len(name.split(".")) == 1:
            return name, ""
        else:
            return name.split(".")[0], name.split(".")[1]


def current_datetime():
    return str(datetime.now())


class log:
    def __init__(self, filename='run.log'):
        self.a = open(filename, 'a')

    def write(self, str):
        str = "%s -> %s" % (current_datetime(), str)
        print("Logging %s" % str)
        self.a.write(str + "\n")
        self.a.flush()

    def write_without_datetime(self, str):
        print(str)
        self.a.write(str + "\n")
        self.a.flush()
    def __del__(self):
        self.a.close()


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


def save_json(path, data, encoding="utf-8"):
    with open(path, 'w', encoding=encoding) as outfile:
        json.dump(data, outfile, ensure_ascii=False, cls=MyEncoder,skipkeys=True,sort_keys=True, indent=4, separators=(',', ':'))


def load_json(path, encoding="utf-8"):
    with open(path, encoding=encoding) as data_file:
        return json.load(data_file)


def save_text(path, text, encoding="utf-8"):
    with open(path, "w", encoding=encoding) as text_file:
        print(text, file=text_file, encoding=encoding)


def clean_folder(path):
    if is_path_exists(path):
        shutil.rmtree(path)


import pickle


def save_pickle(path, obj):
    with open(path, mode='wb') as f:
        pickle.dump(obj, f)


def load_pickle(path):
    with open(path, mode='rb') as f:
        return pickle.load(f)


def get_all_folders(directory):
    return [name for name in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, name))]


try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def get_hostname_from_url(url):
    parsed_uri = urlparse(url)
    return parsed_uri.hostname


def is_path_exists(path):
    return os.path.exists(path)


if __name__ == "__main__":
    print(get_hostname_from_url("http://docs.python.jp/2/library/urlparse.html"))
