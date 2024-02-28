from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
from pyrogram import Client , filters

@Client.on_callback_query(filters.regex('upgrade'))
async def upgrade(bot,update):
	text = """**Free Plan User**
	Daily  Upload limit 2GB
	Price 0
	
	**VIP 1 ** 
	Daily  Upload  limit 10GB
	Price  🌎 0.67$  per Month
	
	**VIP 2 **
	Daily Upload limit 50GB
	Price  🌎 0.97$  per Month

	**VIP 3 **
	Daily Upload limit 250GB
	Price  🌎 1.44$  per Month

	
	**VIP 4 **
	Daily Upload limit 1000GB
	Price  🌎 3.97$  per Month
 
                """
	keybord = InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("ADMIN 🛂",url = "https://t.me/teegrixx")],
        			[InlineKeyboardButton("Cancel",callback_data = "cancel")  ]])
	await update.message.edit(text = text,reply_markup = keybord)
	

@Client.on_message(filters.private & filters.command(["upgrade"]))
async def upgradecm(bot,message):
	text = """**Free Plan User**
	Daily  Upload limit 2GB
	Price 0
	
	**VIP 1 ** 
	Daily  Upload  limit 10GB
	Price  🌎 0.67$  per Month
	
	**VIP 2 **
	Daily Upload limit 50GB
	Price  🌎 0.97$  per Month

	**VIP 3 **
	Daily Upload limit 250GB
	Price  🌎 1.44$  per Month

	
	**VIP 4 **
	Daily Upload limit 1000GB
	Price  🌎 3.97$  per Month
 
                """
	keybord = InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("ADMIN 🛂",url = "https://t.me/teegrixx")],
        			[InlineKeyboardButton("Cancel",callback_data = "cancel")  ]])
	await update.message.edit(text = text,reply_markup = keybord)
