import html
import json
import random
import time
import urllib.request
import urllib.parse

import telegram
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions, ParseMode, Update)
from telegram.error import BadRequest
from telegram.ext import CallbackContext, run_async

henbuttons = [
    [
                        InlineKeyboardButton(
                             text="Uncensored Hentai",
                             url="https://t.me/Uncensored_Hemtai"),
                    ],                
                   [ 
                       InlineKeyboardButton(
                             text="Pornhwa",
                             url="https://t.me/PornhwaHeaven"),                  
                       InlineKeyboardButton(
                             text="Chat",
                             url="https://t.me/Hentai_Chat_Hanime"),
                   ],
    ]

anibuttons = [
    [
                        InlineKeyboardButton(
                             text="Anime Cruise",
                             url="https://t.me/Anime_Cruise"),
                    ],                
                   [ 
                       InlineKeyboardButton(
                             text="Index",
                             url="https://t.me/Cruise_Index"),                  
                       InlineKeyboardButton(
                             text="Chat",
                             url="https://t.me/Anime_Chat_Kaizuryu"),
                   ],
    ]

import tg_bot.modules.fun_strings as fun_strings
from tg_bot.modules.helper_funcs.chat_status import is_user_admin
from tg_bot.modules.helper_funcs.extraction import extract_user
from tg_bot.modules.helper_funcs.decorators import kigcmd


@kigcmd(command='runs')
def runs(update: Update, context: CallbackContext):
    update.effective_message.reply_text(random.choice(fun_strings.RUN_STRINGS))


@kigcmd(command='slap')
def slap(update: Update, context: CallbackContext):
    bot: telegram.Bot = context.bot
    args = context.args
    message = update.effective_message
    chat = update.effective_chat

    reply_text = (
        message.reply_to_message.reply_text
        if message.reply_to_message
        else message.reply_text
    )

    curr_user = html.escape(message.from_user.first_name) if not message.sender_chat else html.escape(
        message.sender_chat.title)
    user_id = extract_user(message, args)

    if user_id == bot.id:
        temp = random.choice(fun_strings.SLAP_Kigyō_TEMPLATES)

        if isinstance(temp, list):
            if temp[2] == "tmute":
                if is_user_admin(update, message.from_user.id):
                    reply_text(temp[1])
                    return

                mutetime = int(time.time() + 60)
                bot.restrict_chat_member(
                    chat.id,
                    message.from_user.id,
                    until_date=mutetime,
                    permissions=ChatPermissions(can_send_messages=False),
                )
            reply_text(temp[0])
        else:
            reply_text(temp)
        return

    if user_id:

        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(slapped_user.first_name if slapped_user.first_name else slapped_user.title)

    else:
        user1 = bot.first_name
        user2 = curr_user

    temp = random.choice(fun_strings.SLAP_TEMPLATES)
    item = random.choice(fun_strings.ITEMS)
    hit = random.choice(fun_strings.HIT)
    throw = random.choice(fun_strings.THROW)
    reply = temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw)

    reply_text(reply, parse_mode=ParseMode.HTML)


@kigcmd(command='pat')
def pat(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = str(update.message.text)
    try:
        msg = msg.split(" ", 1)[1]
    except IndexError:
        msg = ""
    msg_id = (
        update.effective_message.reply_to_message.message_id
        if update.effective_message.reply_to_message
        else update.effective_message.message_id
    )
    pats = []
    pats = json.loads(
        urllib.request.urlopen(
            urllib.request.Request(
                "http://headp.at/js/pats.json",
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) "
                                  "Gecko/20071127 Firefox/2.0.0.11"
                },
            )
        )
            .read()
            .decode("utf-8")
    )
    if "@" in msg and len(msg) > 5:
        context.bot.send_photo(
            chat_id,
            f"https://headp.at/pats/{urllib.parse.quote(random.choice(pats))}",
            caption=msg,
        )
    else:
        context.bot.send_photo(
            chat_id,
            f"https://headp.at/pats/{urllib.parse.quote(random.choice(pats))}",
            reply_to_message_id=msg_id,
        )


@kigcmd(command='roll')
def roll(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(range(1, 7)))


@kigcmd(command='toss')
def toss(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(fun_strings.TOSS))


@kigcmd(command='shrug')
def shrug(update: Update, context: CallbackContext):
    msg = update.effective_message
    reply_text = (
        msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    )
    reply_text(r"¯\_(ツ)_/¯")


@kigcmd(command='rlg')
def rlg(update: Update, context: CallbackContext):
    eyes = random.choice(fun_strings.EYES)
    mouth = random.choice(fun_strings.MOUTHS)
    ears = random.choice(fun_strings.EARS)

    if len(eyes) == 2:
        repl = ears[0] + eyes[0] + mouth[0] + eyes[1] + ears[1]
    else:
        repl = ears[0] + eyes[0] + mouth[0] + eyes[0] + ears[1]
    update.message.reply_text(repl)


@kigcmd(command='decide')
def decide(update: Update, context: CallbackContext):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun_strings.DECIDE))


@kigcmd(command='table')
def table(update: Update, context: CallbackContext):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun_strings.TABLE))

@kigcmd(command='sex')
def sex(update: Update, context: CallbackContext):
    reply_animation = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text
    reply_animation(random.choice(fun_strings.SEX))
    
@kigcmd(command='hemtai')
def hemtai(update: Update, context: CallbackContext):
    reply_photo = update.effective_message.reply_to_message.reply_photo if update.effective_message.reply_to_message else update.effective_message.reply_photo
    reply_photo(photo="https://telegra.ph/file/a01a331e69ab69158482e.jpg", caption=f"• Heyy Pervert!!! Join Below •", 
    reply_markup=InlineKeyboardMarkup(henbuttons),
    parse_mode=ParseMode.MARKDOWN,)

@kigcmd(command='animec')
def animec(update: Update, context: CallbackContext):
    reply_photo = update.effective_message.reply_to_message.reply_photo if update.effective_message.reply_to_message else update.effective_message.reply_photo
    reply_photo(photo="https://telegra.ph/file/6deba46d5cc608ba3a59f.jpg", 
    reply_markup=InlineKeyboardMarkup(anibuttons),
    parse_mode=ParseMode.MARKDOWN,)    
    

from tg_bot.modules.language import gs


def get_help(chat):
    return gs(chat, "fun_help")


__mod_name__ = "Fun"
