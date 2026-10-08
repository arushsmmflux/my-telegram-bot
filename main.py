import os
import logging
import telebot

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

log = logging.getLogger(__name__)


# =========================================================
# BOT
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = telebot.TeleBot(
    BOT_TOKEN,
    parse_mode="HTML"
)


# =========================================================
# SUPPORT
# =========================================================

SUPPORT_LINK = "https://t.me/xylerigcc"


# =========================================================
# WELCOME IMAGE
# =========================================================
# Yahan WELCOME IMAGE ka Telegram FILE ID paste karna.
#
# Example:
# WELCOME_IMAGE = "AgACAgUAAxkBAA..."
#
# Agar empty rahega to bot text bhej dega.

WELCOME_IMAGE = "https://ibb.co/RGL77cpn"


# =========================================================
# FIRST START IMAGE
# =========================================================
# Start karte hi jo image Free / Paid buttons ke upar aayegi.
#
# Agar same image welcome ke liye use karni hai:
# START_IMAGE = WELCOME_IMAGE

START_IMAGE = "https://ibb.co/GhbLV5P"


# =========================================================
# 10 PLANS
# =========================================================

PLANS = [

    {
        "id": 1,
        "name": "𝙈𝙊𝙈 𝘼𝙉𝘿 𝙎𝙊𝙉 😍🔥 (",
        "price": "49",
        "validity": "180 days",
        "videos": "30000+",

        "image": "https://ibb.co/ZRqKVvRQ",
        "qr": "https://ibb.co/fYsgpT3c",

        "demos": [
            {
                "type": "video",
                "id": "BAACAgEAAxkBAAI1uGrHdxiONKpbmlGTyHvowkY5-NOdAAJfBwACm3pBRmnwsGVg3oC1PQQ"
            },
            {
                "type": "video",
                "id": "BAACAgUAAxkBAAI1xGrHePSoNqz0ihnWsfoS2vAlvMXcAAKZIgACv69BVti1ZKjCOw6kPQQ"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_1_DEMO_3_FILE_ID"
            },
            {
                "type": "video",
                "id": "BAACAgUAAxkBAAI2CGrHe3CKZ5ubBvyZTYja35r4DZR8AAKrIgACv69BVlVqtX_Uox0XPQQ"
            },
             {
                "type": "video",
                "id": "BAACAgUAAxkBAAI1z2rHeY3vQOBvAv7RX8Cl3XXG4A01AAKcIgACv69BViaOBb0l2p0NPQQ"
            },
             {
                "type": "video",
                "id": "PASTE_PLAN_1_DEMO_3_FILE_ID"
            },
            {
                "type": "video",
                "id": "BAACAgUAAxkBAAI1y2rHeVx-RkIlGJNKCZw97WDxcuCdAAKaIgACv69BVsbbPDC2Ob_VPQQ"
            }
        ],

        "caption": "PLAN 1 CAPTION",
        "active": True
    },


    {
        "id": 2,
        "name": "𝙍!@𝙋𝙀 𝙑𝙄𝘿𝙀𝙊𝙎 💦👀",
        "price": "69",
        "validity": "180 days",
        "videos": "30000+",

        "image": "https://ibb.co/gbLMg58r",
        "qr": "https://ibb.co/gbLMg58r",

        "demos": [
            {"type": "video", "id": "BAACAgUAAxkBAAI1NGrHXS2WDGTyJId8vRH4d1LU-PlRAAJRIgACv69BVtr0Es6j5DDTPQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI2gWrHiNUQIt0CvCi0dnJGr7seR0I5AAL7IgACv69BVvEdzgSGOYZBPQQ"},
            {"type": "video", "id": "PASTE_PLAN_2_DEMO_3_FILE_ID"},
             {"type": "video", "id": "BAACAgUAAxkBAAI2iWrHiO6fqiYP4xolqkpuX0ZMsS0dAAL9IgACv69BVpy5j6D2cEt6PQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI2jWrHiPZS0lcDuVtCfsflk6BR6TUQAAL-IgACv69BVpWSGbnrEPxWPQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI2hWrHiOJLaQ20bd0ZQccYSGi1DGuDAAL8IgACv69BVn0nBQ-OdSg0PQQ"}
        ],

        "caption": "PLAN 2 CAPTION",
        "active": True
    },


    {
        "id": 3,
        "name": "𝘾𝙃𝙄!𝙇𝘿 𝙑𝙄𝘿!𝙀𝙊 ( 𝘾.𝙋) 🔥👀",
        "price": "49",
        "validity": "180 days",
        "videos": "30000+",

        "image": "https://ibb.co/fYsgpT3c",
        "qr": "PASTE_PLAN_3_QR_HERE",

        "demos": [
            {"type": "video", "id": "BAACAgUAAxkBAAI102rHeZi-bZlCOVmo9Ii4N1CXKMdGAAKdIgACv69BVpPMgg4dHNouPQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI132rHeiQH7V8Xda4tsZ4OXbHSXU2XAAKhIgACv69BVg9-lRdTEe6RPQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI16GrHejbZ4SxzgTWqpGk7Ysz5ZCKhAAKiIgACv69BVrbHAbnH-B1APQQ"},
            {"type": "video", "id": "PASTE_PLAN_3_DEMO_4_FILE_ID"},
             {"type": "video", "id": "BAACAgUAAxkBAAI17GrHekGkiNKYiHfMd_54l1h4_d80AAKjIgACv69BVtazVYarbN0sPQQ"},
             {"type": "video", "id": "PASTE_PLAN_3_DEMO_4_FILE_ID"},
             {"type": "video", "id": "BAACAgUAAxkBAAI18GrHekz_R4t2R4dzv5xikrFHAjE4AAKkIgACv69BVoNd8Uyq6RNMPQQ"},
             {"type": "video", "id": "BAACAgUAAxkBAAI19GrHelmwMFLeHgABj6xXslCrL2EgPQACpSIAAr-vQVZdvb1db57WjT0E"},
            {"type": "video", "id": "BAACAgUAAxkBAAI112rHehWT7ChqF4hbypfAEwmyF9BkAAKeIgACv69BVtXBJ3Uu9oPEPQQ"}
        ],

        "caption": "PLAN 3 CAPTION",
        "active": True
    },


    {
        "id": 4,
        "name": "𝘽𝙃𝘼𝘽𝙃𝙄 𝙑𝙄𝘿𝙀𝙊𝙎  💦👅 ",
        "price": "39",
        "validity": "180 days",
        "videos": "30000+",

        "image": "https://ibb.co/4n9q8mK2",
        "qr": "PASTE_PLAN_4_QR_HERE",

        "demos": [
            {"type": "video", "id": "BAACAgUAAxkBAAI2VGrHh0V0mxFFNp3VOcOb33Ml1G4MAALzIgACv69BVk4g0vpDj712PQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI2WGrHh6zMI-he32oPz4_Bg5wRpq-JAAL1IgACv69BVpTUY_voLFY_PQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI2WmrHh7KLY1uzWB5ystZmXDyl__xJAAL2IgACv69BVnbHhaDQGFm5PQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI2YWrHh8ajZjtBAe6pGjWj8gH8Do8XAAL3IgACv69BVuLRCRB7zpIBPQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI2ZWrHh8wrHURDjV3lm5-E1D-JIU-1AAL4IgACv69BVn8OuNQVbkxbPQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI2UGrHhaPSiODGYfCLDgX2vCg7rNZxAALtIgACv69BVibnUY0jw7XXPQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI2TGrHhZccYoGN9dYTBS3mJMZHjbA4AALsIgACv69BVosDunRUSBK0PQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI2fWrHiI7Nlb-qmDGWX8V5OPABhxF3AAL6IgACv69BVrDggsTSrVXBPQQ"},
            {"type": "video", "id": "PASTE_PLAN_4_DEMO_5_FILE_ID"}
        ],

        "caption": "PLAN 4 CAPTION",
        "active": True
    },


    {
        "id": 5,
        "name": "𝘽𝙃𝘼𝙄 𝘽𝙀𝙃𝘼𝙉 🔥🥵 ",
        "price": "49",
        "validity": "180 days",
        "videos": "30000+",

        "image": "https://ibb.co/fYsgpT3c",
        "qr": "PASTE_PLAN_5_QR_HERE",

        "demos": [
            {"type": "video", "id": "BAACAgUAAxkBAAI2D2rHfDIG-VI27jxnsZvofOtrGTyfAAKuIgACv69BVm1uywMJ7wpRPQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI2E2rHfDzkpAIyxQa_lRAtdlN6yT29AAKwIgACv69BVkO_UZZ-lONrPQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI2F2rHfErohmsyPAs8G3PzT51PSrpMAAKxIgACv69BVjpXV3XoC8KPPQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI2HWrHfFTFQ939rnRsRWwSQLD5RjQqAAKzIgACv69BVrrMSsutBep6PQQ"},
             {"type": "video", "id": "BAACAgUAAxkBAAI2LWrHf2JdymEiQzYPAzuN7rLmXU6LAALSIgACv69BVoCKrwF1v2vCPQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI2HWrHfFTFQ939rnRsRWwSQLD5RjQqAAKzIgACv69BVrrMSsutBep6PQQ"}
        ],

        "caption": "PLAN 5 CAPTION",
        "active": True
    },


    {
        "id": 6,
        "name": "𝗜𝗡𝗦𝗧𝗚𝗥𝗔𝗠 𝗠𝗠𝗦 𝗔𝗟𝗟 😍🔥 ",
        "price": "49",
        "validity": "180 days",
        "videos": "30000+",

        "image": "https://ibb.co/fYsgpT3c",
        "qr": "PASTE_PLAN_6_QR_HERE",

        "demos": [
            {"type": "video", "id": "BAACAgUAAxkBAAI1-GrHevTR_e2y2y3Nia8GN8aFjkQMAAKmIgACv69BVjq7X6WlNlKCPQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI1_GrHev604uRozFYP7sClRfafGVkxAAKnIgACv69BVtjbgnDvti8UPQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI2AAFqx3tSmYWUSW-Z07I43VDM8HNSzgACqSIAAr-vQVaXeLkJQr04Dz0ED"},
            {"type": "video", "id": "BAACAgUAAxkBAAI2BGrHe2Nkdn8bBxL-1uiW0e3IGq5iAAKqIgACv69BVnfq1jhpQgGgPQQ"},
            {"type": "video", "id": "PASTE_PLAN_6_DEMO_5_FILE_ID"}
        ],

        "caption": "PLAN 6 CAPTION",
        "active": True
    },


    {
        "id": 7,
        "name": "𝘽𝘼𝘼𝙋 𝘽𝙀𝙏𝙄 🔥💦 ",
        "price": "58",
        "validity": "180 days",
        "videos": "30000+",

        "image": "https://ibb.co/5X0hc5dd",
        "qr": "https://ibb.co/xK77FFDK",

        "demos": [
            {"type": "video", "id": "BAACAgUAAxkBAAI1vGrHeCGVLxyFtjqCDuc0jk7iB55TAAKWIgACv69BVmJlJgxhHhkOPQQ"},
            {"type": "video", "id": "BAACAgUAAxkBAAI1v2rHeCm5-AjZoCrPiee5IOCLTqQxAAKXIgACv69BVjV55biDkaGePQQ"},
            {"type": "video", "id": "PASTE_PLAN_7_DEMO_3_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_7_DEMO_4_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_7_DEMO_5_FILE_ID"}
        ],

        "caption": "PLAN 7 CAPTION",
        "active": True
    },


    {
        "id": 8,
        "name": "𝙈𝙄𝙓 𝙂𝙍𝙊𝙐𝙋 70𝙆 𝙑𝙄𝘿𝙀𝙊𝙎 🥵",
        "price": "63",
        "validity": "180 days",
        "videos": "30000+",

        "image": "https://ibb.co/qFhKnzcH",
        "qr": "https://ibb.co/tMVzjb0D",

        "demos": [
            {
                "type": "video",
                "id": "BAACAgUAAxkBAAI2PGrHhGx2iYgllaR9-h-CS7nuCFUwAALnIgACv69BVoD11n1hlXQ2PQQ"
            },
            {
                "type": "video",
                "id": "BAACAgUAAxkBAAI2OmrHhGIsfGnOZaBjkRlku4J56E0JAALmIgACv69BVjit1DxrrZ5KPQQ"
                
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_8_DEMO_3_FILE_ID"
            }
        ],

        "caption": (
            "1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n"
            "2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n"
            "3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n"
            "4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 𝙁𝙍𝙄𝘿𝘼𝙔 ✅."
        ),

        "active": True
    },


    {
        "id": 9,
        "name": "𝙂𝙄𝙍𝙇𝙎 𝙒𝙄𝙏𝙃 𝘼𝙉!𝙈@𝙇🔥",
        "price": "49",
        "validity": "180 days",
        "videos": "30000+",

        "image": "https://ibb.co/qFhKnzcH",
        "qr": "https://ibb.co/fYsgpT3c",

        "demos": [
            {"type": "video", "id": "BAACAgUAAxkBAAI2dmrHiGdHP0LzVqL7aLAtu0dacFkfAAL5IgACv69BVgU4Hw3vXvDAPQQ"},
            {"type": "video", "id": "PASTE_PLAN_9_DEMO_2_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_9_DEMO_3_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_9_DEMO_4_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_9_DEMO_5_FILE_ID"}
        ],

        "caption": "PLAN 9 CAPTION",
        "active": True
    },


    {
        "id": 10,
        "name": "𝗔𝗟𝗟 𝗩𝗜𝗣  𝗠𝗘𝗚𝗔 𝗣𝗔𝗖𝗞 🔥 ",
        "price": "169",
        "validity": "180 days",
        "videos": "30000+",

        "image": "https://ibb.co/84598K8j",
        "qr": "https://ibb.co/MDWVSzF8",

        ],

        "caption": "PLAN 10 CAPTION",
        "active": True
    }

]


