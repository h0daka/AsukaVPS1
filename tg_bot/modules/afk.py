import html
import random

from telegram import Update, MessageEntity
from telegram.ext import Filters, CallbackContext
from telegram.error import BadRequest
from tg_bot.modules.sql import afk_sql as sql
from tg_bot.modules.users import get_user_id
from tg_bot.modules.helper_funcs.decorators import kigcmd, kigmsg

AFKVID = "https://telegra.ph/file/c49829f9f5d65947cbc7e.mp4"

@kigmsg(Filters.regex("(?i)^brb"), friendly="afk", group=3)
@kigcmd(command="afk", group=3)
def afk(update: Update, context: CallbackContext):
    args = update.effective_message.text.split(None, 1)
    user = update.effective_user

    if not user:  # ignore channels
        return

    if user.id in (777000, 1087968824):
        return

    notice = ""
    if len(args) >= 2:
        reason = args[1]
        if len(reason) > 100:
            reason = reason[:100]
            notice = "\nYour afk reason was shortened to 100 characters."
    else:
        reason = ""

    sql.set_afk(update.effective_user.id, reason)
    fname = update.effective_user.first_name
    try:
        update.effective_message.reply_video(
            AFKVID,caption="Byii Byii! {} {}".format(fname, notice))
    except BadRequest:
        pass

@kigmsg((Filters.all & Filters.chat_type.groups), friendly='afk', group=1)
def no_longer_afk(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.effective_message

    if not user:  # ignore channels
        return

    res = sql.rm_afk(user.id)
    if res:
        if message.new_chat_members:  # dont say msg
            return
        firstname = update.effective_user.first_name
        try:
            options = [
                "{} Came Back After Masturbating!",
                "{}, Hope You Brought Pizza For Us!",
                "My Darling {}, Is Here!",
                "{} Don't Trash The Chat!",
                "{} You're Looking Great Today!",
                "{} Where Have You Been??",
                "Welcome Back! {}",
                "Name Someone Gey??\n{} Might Be Perfect!",
            ]
            chosen_option = random.choice(options)
            update.effective_message.reply_text(
                chosen_option.format(firstname), parse_mode=None
            )
        except:
            return

@kigmsg((Filters.entity(MessageEntity.MENTION) | Filters.entity(MessageEntity.TEXT_MENTION) & Filters.chat_type.groups), friendly='afk', group=8)
def reply_afk(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    userc = update.effective_user
    userc_id = userc.id
    if message.entities and message.parse_entities(
        [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
    ):
        entities = message.parse_entities(
            [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
        )

        chk_users = []
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

            if ent.type != MessageEntity.MENTION:
                return

            user_id = get_user_id(
                message.text[ent.offset : ent.offset + ent.length]
            )
            if not user_id:
                # Should never happen, since for a user to become AFK they must have spoken. Maybe changed username?
                return

            if user_id in chk_users:
                return
            chk_users.append(user_id)

            try:
                chat = bot.get_chat(user_id)
            except BadRequest:
                print(
                    "Error: Could not fetch userid {} for AFK module".format(
                        user_id
                    )
                )
                return
            fst_name = chat.first_name

            check_afk(update, context, user_id, fst_name, userc_id)

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        fst_name = message.reply_to_message.from_user.first_name
        check_afk(update, context, user_id, fst_name, userc_id)


def check_afk(update, context, user_id, fst_name, userc_id):
    if int(userc_id) == int(user_id):
        return
    afk_D = sql.check_afk_status(user_id)
    is_afk = afk_D.is_afk 
    reason = afk_D.reason
    
    if is_afk:
        if not reason:
            res = "{} is afk".format(fst_name)
            update.effective_message.reply_text(res, parse_mode=None)
        else:
            res = "{} is afk.\nReason: <code>{}</code>".format(
                html.escape(fst_name), html.escape(reason)
            )
            update.effective_message.reply_text(res, parse_mode="html")


def __gdpr__(user_id):
    sql.rm_afk(user_id)

from tg_bot.modules.language import gs

def get_help(chat):
    return gs(chat, "afk_help")

__mod_name__ = "AFK"
