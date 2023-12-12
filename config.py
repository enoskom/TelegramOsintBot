# CONFIG FILE 
# For Telegram Osint Bot

OWNER_TELEGRAM_ID = "" # ADD yout owner id



TELEGRAM_BOT_TOKEN = "" # ADD your telegram bot token 

# Bot name for global 
APP_NAME = "Telegram Osint Bot"

# bot version 
APP_VERSION = "Test Release"

# temporary work dir 
TEMP_DIR = "tmp"+os.sep


# database name  
AUTH_DATABASE = "TOB.sqlite3"

LOG_DATABASE = AUTH_DATABASE

# Authentication codes 0 = owner and 1 = normal admin
AUTH_OWNER_CODE = "0"
AUTH_ADMIN_CODE = "1"

# database table names
AUTH_TABLE_NAME = "telegram_users"



# initral database schema  
DATABASE_INIT_COMMAND  = f"""
    CREATE TABLE IF NOT EXISTS {AUTH_TABLE_NAME} (
    id INTEGER NOT NULL,
    telegram_id INTEGER NOT NULL UNIQUE,
    is_admin INTEGER NOT NULL,
    create_date TEXT NOT NULL,
    PRIMARY KEY("id")
    );
"""
    

# help commands
COMMAND_LIST = f"""{APP_NAME} COMMAND LIST

`/getip 1.1.1.1`
Fetches the information of the target ipv4 address via ipinfo.io

`/getshodan 1.1.1.1`
Searches for target ip address via shodan

`/getiban TRXXXXXXXXXXXXXXXXXXXX`
Parses for target IBAN number 
"""


# information func
def GetVarables() -> None:
    print(f"\VARABLES INFO:")
    print("-"*50)
    print(f"[+] Owner Telegram id       : {OWNER_TELEGRAM_ID}")
    print(f"[+] Telegram user database  : {AUTH_DATABASE}")
    print(f"[+] Temp dir                : {TEMP_DIR}")
    print(f"[+] App name                : {APP_NAME}")
    print(f"[+] Version                 : {APP_VERSION}")
    print("-"*50)
    print("\n\nLOG CONSOLE:")
    print("-"*50)