# =========================================================
# BUTTON STYLES
# =========================================================

STYLE_SERIES = [
    "danger",
    "success",
    "primary",
    "danger",
    "success",
    "primary"
]


def button(text, data=None, url=None, style=None):

    kwargs = {
        "text": text
    }

    if data is not None:
        kwargs["callback_data"] = data

    if url is not None:
        kwargs["url"] = url

    if style is not None:
        kwargs["style"] = style

    return InlineKeyboardButton(**kwargs)


def add_styled(
    kb,
    text,
    data=None,
    url=None,
    index=0
):

    style = STYLE_SERIES[
        index % len(STYLE_SERIES)
    ]

    kb.add(
        button(
            text,
            data=data,
            url=url,
            style=style
        )
    )


# =========================================================
# PLAN HELPER
# =========================================================

def get_plan(pid):

    for plan in PLANS:

        if (
            plan["id"] == pid
            and plan.get("active")
        ):
            return plan

    return None


# =========================================================
# MEDIA SENDER
# =========================================================

def send_photo_or_text(
    chat_id,
    image,
    caption,
    reply_markup=None
):

    if not image:
        bot.send_message(
            chat_id,
            caption,
            reply_markup=reply_markup
        )
        return

    try:

        bot.send_photo(
            chat_id,
            image,
            caption=caption,
            reply_markup=reply_markup
        )

    except Exception:

        log.exception(
            "Could not send configured image"
        )

        bot.send_message(
            chat_id,
            caption,
            reply_markup=reply_markup
        )


