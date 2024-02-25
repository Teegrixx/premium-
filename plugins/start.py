from datetime import date as date_
import datetime
import os
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
import time
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, ForceReply)
import humanize
from helper.progress import humanbytes
from pytz import timezone
from helper.database import insert, find_one, used_limit, usertype, uploadlimit, addpredata, total_rename, total_size
from pyrogram.file_id import FileId
from helper.database import daily as daily_
from helper.date import add_date, check_expi
from config import Config

botid = Config.BOT_TOKEN.split(':')[0]

# Part of Day --------------------
currentTime = datetime.datetime.now()

if currentTime.hour < 12:
    wish = "Good morning."
elif 12 <= currentTime.hour < 12:
    wish = 'Good afternoon.'
else:
    wish = 'Good evening.'

# -------------------------------


@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    old = insert(int(message.chat.id))
    curr = datetime.datetime.now(timezone("Asia/Kolkata"))
    date = curr.strftime('%d %B, %Y')
    time = curr.strftime('%I:%M:%S %p')
    bot_get = await client.get_me()
    await client.send_message(chat_id=Config.LOG_CHANNEL, text=f"**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\nUꜱᴇʀ: {message.from_user.mention}\nIᴅ: `{message.from_user.id}`\nUɴ: @{message.from_user.username}\nFɪʀsᴛ Nᴀᴍᴇ: {message.from_user.first_name}\n\nDᴀᴛᴇ: {date}\nTɪᴍᴇ: {time}\n\nBy: @{bot_get.username}")
    try:
        id = message.text.split(' ')[1]
    except:
        await message.reply_text(text=f"""
	Hello {wish} {message.from_user.first_name }
	__I am file renamer bot, Please sent any telegram 
	**Document Or Video** and enter new filename to rename it__
	""", reply_to_message_id=message.id,
                                 reply_markup=InlineKeyboardMarkup(
                                     [[InlineKeyboardButton("SUPPORT 🐐 "  ,url="https://t.me/grixxtech")],
                                      [InlineKeyboardButton("OWNER 🐮 ", url="https://t.me/teegrixx")]]))
        return
    if id:
        if old == True:
            try:
                await client.send_message(id, "Your Friend already Using Our Bot")
                await message.reply_text(text=f"""
	Hello {wish} {message.from_user.first_name }
	__I am file renamer bot, Please sent any telegram 
	**Document Or Video** and enter new filename to rename it__
	""", reply_to_message_id=message.id,
                                         reply_markup=InlineKeyboardMarkup(
                                             [[InlineKeyboardButton("SUPPORT 🐐"  ,url="https://t.me/grixxtech")], 
                                              [InlineKeyboardButton("OWNER 🐮", url="https://t.me/teegrixx")]]))
            except:
                return
        else:
            await client.send_message(id, "Congrats! You Won 100MB Upload limit")
            _user_ = find_one(int(id))
            limit = _user_["uploadlimit"]
            new_limit = limit + 104857600
            uploadlimit(int(id), new_limit)
            await message.reply_text(text=f"""
	Hello {wish} {message.from_user.first_name }
	__I am file renamer bot, Please sent any telegram 
	**Document Or Video** and enter new filename to rename it__
	""", reply_to_message_id=message.id,
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton("SUPPORT 🐐"  ,url="https://t.me/grixxtech")], 
                                          [InlineKeyboardButton("OWNER 🐮", url="https://t.me/teegrixx")]]))

@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def send_doc(client, message):
    update_channel = Config.FORCE_SUB
    user_id = message.from_user.id
    if update_channel:
        try:
            await client.get_chat_member(update_channel, user_id)
        except UserNotParticipant:
            await message.reply_text("**__You are not subscribed my channel__** ",
                                     reply_to_message_id=message.id,
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton("CHANNEL 📱 "  ,url=f"https://t.me/{update_channel}")]]))
            return
    try:
        bot_data = find_one(int(botid))
        prrename = bot_data['total_rename']
        prsize = bot_data['total_size']
        user_deta = find_one(user_id)
    except:
        await message.reply_text("Use About cmd first /about")
    try:
        used_date = user_deta["date"]
        buy_date = user_deta["prexdate"]
        daily = user_deta["daily"]
        user_type = user_deta["usertype"]
    except:
        await message.reply_text("Database has been Cleared click on /start")
        return

    c_time = time.time()

    if user_type == "Free":
        LIMIT = 600
    else:
        LIMIT = 50
    then = used_date + LIMIT
    left = round(then - c_time)
    conversion = datetime.timedelta(seconds=left)
    ltime = str(conversion)
    if left > 0:
        await message.reply_text(f"Sorry Dude I am not only for YOU \n Flood control is active so please wait for {ltime} ", reply_to_message_id=message.id)
    else:
        # Forward a single message

        media = await client.get_messages(message.chat.id, message.id)
        file = media.document or media.video or media.audio
        dcid = FileId.decode(file.file_id).dc_id
        filename = file.file_name
        value = 2147483648
        used_ = find_one(message.from_user.id)
        used = used_["used_limit"]
        limit = used_["uploadlimit"]
        expi = daily - \
            int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
        if expi != 0:
            today = date_.today()
            pattern = '%Y-%m-%d'
            epcho = int(time.mktime(time.strptime(str(today), pattern)))
            daily_(message.from_user.id, epcho)
            used_limit(message.from_user.id, 0)
        remain = limit - used
        if remain < int(file.file_size):
            await message.reply_text(f"Sorry! I can't upload files that are larger than {humanbytes(limit)}. File size detected {humanbytes(file.file_size)}\nUsed Daly Limit {humanbytes(used)} If U Want to Rename Large File Upgrade Your Plan ", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Upgrade 💰💳 ",callback_data= "upgrade") ]]))
            return
        if value < file.file_size:
            if Config.STRING:
                if buy_date == None:
                    await message.reply_text(f" You Can't Upload More Then {humanbytes(limit)} Used Daly Limit {humanbytes(used)} ", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Upgrade 💰💳 ",callback_data= "upgrade") ]]))
                    return
                pre_check = check_expi(buy_date)
                if pre_check == True:
                    await message.reply_text(f"""__What do you want me to do with this file?__\n**File Name** :- {filename}\n**File Size** :- {humanize.naturalsize(file.file_size)}\n**Dc ID** :- {dcid}""", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝 Rename" ,callback_data= "rename") ,InlineKeyboardButton("✖️ Cancel" ,callback_data="cancel") ]]))
                    total_rename(int(botid), prrename)
                    total_size(int(botid), prsize, file.file_size)
                else:
                    uploadlimit(message.from_user.id, 2147483648)
                    usertype(message.from_user.id, "Free")

                    await message.reply_text(f'Your Plane Expired On {buy_date}', quote=True)
                    return
            else:
                await message.reply_text("Can't upload files bigger than 2GB ")
                return
        else:
            if buy_date:
                pre_check = check_expi(buy_date)
                if pre_check == False:
                    uploadlimit(message.from_user.id, 2147483648)
                    usertype(message.from_user.id, "Free")

            filesize = humanize.naturalsize(file.file_size)
            fileid = file.file_id
            total_rename(int(botid), prrename)
            total_size(int(botid), prsize, file.file_size)
            await message.reply_text(f"""__What do you want me to do with this file?__\n**File Name** :- {filename}\n**File Size** :- {filesize}\n**Dc ID** :- {dcid}""", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📝 Rename" ,callback_data= "rename"),
                  InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]]))
