import os

FILE_DIR        =   os.path.dirname(os.path.abspath(__file__))
ICON_FILE       =   os.path.join(FILE_DIR,'icons','icon128.png')
TRAY_ICON_FILE  =   os.path.join(FILE_DIR,'icons','icon32.png')
CONFIG_DIR 	    =	os.path.join(os.getenv("HOME"),'.config','serial2cmd')
CONFIG_FILE     =	os.path.join(CONFIG_DIR, 'config.json')
DEFAULT_CONFIG_FILE = os.path.join(FILE_DIR,'data','config.json')
