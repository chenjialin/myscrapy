# -*- coding: utf-8 -*-
import os
import configparser

from sqlalchemy import create_engine

BaseDir = os.path.dirname(os.path.dirname(__file__))

config = configparser.ConfigParser()
env = os.environ.get('DATAMINING_ENV', 'LOCAL')  # PROD/DEV/LOCAL

if env in ('PROD', 'UAT'):
    config.read(os.path.join(BaseDir, 'conf/conf.ini'))
elif env == 'DEV':
    config.read(os.path.join(BaseDir, 'conf/conf_dev.ini'))
else:
    config.read(os.path.join(BaseDir, 'conf/conf_local.ini'))


# data mining db
default_engine = create_engine('mysql+pymysql://{user}:{pass_wd}@{host}:{port}/{db}?charset={charset}'.format(
            user=config.get("DB", "User"),
            pass_wd=config.get("DB", "Password"),
            host=config.get("DB", "Host"),
            port=config.get("DB", "Port"),
            db=config.get("DB", "Db"),
            charset='utf8'),
            echo=False,
            pool_size=50,
            pool_recycle=3600)
