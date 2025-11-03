from configparser import ConfigParser

config = ConfigParser()

TFL_APP_ID=config['DEFAULT'].get('TFL_APP_ID', '')