# =========================================================
# START SCREEN
# =========================================================

START_CAPTION = (
  " 𝘽𝙚𝙛𝙤𝙧𝙚 𝙘𝙤𝙣𝙩𝙞𝙣𝙪𝙞𝙣𝙜, 𝙥𝙡𝙚𝙖𝙨𝙚 𝙘𝙤𝙣𝙛𝙞𝙧𝙢 𝙮𝙤𝙪 𝙖𝙧𝙚 18 𝙤𝙧 𝙤𝙡𝙙𝙚𝙧."
)


def send_start_screen(chat_id):

    kb = InlineKeyboardMarkup()

    kb.row(
        button(
            " 𝙔𝙀𝙎 𝙄 𝘼𝙈 18+ ✅",
            data="free",
            style="success"
        ),
        button(
            "𝙄 𝘼𝙈 𝙉𝙊𝙏 18+ ❌",
            data="paid",
            style="danger"
        )
    )

    send_photo_or_text(
        chat_id,
        START_IMAGE,
        START_CAPTION,
        kb
    )


# =========================================================
# PAID SCREEN
# =========================================================

def send_paid_screen(chat_id):

    kb = InlineKeyboardMarkup()

    add_styled(
        kb,
        "🔙 𝘽𝘼𝘾𝙆",
        data="start",
        index=2
    )

    bot.send_message(
        chat_id,
        " <b>𝙏𝙃𝙄𝙎 𝘽𝙊𝙏 𝙄𝙎 𝙊𝙉𝙇𝙔 𝙁𝙊𝙍 18+ 𝙐𝙎𝙀𝙍𝙎‼️</b>\n\n",
        reply_markup=kb
    )


