# -*- coding: utf-8 -*-
# Author: 梁开孟
# date: 2023/8/24

import os
import base64
import warnings
import dreamlake
import configparser

warnings.filterwarnings('ignore')


def decrypt(text):
    return base64.b64decode(text).decode('utf-8')


def encryption(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')


def get_config(usr='scott', encoding='utf-8'):
    filename = os.path.join(os.path.dirname(dreamlake.__file__), 'ocl.ini')
    if os.path.exists(filename):
        config = configparser.ConfigParser()
        config.read(filename, encoding=encoding)
        try:
            user = decrypt(config.get(usr, 'user'))
            password = decrypt(config.get(usr, 'password'))
            host = decrypt(config.get(usr, 'host'))
            port = decrypt(config.get(usr, 'port'))
            sid = decrypt(config.get(usr, 'sid'))
        except configparser.NoSectionError:
            raise ValueError(f"User '{usr}' not found in configuration file.")
    else:
        raise FileNotFoundError(f"Configuration file not found: {filename}")
    return user, password, host, port, sid


def add_config(user, password, host, port, sid, encoding='utf-8'):
    filename = os.path.join(os.path.dirname(dreamlake.__file__), 'ocl.ini')
    if os.path.exists(filename):
        config = configparser.ConfigParser()
        config.read(filename, encoding=encoding)

        config[user] = {
            'user': encryption(user),
            'password': encryption(password),
            'host': encryption(host),
            'port': encryption(port),
            'sid': encryption(sid)
        }

        with open(filename, 'w') as configfile:
            config.write(configfile)
    else:
        raise FileNotFoundError(f"Configuration file not found: {filename}")


def set_config(session, option, value, encoding='utf-8'):
    filename = os.path.join(os.path.dirname(dreamlake.__file__), 'ocl.ini')
    if os.path.exists(filename):
        config = configparser.ConfigParser()
        config.read(filename, encoding=encoding)

        config.set(session, option, encryption(value))

        with open(filename, 'w') as configfile:
            config.write(configfile)
    else:
        raise FileNotFoundError(f"Configuration file not found: {filename}")
