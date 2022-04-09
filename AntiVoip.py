from pyrogram import *
from pyrogram.types import *

api_id = 9
api_hash = " "
antivoip_token = " " # token del bot

antivoip = Client('antivoip', api_id, api_hash, bot_token=antivoip_token)

@antivoip.on_message(filters.private & filters.command("start"))
async def start(client, message):
    await message.reply_text(f"{message.from_user.mention} ciao sono un antivoip completo", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("👨🏻‍💻 DEVELOPER 👨🏻‍💻", url="t.me/ChillatoDev")]
    ]))

@antivoip.on_message(filters.new_chat_members)
async def aggiunta_antivoip(client, message):
    for user in message.new_chat_members:
        if user.is_self:
            await message.reply_text("ciao grazie per avermi aggiunto") # messaggio aggiunta bot
        else:
            try:
                await client.get_chat_member(message.from_user.id)
            except:
                utentevoip = await client.get_users(message.from_user.id)
                if not utentevoip.dc_id == None and not utentevoip.dc_id == 4:
                    await client.ban_chat_member(message.chat.id, message.from_user.id)
                    await message.reply(f"{utentevoip.mention} è risultato voip")
                elif utentevoip.dc_id == None:
                    await client.restrict_chat_member(message.chat.id, message.from_user.id, ChatPermissions(can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False))
                    await message.reply_text(f"{utentevoip.mention} non hai un immagine profile impostala e premi fatto!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ FATTO ✅", "fatto_"+str(message.from_user.id))]]))
                elif utentevoip.dc_id == 4:
                    await message.reply_text(f"{utentevoip.mention} non è un voip")


@antivoip.on_callback_query()
async def bottoni(client, query):
    if query.data.startswith("fatto"):
        if query.data.split("_")[1] == str(query.from_user.id):
            queryvoip = await client.get_users(query.from_user.id)
            if queryvoip.dc_id == 4:
                await client.restrict_chat_member(query.message.chat.id, query.from_user.id, ChatPermissions(can_send_messages=True))
                await query.message.delete()
            elif not queryvoip.dc_id == None and not queryvoip.dc_id == 4:
                await client.ban_chat_member(query.message.chat.id, query.from_user.id)
                await query.message.edit(f"{queryvoip.mention} è risultato voip")
            elif queryvoip.dc_id == None:
                await query.answer("imposta un immagine!", show_alert=True)

antivoip.run()
