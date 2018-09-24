import os
import yaml


env_config_name = os.path.join(os.path.dirname(__file__), 'env.yaml')
ENVIRONMENTS = yaml.safe_load(open(env_config_name))

# Please setup your env name and env.yaml accordingly
ENV_NAME = 'dev'

ENV = ENVIRONMENTS[ENV_NAME]

DATABASE_IP = ENV.get('database-ip')
DATABASE_PORT = ENV.get('database-port')
DATABASE_USER = ENV.get('database-user')
DATABASE_PASSWORD = ENV.get('database-password')
DATABASE_NAME = ENV.get('database-name')

LOCAL_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@{ip}:{port}/{database}').format(
        user=DATABASE_USER, password=DATABASE_PASSWORD, ip=DATABASE_IP, port=DATABASE_PORT,
        database=DATABASE_NAME)

SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI
