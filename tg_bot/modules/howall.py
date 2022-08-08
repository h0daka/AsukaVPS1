import random
from .. import telethn as asst
from telethon import Button, events

BUTTON = [[Button.url("❓ What Is This", "https://t.me/AsukaUpdates/22")]]
HOT = "https://telegra.ph/file/096ac399f60404f893902.mp4"
SMEXY = "https://telegra.ph/file/228d41c1d991a32475fa6.mp4"
LEZBIAN = "https://telegra.ph/file/489f5aeceabde13b04f45.mp4"
BIGBALL = "https://i.gifer.com/8ZUg.gif"
LANG = "https://telegra.ph/file/fa19e475af3682261c973.mp4"
CUTIE = "https://telegra.ph/file/8e5db4f15a249a01929a8.mp4"
DANCE = "https://telegra.ph/file/93551c52c56a168448023.mp4"

@asst.on(events.NewMessage(pattern="/horny ?(.*)"))
async def horny(e):
         user_id = e.sender.id
         user_name = e.sender.first_name
         mention = f"[{user_name}](tg://user?id={str(user_id)})"
         mm = random.randint(1,100)
         HORNY = f"**🔥** {mention} **Is** {mm}**% Horny!**"
         await e.reply(HORNY, buttons=BUTTON, file=HOT)

@asst.on(events.NewMessage(pattern="/gay ?(.*)"))
async def gay(e):
         user_id = e.sender.id
         user_name = e.sender.first_name
         mention = f"[{user_name}](tg://user?id={str(user_id)})"
         mm = random.randint(1,100)
         GAY = f"**🏳‍🌈** {mention} **Is** {mm}**% Gay!**"
         await e.reply(GAY, buttons=BUTTON, file=SMEXY)

@asst.on(events.NewMessage(pattern="/lezbian ?(.*)"))
async def lezbian(e):
         user_id = e.sender.id
         user_name = e.sender.first_name
         mention = f"[{user_name}](tg://user?id={str(user_id)})"
         mm = random.randint(1,100)
         FEK = f"**💜** {mention} **Is** {mm}**% Lezbian!**"
         await e.reply(FEK, buttons=BUTTON, file=LEZBIAN)

@asst.on(events.NewMessage(pattern="/boobs ?(.*)"))
async def boobs(e):
         user_id = e.sender.id
         user_name = e.sender.first_name
         mention = f"[{user_name}](tg://user?id={str(user_id)})"
         mm = random.randint(1,100)
         BOOBS = f"**🍒** {mention}**'s Boobs Size Is** {mm}**!**"
         await e.reply(BOOBS, buttons=BUTTON, file=BIGBALL)

@asst.on(events.NewMessage(pattern="/cock ?(.*)"))
async def cock(e):
         user_id = e.sender.id
         user_name = e.sender.first_name
         mention = f"[{user_name}](tg://user?id={str(user_id)})"
         mm = random.randint(1,100)
         COCK = f"**🍆** {mention}**'s Cock Size Is** {mm}**cm**"
         await e.reply(COCK, buttons=BUTTON, file=LANG)

@asst.on(events.NewMessage(pattern="/cute ?(.*)"))
async def cute(e):
         user_id = e.sender.id
         user_name = e.sender.first_name
         mention = f"[{user_name}](tg://user?id={str(user_id)})"
         mm = random.randint(1,100)
         CUTE = f"**🍑** {mention} {mm}**% Cute**"
         await e.reply(CUTE, buttons=BUTTON, file=CUTIE)
         
@asst.on(events.NewMessage(pattern="/dance ?(.*)"))
async def dance(e):
         await e.reply(file=DANCE)

__help__ = """
➛ /horny - Check Your Current Hornyess 
➛ /gay - Check Your Current Gayness 
➛ /lezbian - Check Your Current Lezbianess 
➛ /boobs - Check Your Current Boobs Size 
➛ /cock - Check Your Current Cock Size 
➛ /cute - Check Your Current Cuteness 

Note :- This Module Is For Fun Only
"""

__mod_name__ = "How-All"
