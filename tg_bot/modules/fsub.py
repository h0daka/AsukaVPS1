import logging
import time

from pyrogram import filters, Client
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameNotOccupied,
    UserNotParticipant,
)
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot import DRAGONS as SUDO_USERS
from tg_bot import pbot
from tg_bot.modules.sql import forceSubscribe_sql as sql


logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(
    lambda _, __, query: query.data == "onUnMuteRequest"
)


@pbot.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
    user_id = cb.from_user.id
    chat_id = cb.message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        channel = chat_db.channel
        chat_member = client.get_chat_member(chat_id, user_id)
        if chat_member.restricted_by:
            if chat_member.restricted_by.id == (client.get_me()).id:
                try:
                    client.get_chat_member(channel, user_id)
                    client.unban_chat_member(chat_id, user_id)
                    cb.message.delete()
                    # if cb.message.reply_to_message.from_user.id == user_id:
                    # cb.message.delete()
                except UserNotParticipant:
                    client.answer_callback_query(
                        cb.id,
                        text=f"Join @{channel} Channel And Press The Unmute Me Button.",
                        show_alert=True,
                    )
            else:
                client.answer_callback_query(
                    cb.id,
                    text="You Are Muted By Admins For Another Reason.",
                    show_alert=True,
                )
        else:
            if (
                not client.get_chat_member(chat_id, (client.get_me()).id).status
                == "administrator"
            ):
                client.send_message(
                    chat_id,
                    f"**{cb.from_user.mention} Is Trying To Unmute Himself But I Can Not Unmute As I Lack Admin Rights.**\n__#LeavingChat...__",
                )

            else:
                client.answer_callback_query(
                    cb.id,
                    text="Do Not Press The Unmute Button While You Can Talk.",
                    show_alert=True,
                )


@pbot.on_message(filters.text & ~filters.private, group=1)
def _check_member(client, message):
    chat_id = message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        user_id = message.from_user.id
        if (
            not client.get_chat_member(chat_id, user_id).status
            in ("administrator", "creator")
            and not user_id in SUDO_USERS
        ):
            channel = chat_db.channel
            try:
                client.get_chat_member(channel, user_id)
            except UserNotParticipant:
                try:
                    sent_message = message.reply_text(
                        "Hey {} \n **You have Not Joined @{} Channel Yet**🧐 \n \nPlease Join [This Channel](https://t.me/{}) And Press The **Unmute Me** Button. \n \n ".format(
                            message.from_user.mention, channel, channel
                        ),
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "• Channel •",
                                        url="https://t.me/{}".format(channel),
                                    )
                                ],
                                [
                                    InlineKeyboardButton(
                                        "• Unmute Me •", callback_data="onUnMuteRequest"
                                    )
                                ],
                            ]
                        ),
                    )
                    client.restrict_chat_member(
                        chat_id, user_id, ChatPermissions(can_send_messages=False)
                    )
                except ChatAdminRequired:
                    sent_message.edit(
                        "**I Am Not Admin Here...**\n__Give Me Permission To Ban Users First... \n#EndingFSub...__"
                    )

            except ChatAdminRequired:
                client.send_message(
                    chat_id,
                    text=f"**I Am Not Admin In The @{channel} Channel.**\n__Promote Me In The Channel.\n#EndingFSub...__",
                )


@pbot.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
def config(client, message):
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status == "creator" or user.user.id in SUDO_USERS:
        chat_id = message.chat.id
        if len(message.command) > 1:
            input_str = message.command[1]
            input_str = input_str.replace("@", "")
            if input_str.lower() in ("off", "no", "disable"):
                sql.disapprove(chat_id)
                message.reply_text("**Force Sub Has Been Disabled Successfully.**")
            elif input_str.lower() in ("clear"):
                sent_message = message.reply_text(
                    "**Unmuting All The Members Who Were Muted For Not Joining The Channel...**"
                )
                try:
                    for chat_member in client.get_chat_members(
                        message.chat.id, filter="restricted"
                    ):
                        if chat_member.restricted_by.id == (client.get_me()).id:
                            client.unban_chat_member(chat_id, chat_member.user.id)
                            time.sleep(1)
                    sent_message.edit("**Unmuted All The Members Who Were Muted By Me For Not Joining The Channel.**")
                except ChatAdminRequired:
                    sent_message.edit(
                        "**I Am Not an Admin In This Chat.**\n__I Can Not Unmute Members As I Lack Admin Rights.__"
                    )
            else:
                try:
                    client.get_chat_member(input_str, "me")
                    sql.add_channel(chat_id, input_str)
                    message.reply_text(
                        f"**Force Subscribe Has Been Enabled**\n__FSub Enabled, All the Group Members Have to Subscribe This [Channel](https://t.me/{input_str}) For Sending Messages In This Chat.__",
                        disable_web_page_preview=True,
                    )
                except UserNotParticipant:
                    message.reply_text(
                        f"**I Am Not an Admin In Target Channel.**\n__Promote Me As An Admin In The [Channel](https://t.me/{input_str}) To Enable Force Subscribe.__",
                        disable_web_page_preview=True,
                    )
                except (UsernameNotOccupied, PeerIdInvalid):
                    message.reply_text(f"**Invalid Channel Username.**")
                except Exception as err:
                    message.reply_text(f"**Error:** ```{err}```")
        else:
            if sql.fs_settings(chat_id):
                message.reply_text(
                    f"**Force Sub Has Been Enabled.**\n__For This [Channel](https://t.me/{sql.fs_settings(chat_id).channel})__",
                    disable_web_page_preview=True,
                )
            else:
                message.reply_text("**Force Subscribe For This Chat Is Disabled.**")
    else:
        message.reply_text(
            "**Only The Owner Of This Chat Can Enable Force Subscribe.**"
        )


__help__ = """
  *Force Subscribe:*

  Asuka can mute members who are not subscribed your channel until they subscribe When enabled I will mute unsubscribed members and show them a unmute button. When they pressed the button I will unmute them

  *Setup* *:* *Only for chat owner*
  ❍ Add me in your group as admin
  ❍ Add me in your channel as admin 
    
  *Commmands*
  ❍ /fsub {channel username} *:* To turn on and setup the channel.

    💡Do this first...

  ❍ /fsub *:* To get the current settings.
  ❍ /fsub disable *:* To turn of ForceSubscribe..

    💡If you disable fsub, you need to set again for working.. /fsub {channel username} 

  ❍ /fsub clear *:* To unmute all members who are muted by me for not joining the channel.
"""
__mod_name__ = "FSub"
