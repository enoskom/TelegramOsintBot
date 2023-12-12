import sqlite3
import datetime
import telebot
import threading
import shutil
import os
import random
import requests
import time
import platform
from pydub import AudioSegment
from telebot import types

# external library imports
from varaibles import *




# check temp dir if not exists make a dir
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


# connect a authentication database 
MAIN_DATABSE = sqlite3.connect(database=AUTH_DATABASE, check_same_thread=False)
MAIN_DATABASE_CUROSR = MAIN_DATABSE.cursor()
MAIN_DATABASE_CUROSR.execute(DATABASE_INIT_COMMAND)


# print global varaibles from screen
GetVarables()


# insert owner id in databsae
def generate_owner_user(telegram_id:str):
    
    check_user_exists = f"SELECT * FROM {AUTH_TABLE_NAME} WHERE telegram_id=?"
    MAIN_DATABASE_CUROSR.execute(check_user_exists, (telegram_id,))
    results = MAIN_DATABASE_CUROSR.fetchall()
    if len(results) != 0:
        return [ "false", f"Kullanıcı: {telegram_id} zaten sistemde var"]
    
    insert_tuple = (telegram_id, 0, ReturnCreateTime() )
    generate_user = f"""INSERT INTO {AUTH_TABLE_NAME} (telegram_id,  is_admin, create_date) VALUES (?, ?,?)"""    
    MAIN_DATABASE_CUROSR.execute(generate_user, insert_tuple)
    MAIN_DATABSE.commit()
    return ["true", f"Kullanıcı: {telegram_id} eklendi"]



# insert new admin in database 
def add_new_admin(telegram_id:str):
    
    check_user_exists = f"SELECT * FROM {AUTH_TABLE_NAME} WHERE telegram_id=?"
    MAIN_DATABASE_CUROSR.execute(check_user_exists, (telegram_id,))
    results = MAIN_DATABASE_CUROSR.fetchall()
    if len(results) != 0:
        return [ "false", f"user {telegram_id} exists"]
    insert_tuple = (telegram_id, 1, ReturnCreateTime() )
    generate_user = f"""INSERT INTO {AUTH_TABLE_NAME} (telegram_id,  is_admin, create_date) VALUES (?, ?,?)"""    
    MAIN_DATABASE_CUROSR.execute(generate_user, insert_tuple)
    MAIN_DATABSE.commit()
    return ["true", f"user: {telegram_id} eklendi"]


# delete admin from database
def un_admin(telegram_id:str):
    telegram_id = telegram_id
    if telegram_id == OWNER_TELEGRAM_ID:
        return [ "false" , "kurucu yetkileri alınamaz" ]
    
    
    check_user_exists = f"SELECT * FROM {AUTH_TABLE_NAME} WHERE telegram_id=?"
    MAIN_DATABASE_CUROSR.execute(check_user_exists, (telegram_id,))
    results = MAIN_DATABASE_CUROSR.fetchall()
    if len(results) == 0:
        return [ "false", f"user {telegram_id} not exists"]
    command_is = f"DELETE FROM {AUTH_TABLE_NAME} WHERE telegram_id=?"
    MAIN_DATABASE_CUROSR.execute(command_is, (telegram_id,))
    MAIN_DATABSE.commit()
    return [ "true", f"user {telegram_id} deleted." ]

# check user is owner if is owner return true else return false
def is_owner(telegram_id:str):
    telegram_id = str(telegram_id)
    
    query_sql = f"SELECT * FROM {AUTH_TABLE_NAME} WHERE telegram_id=? AND is_admin=?"
    query_tuple = (telegram_id, AUTH_OWNER_CODE)
    MAIN_DATABASE_CUROSR.execute(query_sql, query_tuple)
    results = MAIN_DATABASE_CUROSR.fetchall()
    if len(results) != 0:
        return True
    else:
        return False
    
# check user is admin or un authorized user
def is_admin(telegram_id:str):
    telegram_id = str(telegram_id)
    query_sql = f"SELECT * FROM {AUTH_TABLE_NAME} WHERE telegram_id=? AND is_admin=?"
    query_tuple = (telegram_id, AUTH_ADMIN_CODE)
    MAIN_DATABASE_CUROSR.execute(query_sql, query_tuple)
    results = MAIN_DATABASE_CUROSR.fetchall()
    if len(results) != 0:
        return True
    else:
        return False


