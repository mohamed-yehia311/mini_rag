from helpers.config import get_setting, Settings

class BaseDataModel:

    def __init__(self, db_client: object):
        self.db_client = db_client
        self.app_Settings = get_setting()
        