# =========================================================
# WELCOME / FREE HOME
# =========================================================

WELCOME_CAPTION = (
   "<b> 𝙃𝙀𝙔 👋🏻, 𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 𝙤𝙪𝙧 𝙫𝙞𝙥 𝙗𝙤𝙩  😍</b> \n\n"
"𝙏𝙃𝙄𝙎 𝘽𝙊𝙏 𝘾𝙊𝙉𝘼𝙏𝘼𝙄𝙉 𝙁𝙊𝙇𝙇𝙊𝙒𝙄𝙉𝙂 𝙋𝙇𝘼𝙉𝙎 ✅\n" 
"𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂 𝙋𝙍𝙄𝘾𝙀 𝙄𝙎 𝙅𝙐𝙎𝙏 ₹39 ‼️\n\n"
"| 🔥𝘾𝙃𝙄!𝙇𝘿 𝙑𝙄𝘿𝙀𝙊𝙎 ( 𝘾𝙋 ) ( 𝘾𝙃𝙊𝙏𝙀 𝘽𝘼𝘾𝘾𝙃𝙀 ) \n" 
"| 🔥𝘽𝙃𝘼𝘽𝙃𝙄 𝙑𝙄𝘿𝙀0𝙎 \n" 
"| 🔥𝙈0𝙈 𝘼𝙉𝘿 𝙎𝙊#𝙉 \n" 
"| 🔥𝙍!@𝙋𝙀 𝙑𝙄𝘿𝙀0𝙎\n" 
"| 🔥𝘽𝘼#𝙋 𝘽𝙀𝙏𝙄 \n" 
"| 🔥𝗜𝗡𝗦𝗧𝗚𝗥𝗔𝗠 𝗠𝗠#𝗦 𝗔𝗟𝗟 \n"  
"| 🔥𝙂𝙄𝙍𝙇𝙎 𝙒𝙄𝙏𝙃 𝘼𝙉𝙄𝙈!𝘼𝙇 \n" 
"| 🔥 𝙈𝙄𝙓 𝙂𝙍𝙊𝙐𝙋 70𝙆 𝙑𝙄𝘿𝙀𝙊 \n" 
"| 🔥𝘽𝙃𝘼𝙄 𝘽𝙀𝙃𝘼𝙉 \n" 
"| 🔥𝗔𝗟𝗟 𝗩𝗜𝗣  𝗠𝗘𝗚𝗔 𝗣𝗔𝗖𝗞 \n\n"
"𝘽𝙀𝙉𝙄𝙁𝙄𝙏𝙎 𝙊𝙁 𝙊𝙐𝙍 𝘽𝙊𝙏 ✅ \n" 
"1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙑𝙄𝘿𝙀𝙊𝙎 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅ \n" 
"2. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝘿𝙊𝙒𝙉𝙇𝙊𝘼𝘿 𝙁𝙍𝙀𝙀 ✅ \n" 
"3. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ✅ \n" 
"4. 𝘿𝙄𝙍𝙀𝘾𝙏 𝙒𝘼𝙏𝘾𝙃 𝙑𝙄𝘿𝙀𝙊𝙎 ✅ \n" 
"<b>𝙏𝙊 𝘽𝙐𝙔 𝙋𝙇𝘼𝙉𝙎 𝘾𝙃𝙀𝘾𝙇 𝘽𝙐𝙏𝙏𝙊𝙉𝙎 𝘽𝙀𝙇𝙊𝙒 𝘼𝙉𝘿 𝘾𝙃𝙀𝘾𝙆 𝘿𝙀𝙈𝙊 𝘼𝙇𝙎𝙊</b> 😍🔥"
)