# check access status
def is_yetkili(telegram_id:str):
    
    if is_owner(telegram_id=telegram_id):
        return True
    query_sql = f"SELECT * FROM {AUTH_TABLE_NAME} WHERE telegram_id=? AND is_admin=?"
    query_tuple = (telegram_id, AUTH_ADMIN_CODE)
    MAIN_DATABASE_CUROSR.execute(query_sql, query_tuple)
    results = MAIN_DATABASE_CUROSR.fetchall()
    if len(results) != 0:
        return True
    else:
        return False
    
    
# set a bot object 
TelegramOsintProject = telebot.TeleBot(token=TELEGRAM_BOT_TOKEN)
generate_owner_user(OWNER_TELEGRAM_ID)


@TelegramOsintProject.message_handler(commands=["newadmin"])
def add_new_admin(msg): 
    command_inviter = msg.from_user
    inviter_id = str(command_inviter.id)
    
    if not is_owner(inviter_id):
        return
    
    if msg.reply_to_message != None:
        results_is = add_new_admin(str(msg.reply_to_message.from_user.id))
        if results_is[0] != "true":
            TelegramOsintProject.reply_to(msg, f"Hata: {str(results_is[1])}")
        else:
            TelegramOsintProject.reply_to(msg, f"işlem başarılı: {str(results_is[1])}")
    elif len(msg.text.split(" ")) >= 2:
        target_user_id = msg.text.split(" ")[1]
        if not target_user_id.isnumeric():
            err_msg = "[ - ] Hata: Kullanıcı id si nümerik olmalıdır."
            TelegramOsintProject.reply_to(msg, text=err_msg)
            return                    
        results_is = add_new_admin(str(target_user_id))
        TelegramOsintProject.reply_to(msg, text=results_is[1])
        return
    else:
        TelegramOsintProject.reply_to(msg,"Lütfen eklenecek kişinin mesajını yanıtlayınız.")
        return 


@TelegramOsintProject.message_handler(commands=["deladmin"])
def delete_admin(msg):
    command_inviter = msg.from_user
    inviter_id = str(command_inviter.id)
    
    if not is_owner(inviter_id):
        return
        
    if msg.reply_to_message != None:
        target_id = str(msg.reply_to_message.from_user.id)
        targetFullname= str(msg.reply_to_message.from_user.full_name)
        unadm_status = un_admin(target_id)
        TelegramOsintProject.reply_to(msg, unadm_status[1])
        return
    elif len(msg.text.split(" ")) >= 2:
        target_user_id = msg.text.split(" ")[1]
        if not target_user_id.isnumeric():
            err_msg = "[ - ] Hata: Kullanıcı id si nümerik olmalıdır."
            TelegramOsintProject.reply_to(msg, text=err_msg)
            return    
        results_is = un_admin(str(target_user_id))
        TelegramOsintProject.reply_to(msg, text=results_is[1])
        return
    else:
        TelegramOsintProject.reply_to(msg, "Lütfen bir mesaj yanıtlayınız.")
        return




@TelegramOsintProject.message_handler(commands=["checkadmin"])
def admin_control(msg):
    command_inviter = msg.from_user
    inviter_id = str(command_inviter.id)
    if not is_yetkili(inviter_id):
        return
        
    if msg.reply_to_message != None:
        target_id = str(msg.reply_to_message.from_user.id)
        target_username = str(msg.reply_to_message.from_user.username)
        if is_yetkili(target_id):
            TelegramOsintProject.reply_to(msg, f"USER: @{str(target_username)}\nID: {str(target_id)}\nDurum: yetkili ✅ ")
        else:
            TelegramOsintProject.reply_to(msg, f"USER: @{str(target_username)}\nID: {str(target_id)}\nDurum yetkisiz ❌ ")
    else:
        target_id = str(msg.from_user.id)
        target_username = str(msg.from_user.username)
        if is_yetkili(target_id):
            TelegramOsintProject.reply_to(msg, f"USER: @{str(target_username)}\nID: {str(target_id)}\nDurum: yetkili ✅ ")
        else:
            TelegramOsintProject.reply_to(msg, f"USER: @{str(target_username)}\nID: {str(target_id)}\nDurum yetkisiz ❌ ")


@TelegramOsintProject.message_handler(commands=["help", "start"])
def print_help_menu(msg):
    command_inviter = msg.from_user
    inviter_id = str(command_inviter.id)
    if not is_yetkili:
        return
    TelegramOsintProject.reply_to(msg, text=COMMAND_LIST, parse_mode="markdown")



# run loop
TelegramOsintProject.infinity_polling()