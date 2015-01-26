import os
class Config(object):
    DEBUG = False

    SECRET_KEY = os.environ['SECRET_KEY']
    REGISTRY_BASE_URL = os.environ['REGISTRY_BASE_URL']
    REGISTRY_CONSUMER_KEY = os.environ['REGISTRY_CONSUMER_KEY']
    REGISTRY_CONSUMER_SECRET = os.environ['REGISTRY_CONSUMER_SECRET']
    ORGANISATIONS_BASE_URL = os.environ['ORGANISATIONS_BASE_URL']
    FISHING_BASE_URL = os.environ['FISHING_BASE_URL']
    WORK_UK_BASE_URL = os.environ['WORK_UK_BASE_URL']
    LOCALGOV_BASE_URL = os.environ['LOCALGOV_BASE_URL']
    BASE_URL = os.environ['BASE_URL']
    MONGODB_DB = os.environ['MONGODB_DB']
    MONGODB_HOST = os.environ['MONGODB_HOST']
    REDISCLOUD_URL = os.environ['REDISCLOUD_URL']
    CATTLE_BASE_URL = os.environ['CATTLE_BASE_URL']
    WORK_BASE_URL = os.environ['WORK_BASE_URL']
    

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(DevelopmentConfig):
    TESTING = True