def send_home(chat_id):

    kb = InlineKeyboardMarkup()

    active_plans = [
        p for p in PLANS
        if p.get("active")
    ]

    for i, p in enumerate(active_plans):

        add_styled(
            kb,
            f" {p['name']} · ₹{p['price']}",
            data=f"plan:{p['id']}",
            index=i
        )

    add_styled(
        kb,
        "🎬 𝘿𝙀𝙈𝙊",
        data="demo_menu",
        index=0
    )

    add_styled(
        kb,
        " 𝙎𝙐𝙋𝙋𝙊𝙍𝙏📞",
        url=SUPPORT_LINK,
        index=1
    )

    send_photo_or_text(
        chat_id,
        WELCOME_IMAGE,
        WELCOME_CAPTION,
        kb
    )


# =========================================================
# DEMO PLAN SELECTOR
# =========================================================

def send_demo_menu(chat_id):

    kb = InlineKeyboardMarkup()

    bot.send_message(
        chat_id,
        "🎬 <b>𝘿𝙀𝙈𝙊</b>\n\n"
        "𝘿𝙚𝙢𝙤 𝙙𝙚𝙠𝙝𝙣𝙚 𝙠𝙚 𝙡𝙞𝙮𝙚 "
        "𝙠𝙤𝙞 𝙥𝙡𝙖𝙣 𝙨𝙚𝙡𝙚𝙘𝙩 𝙠𝙖𝙧𝙤.\n\n"
        "👇 <b>𝙎𝙚𝙡𝙚𝙘𝙩 𝙖 𝙥𝙡𝙖𝙣:</b>"
    )

    active_plans = [
        p for p in PLANS
        if p.get("active")
    ]

    for i, p in enumerate(active_plans):

        add_styled(
            kb,
            f"🎬 {p['name']}",
            data=f"demo_plan:{p['id']}",
            index=i
        )

    add_styled(
        kb,
        "🔙 𝘽𝘼𝘾𝙆",
        data="home",
        index=2
    )

    bot.send_message(
        chat_id,
        "👇 <b>𝘾𝙝𝙤𝙤𝙨𝙚 𝙥𝙡𝙖𝙣:</b>",
        reply_markup=kb
    )


# =========================================================
# PLAN DETAILS
# =========================================================

def send_plan(chat_id, plan):

    caption = (
        f"📦 <b>𝙋𝙡𝙖𝙣:</b> {plan['name']}\n\n"
        f"💰 <b>𝙋𝙧𝙞𝙘𝙚:</b> ₹{plan['price']}\n"
        f"⏳ <b>𝙑𝙖𝙡𝙞𝙙𝙞𝙩𝙮:</b> {plan['validity']}\n"
        f"🎬 <b>𝙑𝙞𝙙𝙚𝙤𝙨:</b> {plan['videos']}\n\n"
        f"{plan['caption']}"
    )

    kb = InlineKeyboardMarkup()

    kb.row(
        button(
            " 𝘽𝙐𝙔 𝙉𝙊𝙒 💳",
            data=f"buy:{plan['id']}",
            style="danger"
        )
    )

    kb.row(
        button(
            " 𝘿𝙀𝙈𝙊 🎬",
            data=f"demo_plan:{plan['id']}",
            style="success"
        )
    )

    kb.row(
        button(
            " 𝘽𝘼𝘾𝙆",
            data="home",
            style="primary"
        )
    )

    send_photo_or_text(
        chat_id,
        plan.get('image', ''),
        caption,
        kb
    )

# =========================================================
# DEMO STATE
# =========================================================
#
# demo_sessions[user_id] = {
#     "plan_id": 1,
#     "index": 0,
#     "message_id": 123
# }

demo_sessions = {}


