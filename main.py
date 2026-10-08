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

WELCOME_IMAGE = ""


# =========================================================
# FIRST START IMAGE
# =========================================================
# Start karte hi jo image Free / Paid buttons ke upar aayegi.
#
# Agar same image welcome ke liye use karni hai:
# START_IMAGE = WELCOME_IMAGE

START_IMAGE = ""


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

        "image": "PASTE_PLAN_1_IMAGE_HERE",
        "qr": "PASTE_PLAN_1_QR_HERE",

        "demos": [
            {
                "type": "video",
                "id": "BAACAgUAAxkBAAI06GrHM2QUeiT0Q6J5yEopeA96Aim1AAJKIwACv685VjMk0xUgmBWJPQQ"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_1_DEMO_2_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_1_DEMO_3_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_1_DEMO_4_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_1_DEMO_5_FILE_ID"
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

        "image": "PASTE_PLAN_2_IMAGE_HERE",
        "qr": "PASTE_PLAN_2_QR_HERE",

        "demos": [
            {"type": "video", "id": "PASTE_PLAN_2_DEMO_1_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_2_DEMO_2_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_2_DEMO_3_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_2_DEMO_4_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_2_DEMO_5_FILE_ID"}
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

        "image": "PASTE_PLAN_3_IMAGE_HERE",
        "qr": "PASTE_PLAN_3_QR_HERE",

        "demos": [
            {"type": "video", "id": "PASTE_PLAN_3_DEMO_1_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_3_DEMO_2_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_3_DEMO_3_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_3_DEMO_4_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_3_DEMO_5_FILE_ID"}
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

        "image": "PASTE_PLAN_4_IMAGE_HERE",
        "qr": "PASTE_PLAN_4_QR_HERE",

        "demos": [
            {"type": "video", "id": "PASTE_PLAN_4_DEMO_1_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_4_DEMO_2_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_4_DEMO_3_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_4_DEMO_4_FILE_ID"},
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

        "image": "PASTE_PLAN_5_IMAGE_HERE",
        "qr": "PASTE_PLAN_5_QR_HERE",

        "demos": [
            {"type": "video", "id": "PASTE_PLAN_5_DEMO_1_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_5_DEMO_2_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_5_DEMO_3_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_5_DEMO_4_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_5_DEMO_5_FILE_ID"}
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

        "image": "PASTE_PLAN_6_IMAGE_HERE",
        "qr": "PASTE_PLAN_6_QR_HERE",

        "demos": [
            {"type": "video", "id": "PASTE_PLAN_6_DEMO_1_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_6_DEMO_2_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_6_DEMO_3_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_6_DEMO_4_FILE_ID"},
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

        "image": "PASTE_PLAN_7_IMAGE_HERE",
        "qr": "PASTE_PLAN_7_QR_HERE",

        "demos": [
            {"type": "video", "id": "PASTE_PLAN_7_DEMO_1_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_7_DEMO_2_FILE_ID"},
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

        "image": "PASTE_PLAN_8_IMAGE_HERE",
        "qr": "PASTE_PLAN_8_QR_HERE",

        "demos": [
            {
                "type": "video",
                "id": "BAACAgUAAxkBAAI06GrHM2QUeiT0Q6J5yEopeA96Aim1AAJKIwACv685VjMk0xUgmBWJPQQ"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_8_DEMO_2_FILE_ID"
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
        "price": "00",
        "validity": "180 days",
        "videos": "30000+",

        "image": "PASTE_PLAN_9_IMAGE_HERE",
        "qr": "PASTE_PLAN_9_QR_HERE",

        "demos": [
            {"type": "video", "id": "PASTE_PLAN_9_DEMO_1_FILE_ID"},
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

        "image": "PASTE_PLAN_10_IMAGE_HERE",
        "qr": "PASTE_PLAN_10_QR_HERE",

        "demos": [
            {"type": "video", "id": "PASTE_PLAN_10_DEMO_1_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_10_DEMO_2_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_10_DEMO_3_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_10_DEMO_4_FILE_ID"},
            {"type": "video", "id": "PASTE_PLAN_10_DEMO_5_FILE_ID"}
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
    "✨ <b>𝙒𝙀𝙇𝘾𝙊𝙈𝙀</b> ✨\n\n"
    "𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 𝙤𝙪𝙧 𝙎𝙎𝙈 𝙘𝙤𝙪𝙧𝙨𝙚.\n"
    "𝘾𝙝𝙤𝙤𝙨𝙚 𝙖𝙣 𝙤𝙥𝙩𝙞𝙤𝙣 𝙗𝙚𝙡𝙤𝙬.\n\n"
    "👇 <b>𝙋𝙡𝙚𝙖𝙨𝙚 𝙘𝙝𝙤𝙤𝙨𝙚:</b>"
)


def send_start_screen(chat_id):

    kb = InlineKeyboardMarkup()

    kb.row(
        button(
            " 𝙁𝙍𝙀𝙀",
            data="free",
            style="success"
        ),
        button(
            " 𝙋𝘼𝙄𝘿",
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
        "🔒 <b>𝙊𝙉𝙇𝙔 𝙁𝙊𝙍 𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝙐𝙎𝙀𝙍𝙎</b>\n\n"
        "✨ 𝙏𝙝𝙞𝙨 𝙨𝙚𝙘𝙩𝙞𝙤𝙣 𝙞𝙨 𝙛𝙤𝙧 𝙥𝙧𝙚𝙢𝙞𝙪𝙢 𝙪𝙨𝙚𝙧𝙨.",
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
            f"📦 {p['name']} · ₹{p['price']}",
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
        "💬 𝙎𝙐𝙋𝙋𝙊𝙍𝙏",
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
            "🔴 𝘽𝙐𝙔 𝙉𝙊𝙒 💳",
            data=f"buy:{plan['id']}",
            style="danger"
        ),
        button(
            "🟢 𝘿𝙀𝙈𝙊 🎬",
            data=f"demo_plan:{plan['id']}",
            style="success"
        )
    )

    add_styled(
        kb,
        "🔵 𝘽𝘼𝘾𝙆",
        data="home",
        index=2
    )

    send_photo_or_text(
        chat_id,
        plan.get("image", ""),
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

    # Next button
    if index < len(demos) - 1:

        kb.add(
            button(
                "🔵 𝙉𝙀𝙓𝙏 𝘿𝙀𝙈𝙊 ➡️",
                data=f"next_demo:{plan_id}:{index}",
                style="primary"
            )
        )

    else:

        kb.add(
            button(
                "🔴 𝘿𝙀𝙈𝙊 𝙊𝙑𝙀𝙍",
                data=f"demo_over:{plan_id}",
                style="danger"
            )
        )

    kb.add(
        button(
            "🟢 𝘽𝘼𝘾𝙆 𝙏𝙊 𝙋𝙇𝘼𝙉",
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
            "🔴 𝘽𝙐𝙔 𝙋𝘼𝘾𝙆 💳",
            data=f"buy:{plan_id}",
            style="danger"
        )
    )

    kb.row(
        button(
            "🟢 𝘾𝙃𝘼𝙉𝙂𝙀 𝙋𝙇𝘼𝙉",
            data="demo_menu",
            style="success"
        )
    )

    kb.row(
        button(
            "🔵 𝘽𝘼𝘾𝙆 𝙏𝙊 𝙋𝙇𝘼𝙉",
            data=f"plan:{plan_id}",
            style="primary"
        )
    )

    bot.send_message(
        chat_id,
        "🏁 <b>𝘿𝙀𝙈𝙊 𝙊𝙑𝙀𝙍</b>\n\n"
        "✨ 𝙋𝙡𝙚𝙖𝙨𝙚 𝙥𝙪𝙧𝙘𝙝𝙖𝙨𝙚 𝙩𝙝𝙚 "
        "𝙥𝙧𝙚𝙢𝙞𝙪𝙢 𝙥𝙡𝙖𝙣 𝙩𝙤 𝙘𝙤𝙣𝙩𝙞𝙣𝙪𝙚.",
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
            "🟢 𝙄 𝙋𝘼𝙄𝘿",
            data=f"paid:{plan['id']}",
            style="success"
        ),
        button(
            "🔵 𝘽𝘼𝘾𝙆",
            data=f"plan:{plan['id']}",
            style="primary"
        )
    )

    caption = (
        f"💰 <b>𝙋𝙖𝙮: ₹{plan['price']}</b>\n\n"
        "1️⃣ 𝙎𝙘𝙖𝙣 𝙩𝙝𝙚 𝙌𝙍.\n"
        "2️⃣ 𝙋𝙖𝙮 𝙩𝙝𝙚 𝙚𝙭𝙖𝙘𝙩 𝙖𝙢𝙤𝙪𝙣𝙩.\n"
        "3️⃣ 𝘾𝙡𝙞𝙘𝙠 <b>𝙄 𝙋𝘼𝙄𝘿</b>.\n"
        "4️⃣ 𝙎𝙚𝙣𝙙 𝙥𝙖𝙮𝙢𝙚𝙣𝙩 𝙨𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩."
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