# =========================================================
# SEND ONE DEMO
# =========================================================
def send_demo(
    chat_id,
    user_id,
    plan_id,
    index,
    delete_message_id=None
):

    plan = get_plan(plan_id)

    if not plan:
        bot.send_message(
            chat_id,
            "❌ 𝙋𝙡𝙖𝙣 𝙣𝙤𝙩 𝙛𝙤𝙪𝙣𝙙."
        )
        return

    demos = plan.get("demos", [])

    # Remove empty placeholder demos
    demos = [
        d for d in demos
        if d.get("id")
        and not str(d["id"]).startswith("PASTE_")
    ]

    # All demos finished
    if index >= len(demos):

        send_demo_over(
            chat_id,
            plan_id
        )

        return

    # Delete previous demo
    if delete_message_id:

        try:
            bot.delete_message(
                chat_id,
                delete_message_id
            )

        except Exception:
            log.exception(
                "Could not delete previous demo"
            )

    demo = demos[index]

    demo_type = demo.get("type")
    file_id = demo.get("id")

    kb = InlineKeyboardMarkup()

    # Always show NEXT DEMO
    kb.add(
        button(
            " 𝙉𝙀𝙓𝙏 𝘿𝙀𝙈𝙊 ➡️",
            data=f"next_demo:{plan_id}:{index}",
            style="primary"
        )
    )

    # Back to plan
    kb.add(
        button(
            " 𝘽𝘼𝘾𝙆 𝙏𝙊 𝙋𝙇𝘼𝙉",
            data=f"plan:{plan_id}",
            style="success"
        )
    )

    try:

        if demo_type == "video":

            sent = bot.send_video(
                chat_id,
                file_id,
                caption=(
                    f"🎬 <b>{plan['name']}</b>\n"
                    f"𝘿𝙚𝙢𝙤 {index + 1}/{len(demos)}"
                ),
                reply_markup=kb
            )

        elif demo_type == "photo":

            sent = bot.send_photo(
                chat_id,
                file_id,
                caption=(
                    f"📸 <b>{plan['name']}</b>\n"
                    f"𝘿𝙚𝙢𝙤 {index + 1}/{len(demos)}"
                ),
                reply_markup=kb
            )

        else:

            sent = bot.send_document(
                chat_id,
                file_id,
                caption=(
                    f"📁 <b>{plan['name']}</b>\n"
                    f"𝘿𝙚𝙢𝙤 {index + 1}/{len(demos)}"
                ),
                reply_markup=kb
            )

        demo_sessions[user_id] = {
            "plan_id": plan_id,
            "index": index,
            "message_id": sent.message_id
        }

    except Exception:

        log.exception(
            "Could not send demo"
        )

        bot.send_message(
            chat_id,
            "❌ 𝘿𝙚𝙢𝙤 𝙛𝙞𝙡𝙚 𝙨𝙚𝙩𝙩𝙞𝙣𝙜 𝙢𝙚𝙞𝙣 𝙞𝙨𝙨𝙪𝙚 𝙝𝙖𝙞."
        )
# =========================================================
# DEMO OVER
# =========================================================

def send_demo_over(chat_id, plan_id):

    kb = InlineKeyboardMarkup()

    kb.row(
        button(
            " 𝘽𝙐𝙔 𝙋𝘼𝘾𝙆 💳",
            data=f"buy:{plan_id}",
            style="danger"
        )
    )

    kb.row(
        button(
            " 𝘽𝘼𝘾𝙆 𝙏𝙊 𝙋𝙇𝘼𝙉",
            data=f"plan:{plan_id}",
            style="primary"
        )
    )

    bot.send_message(
        chat_id,
        "🚫 <b>𝘿𝙀𝙈𝙊 𝙊𝙑𝙀𝙍</b>\n\n"
        "💎 <b>𝙋𝙇𝙀𝘼𝙎𝙀 𝙋𝙐𝙍𝘾𝙃𝘼𝙎𝙀 𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝙋𝙇𝘼𝙉</b>",
        reply_markup=kb
    )

# =========================================================
# PAYMENT
# =========================================================

def send_payment(chat_id, user_id, plan):

    qr = plan.get("qr", "")

    if not qr:

        bot.send_message(
            chat_id,
            "⚠️ 𝙋𝙖𝙮𝙢𝙚𝙣𝙩 𝙌𝙍 𝙞𝙨 𝙣𝙤𝙩 𝙨𝙚𝙩 𝙮𝙚𝙩."
        )

        return

    kb = InlineKeyboardMarkup()

    kb.row(
        button(
            " 𝙄 𝙋𝘼𝙄𝘿",
            data=f"paid:{plan['id']}",
            style="success"
        ),
        button(
            " 𝘽𝘼𝘾𝙆",
            data=f"plan:{plan['id']}",
            style="primary"
        )
    )

    caption = (
        f" <b>𝙋𝘼𝙔𝙈𝙀𝙉𝙏 𝙋𝘼𝙂𝙀 💳: ₹{plan['price']}</b>\n\n"
        "1️⃣ 𝙎𝙘𝙖𝙣 𝙩𝙝𝙚 𝙌𝙍.\n"
        "2️⃣ 𝙋𝙖𝙮 𝙩𝙝𝙚 𝙚𝙭𝙖𝙘𝙩 𝙖𝙢𝙤𝙪𝙣𝙩.\n"
        "3️⃣ 𝘾𝙡𝙞𝙘𝙠 <b>𝙄 𝙋𝘼𝙄𝘿✅</b>.\n"
        "4️⃣ 𝙎𝙚𝙣𝙙 𝙥𝙖𝙮𝙢𝙚𝙣𝙩 𝙨𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩.✅"
    )

    send_photo_or_text(
        chat_id,
        qr,
        caption,
        kb
    )


# =========================================================
# SCREENSHOT STATE
# =========================================================

waiting_screenshot = {}
pending_orders = {}


# =========================================================
# START COMMAND
# =========================================================

@bot.message_handler(commands=["start"])
def start(message):

    send_start_screen(
        message.chat.id
    )


# =========================================================
# FREE
# =========================================================

@bot.callback_query_handler(
    func=lambda call: call.data == "free"
)
def free_button(call):

    bot.answer_callback_query(call.id)

    send_home(
        call.message.chat.id
    )


# =========================================================
# PAID
# =========================================================

@bot.callback_query_handler(
    func=lambda call: call.data == "paid"
)
def paid_button(call):

    bot.answer_callback_query(call.id)

    send_paid_screen(
        call.message.chat.id
    )


# =========================================================
# START BACK
# =========================================================

@bot.callback_query_handler(
    func=lambda call: call.data == "start"
)
def start_back(call):

    bot.answer_callback_query(call.id)

    send_start_screen(
        call.message.chat.id
    )


# =========================================================
# HOME
# =========================================================

@bot.callback_query_handler(
    func=lambda call: call.data == "home"
)
def home_button(call):

    bot.answer_callback_query(call.id)

    send_home(
        call.message.chat.id
    )


# =========================================================
# DEMO MENU
# =========================================================

@bot.callback_query_handler(
    func=lambda call: call.data == "demo_menu"
)
def demo_button(call):

    bot.answer_callback_query(call.id)

    send_demo_menu(
        call.message.chat.id
    )


# =========================================================
# PLAN
# =========================================================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("plan:")
)
def plan_button(call):

    bot.answer_callback_query(call.id)

    try:

        plan_id = int(
            call.data.split(":")[1]
        )

    except Exception:

        return

    plan = get_plan(plan_id)

    if not plan:
        return

    send_plan(
        call.message.chat.id,
        plan
    )


# =========================================================
# DEMO PLAN SELECT
# =========================================================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("demo_plan:")
)
def demo_plan_button(call):

    bot.answer_callback_query(call.id)

    try:

        plan_id = int(
            call.data.split(":")[1]
        )

    except Exception:

        return

    plan = get_plan(plan_id)

    if not plan:
        return

    # Start from demo 1
    send_demo(
        call.message.chat.id,
        call.from_user.id,
        plan_id,
        0
    )


# =========================================================
# NEXT DEMO
# =========================================================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("next_demo:")
)
def next_demo_button(call):

    bot.answer_callback_query(call.id)

    try:

        parts = call.data.split(":")

        plan_id = int(parts[1])
        current_index = int(parts[2])

    except Exception:

        return

    session = demo_sessions.get(
        call.from_user.id
    )

    old_message_id = None

    if session:

        old_message_id = session.get(
            "message_id"
        )

    # Next demo
    send_demo(
        call.message.chat.id,
        call.from_user.id,
        plan_id,
        current_index + 1,
        delete_message_id=old_message_id
    )


# =========================================================
# DEMO OVER
# =========================================================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("demo_over:")
)
def demo_over_button(call):

    bot.answer_callback_query(call.id)

    try:

        plan_id = int(
            call.data.split(":")[1]
        )

    except Exception:

        return

    session = demo_sessions.pop(
        call.from_user.id,
        None
    )

    if session:

        try:

            bot.delete_message(
                call.message.chat.id,
                session["message_id"]
            )

        except Exception:

            pass

    send_demo_over(
        call.message.chat.id,
        plan_id
    )


# =========================================================
# BUY
# =========================================================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("buy:")
)
def buy_button(call):

    bot.answer_callback_query(call.id)

    try:

        plan_id = int(
            call.data.split(":")[1]
        )

    except Exception:

        return

    plan = get_plan(plan_id)

    if not plan:
        return

    send_payment(
        call.message.chat.id,
        call.from_user.id,
        plan
    )


# =========================================================
# PAID
# =========================================================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("paid:")
)
def paid_confirm(call):

    bot.answer_callback_query(call.id)

    try:

        plan_id = int(
            call.data.split(":")[1]
        )

    except Exception:

        return

    plan = get_plan(plan_id)

    if not plan:
        return

    uid = call.from_user.id

    waiting_screenshot.add(uid)

    pending_orders[uid] = {
        "plan_id": plan_id
    }

    bot.send_message(
        call.message.chat.id,
        "📸 <b>𝙋𝙖𝙮𝙢𝙚𝙣𝙩 𝙨𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩 𝙨𝙚𝙣𝙙 𝙠𝙖𝙧𝙤.</b>"
    )


# =========================================================
# SCREENSHOT HANDLER
# =========================================================

@bot.message_handler(
    content_types=["photo"]
)
def screenshot_handler(message):

    uid = message.from_user.id

    if uid not in waiting_screenshot:
        return

    order = pending_orders.get(uid)

    if not order:
        return

    plan = get_plan(
        order["plan_id"]
    )

    if not plan:
        return

    screenshot_id = (
        message.photo[-1].file_id
    )

    waiting_screenshot.discard(uid)

    try:

        bot.send_photo(
            ADMIN_ID,
            screenshot_id,
            caption=(
                "💳 <b>𝙉𝙀𝙒 𝙋𝘼𝙔𝙈𝙀𝙉𝙏</b>\n\n"
                f"👤 User ID: <code>{uid}</code>\n"
                f"📦 Plan: {plan['name']}\n"
                f"💰 Amount: ₹{plan['price']}"
            )
        )

        bot.reply_to(
            message,
            "✅ <b>𝙎𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩 𝙨𝙚𝙣𝙩.</b>\n"
            "𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩 𝙛𝙤𝙧 𝙖𝙥𝙥𝙧𝙤𝙫𝙖𝙡."
        )

    except Exception:

        log.exception(
            "Could not send payment screenshot"
        )

        bot.reply_to(
            message,
            "❌ 𝙎𝙤𝙢𝙚𝙩𝙝𝙞𝙣𝙜 𝙬𝙚𝙣𝙩 𝙬𝙧𝙤𝙣𝙜."
        )


# =========================================================
# ADMIN MEDIA ID MODE
# =========================================================
#
# IMPORTANT:
# Ab photo/video bhejne par ID automatically nahi milegi
# jab tak admin /getid command na kare.
#
# Admin:
# /getid
#
# Bot:
# Send photo/video/document
#
# Phir bot exact FILE ID reply karega.
#

admin_waiting_media_id = set()


@bot.message_handler(
    commands=["getid"]
)
def getid_command(message):

    if message.from_user.id != ADMIN_ID:

        bot.reply_to(
            message,
            "❌ Not allowed."
        )

        return

    admin_waiting_media_id.add(
        message.from_user.id
    )

    bot.reply_to(
        message,
        "📸 <b>𝙎𝙚𝙣𝙙 𝙥𝙝𝙤𝙩𝙤, 𝙫𝙞𝙙𝙚𝙤 𝙤𝙧 𝙙𝙤𝙘𝙪𝙢𝙚𝙣𝙩 𝙣𝙤𝙬.</b>\n\n"
        "𝙄 𝙬𝙞𝙡𝙡 𝙧𝙚𝙥𝙡𝙮 𝙬𝙞𝙩𝙝 𝙩𝙝𝙚 𝙁𝙞𝙡𝙚 𝙄𝘿."
    )


# =========================================================
# ADMIN PHOTO ID
# =========================================================

@bot.message_handler(
    content_types=["photo"]
)
def admin_photo_id(message):

    uid = message.from_user.id

    if uid != ADMIN_ID:
        return

    if uid not in admin_waiting_media_id:
        return

    file_id = message.photo[-1].file_id

    admin_waiting_media_id.discard(uid)

    bot.reply_to(
        message,
        "📸 <b>PHOTO FILE ID:</b>\n\n"
        f"<code>{file_id}</code>"
    )


# =========================================================
# ADMIN VIDEO ID
# =========================================================

@bot.message_handler(
    content_types=["video"]
)
def admin_video_id(message):

    uid = message.from_user.id

    if uid != ADMIN_ID:
        return

    if uid not in admin_waiting_media_id:
        return

    file_id = message.video.file_id

    admin_waiting_media_id.discard(uid)

    bot.reply_to(
        message,
        "🎬 <b>VIDEO FILE ID:</b>\n\n"
        f"<code>{file_id}</code>"
    )


# =========================================================
# ADMIN DOCUMENT ID
# =========================================================

@bot.message_handler(
    content_types=["document"]
)
def admin_document_id(message):

    uid = message.from_user.id

    if uid != ADMIN_ID:
        return

    if uid not in admin_waiting_media_id:
        return

    file_id = message.document.file_id

    admin_waiting_media_id.discard(uid)

    bot.reply_to(
        message,
        "📁 <b>DOCUMENT FILE ID:</b>\n\n"
        f"<code>{file_id}</code>"
    )


# =========================================================
# ADMIN ONLY - /id
# =========================================================
# Optional shortcut:
# /id ke baad photo/video/document bhejo.

@bot.message_handler(
    commands=["id"]
)
def id_command(message):

    if message.from_user.id != ADMIN_ID:

        bot.reply_to(
            message,
            "❌ Not allowed."
        )

        return

    admin_waiting_media_id.add(
        message.from_user.id
    )

    bot.reply_to(
        message,
        "📲 <b>Media bhejo.</b>\n\n"
        "𝙋𝙝𝙤𝙩𝙤 / 𝙑𝙞𝙙𝙚𝙤 / 𝘿𝙤𝙘𝙪𝙢𝙚𝙣𝙩"
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    log.info(
        "Bot started successfully."
    )

    bot.infinity_polling(
        skip_pending=True,
        timeout=30,
        long_polling_timeout=30
    )
