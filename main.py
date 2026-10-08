import os
import logging
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ============================================================
# RAILWAY VARIABLES
# ============================================================

TOKEN = os.getenv("BOT_TOKEN", "").strip()

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing in Railway Variables")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("course_bot")

bot = telebot.TeleBot(TOKEN)


# ============================================================
# BASIC SETTINGS
# ============================================================

SUPPORT_LINK = "https://t.me/xylerigcc"

MAINTENANCE_MODE = True

MAINTENANCE_TEXT = """
🛠️ 𝘽𝙊𝙏 𝙐𝙉𝘿𝙀𝙍 𝙈𝘼𝙄𝙉𝙏𝙀𝙉𝘼𝙉𝘾𝙀

✨ We are currently updating the bot.

⏳ Please try again later.

🙏 Thanks for your patience.
"""


# ============================================================
# ============================================================
#                 EDIT YOUR 10 PLANS HERE
# ============================================================
# ============================================================

PLANS = [

    # ========================================================
    # PLAN 1
    # ========================================================

    {
        "id": 1,
        "name": "PLAN hai bsdk",
        "price": "90",
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


    # ========================================================
    # PLAN 2
    # ========================================================

    {
        "id": 2,
        "name": "PLAN 2",
        "price": "00",
        "validity": "180 days",
        "videos": "30000+",

        "image": "PASTE_PLAN_2_IMAGE_HERE",
        "qr": "PASTE_PLAN_2_QR_HERE",

        "demos": [
            {
                "type": "video",
                "id": "PASTE_PLAN_2_DEMO_1_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_2_DEMO_2_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_2_DEMO_3_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_2_DEMO_4_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_2_DEMO_5_FILE_ID"
            }
        ],

        "caption": "PLAN 2 CAPTION",

        "active": True
    },


    # ========================================================
    # PLAN 3
    # ========================================================

    {
        "id": 3,
        "name": "PLAN 3",
        "price": "00",
        "validity": "180 days",
        "videos": "30000+",

        "image": "PASTE_PLAN_3_IMAGE_HERE",
        "qr": "PASTE_PLAN_3_QR_HERE",

        "demos": [
            {
                "type": "video",
                "id": "PASTE_PLAN_3_DEMO_1_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_3_DEMO_2_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_3_DEMO_3_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_3_DEMO_4_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_3_DEMO_5_FILE_ID"
            }
        ],

        "caption": "PLAN 3 CAPTION",

        "active": True
    },


    # ========================================================
    # PLAN 4
    # ========================================================

    {
        "id": 4,
        "name": "PLAN 4",
        "price": "00",
        "validity": "180 days",
        "videos": "30000+",

        "image": "PASTE_PLAN_4_IMAGE_HERE",
        "qr": "PASTE_PLAN_4_QR_HERE",

        "demos": [
            {
                "type": "video",
                "id": "PASTE_PLAN_4_DEMO_1_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_4_DEMO_2_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_4_DEMO_3_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_4_DEMO_4_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_4_DEMO_5_FILE_ID"
            }
        ],

        "caption": "PLAN 4 CAPTION",

        "active": True
    },


    # ========================================================
    # PLAN 5
    # ========================================================

    {
        "id": 5,
        "name": "PLAN 5",
        "price": "00",
        "validity": "180 days",
        "videos": "30000+",

        "image": "PASTE_PLAN_5_IMAGE_HERE",
        "qr": "PASTE_PLAN_5_QR_HERE",

        "demos": [
            {
                "type": "video",
                "id": "PASTE_PLAN_5_DEMO_1_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_5_DEMO_2_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_5_DEMO_3_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_5_DEMO_4_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_5_DEMO_5_FILE_ID"
            }
        ],

        "caption": "PLAN 5 CAPTION",

        "active": True
    },


    # ========================================================
    # PLAN 6
    # ========================================================

    {
        "id": 6,
        "name": "PLAN 6",
        "price": "00",
        "validity": "180 days",
        "videos": "30000+",

        "image": "PASTE_PLAN_6_IMAGE_HERE",
        "qr": "PASTE_PLAN_6_QR_HERE",

        "demos": [
            {
                "type": "video",
                "id": "PASTE_PLAN_6_DEMO_1_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_6_DEMO_2_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_6_DEMO_3_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_6_DEMO_4_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_6_DEMO_5_FILE_ID"
            }
        ],

        "caption": "PLAN 6 CAPTION",

        "active": True
    },


    # ========================================================
    # PLAN 7
    # ========================================================

    {
        "id": 7,
        "name": "PLAN 7",
        "price": "00",
        "validity": "180 days",
        "videos": "30000+",

        "image": "PASTE_PLAN_7_IMAGE_HERE",
        "qr": "PASTE_PLAN_7_QR_HERE",

        "demos": [
            {
                "type": "video",
                "id": "PASTE_PLAN_7_DEMO_1_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_7_DEMO_2_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_7_DEMO_3_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_7_DEMO_4_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_7_DEMO_5_FILE_ID"
            }
        ],

        "caption": "PLAN 7 CAPTION",

        "active": True
    },


    # ========================================================
    # PLAN 8
    # ========================================================

    {
        "id": 8,
        "name": "youtube viral shorts 🔥",
        "price": "58",
        "validity": "180 days",
        "videos": "30000+",

        "image": "https://ibb.co/5X0hc5dd",
        "qr": "https://ibb.co/xK77FFDK",

        "demos": [
            {
                "type": "video",
                "id": "BAACAgUAAxkBAAI06GrHM2QUeiT0Q6J5yEopeA96Aim1AAJKIwACv685VjMk0xUgmBWJPQQ"
            },
            {
                "type": "video",
                "id": "PASTE_VIDEO_FILE_ID_2_HERE"
            },
            {
                "type": "video",
                "id": "PASTE_VIDEO_FILE_ID_3_HERE"
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


    # ========================================================
    # PLAN 9
    # ========================================================

    {
        "id": 9,
        "name": "PLAN 9",
        "price": "00",
        "validity": "180 days",
        "videos": "30000+",

        "image": "PASTE_PLAN_9_IMAGE_HERE",
        "qr": "PASTE_PLAN_9_QR_HERE",

        "demos": [
            {
                "type": "video",
                "id": "PASTE_PLAN_9_DEMO_1_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_9_DEMO_2_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_9_DEMO_3_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_9_DEMO_4_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_9_DEMO_5_FILE_ID"
            }
        ],

        "caption": "PLAN 9 CAPTION",

        "active": True
    },


    # ========================================================
    # PLAN 10
    # ========================================================

    {
        "id": 10,
        "name": "PLAN 10",
        "price": "00",
        "validity": "180 days",
        "videos": "30000+",

        "image": "PASTE_PLAN_10_IMAGE_HERE",
        "qr": "PASTE_PLAN_10_QR_HERE",

        "demos": [
            {
                "type": "video",
                "id": "PASTE_PLAN_10_DEMO_1_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_10_DEMO_2_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_10_DEMO_3_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_10_DEMO_4_FILE_ID"
            },
            {
                "type": "video",
                "id": "PASTE_PLAN_10_DEMO_5_FILE_ID"
            }
        ],

        "caption": "PLAN 10 CAPTION",

        "active": True
    }

]


# ============================================================
# FIND PLAN
# ============================================================

def get_plan(plan_id):
    for plan in PLANS:
        if plan["id"] == plan_id:
            return plan
    return None


# ============================================================
# START
# ============================================================

@bot.message_handler(commands=["start"])
def start(message):

    if MAINTENANCE_MODE:

        keyboard = InlineKeyboardMarkup()

        keyboard.add(
            InlineKeyboardButton(
                "🛠️ 𝘽𝙊𝙏 𝙐𝙉𝘿𝙀𝙍 𝙈𝘼𝙄𝙉𝙏𝙀𝙉𝘼𝙉𝘾𝙀",
                callback_data="maintenance"
            )
        )

        keyboard.add(
            InlineKeyboardButton(
                "💬 𝙎𝙐𝙋𝙋𝙊𝙍𝙏",
                url=SUPPORT_LINK
            )
        )

        bot.send_message(
            message.chat.id,
            MAINTENANCE_TEXT,
            reply_markup=keyboard
        )

        return

    send_home(message.chat.id)


# ============================================================
# MAINTENANCE BUTTON
# ============================================================

@bot.callback_query_handler(func=lambda call: call.data == "maintenance")
def maintenance(call):

    bot.answer_callback_query(
        call.id,
        "🛠️ Bot is currently under maintenance."
    )


# ============================================================
# HOME
# ============================================================

def send_home(chat_id):

    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            "📚 𝙑𝙄𝙀𝙒 𝙋𝙇𝘼𝙉𝙎",
            callback_data="plans"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "🎬 𝘿𝙀𝙈𝙊",
            callback_data="demo_menu"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "💬 𝙎𝙐𝙋𝙋𝙊𝙍𝙏",
            url=SUPPORT_LINK
        )
    )

    bot.send_message(
        chat_id,
        "🎓 𝙎𝙎𝙈 𝘾𝙊𝙐𝙍𝙎𝙀\n\n"
        "✨ Choose an option below:",
        reply_markup=keyboard
    )


# ============================================================
# PLANS MENU
# ============================================================

@bot.callback_query_handler(func=lambda call: call.data == "plans")
def plans_menu(call):

    bot.answer_callback_query(call.id)

    keyboard = InlineKeyboardMarkup()

    active_plans = [
        p for p in PLANS
        if p.get("active", True)
    ]

    for plan in active_plans:

        keyboard.add(
            InlineKeyboardButton(
                f"📦 {plan['name']} — ₹{plan['price']}",
                callback_data=f"plan:{plan['id']}"
            )
        )

    keyboard.add(
        InlineKeyboardButton(
            "⬅️ 𝘽𝘼𝘾𝙆",
            callback_data="home"
        )
    )

    bot.edit_message_text(
        "📚 𝘼𝙑𝘼𝙄𝙇𝘼𝘽𝙇𝙀 𝙋𝙇𝘼𝙉𝙎\n\n"
        "👇 Select your plan:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=keyboard
    )


# ============================================================
# PLAN DETAILS
# ============================================================

@bot.callback_query_handler(func=lambda call: call.data.startswith("plan:"))
def show_plan(call):

    bot.answer_callback_query(call.id)

    try:
        plan_id = int(call.data.split(":")[1])
    except:
        return

    plan = get_plan(plan_id)

    if not plan:
        return

    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            "🎬 𝘿𝙀𝙈𝙊",
            callback_data=f"demo_start:{plan_id}"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "🛒 𝘽𝙐𝙔 𝙉𝙊𝙒",
            callback_data=f"buy:{plan_id}"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "⬅️ 𝘽𝘼𝘾𝙆",
            callback_data="plans"
        )
    )

    text = (
        f"📦 {plan['name']}\n\n"
        f"💰 Price: ₹{plan['price']}\n"
        f"⏳ Validity: {plan['validity']}\n"
        f"🎬 Videos: {plan['videos']}\n\n"
        f"{plan['caption']}"
    )

    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=keyboard
    )


# ============================================================
# DEMO MENU
# ============================================================

@bot.callback_query_handler(func=lambda call: call.data == "demo_menu")
def demo_menu(call):

    bot.answer_callback_query(call.id)

    keyboard = InlineKeyboardMarkup()

    for plan in PLANS:

        if not plan.get("active", True):
            continue

        if not plan.get("demos"):
            continue

        keyboard.add(
            InlineKeyboardButton(
                f"🎬 {plan['name']}",
                callback_data=f"demo_start:{plan['id']}"
            )
        )

    keyboard.add(
        InlineKeyboardButton(
            "⬅️ 𝘽𝘼𝘾𝙆",
            callback_data="home"
        )
    )

    bot.edit_message_text(
        "🎬 𝘿𝙀𝙈𝙊 𝙎𝙀𝘾𝙏𝙄𝙊𝙉\n\n"
        "👇 Select a plan:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=keyboard
    )


# ============================================================
# DEMO STATE
# ============================================================

demo_states = {}


# ============================================================
# SEND DEMO
# ============================================================

def send_demo(chat_id, plan_id, index=0):

    plan = get_plan(plan_id)

    if not plan:
        return

    demos = plan.get("demos", [])

    if not demos:
        bot.send_message(
            chat_id,
            "❌ No demos available for this plan."
        )
        return

    if index >= len(demos):
        send_demo_over(chat_id, plan_id)
        return

    demo = demos[index]

    media_type = demo.get("type", "video")
    file_id = demo.get("id", "").strip()

    if not file_id:
        bot.send_message(
            chat_id,
            f"⚠️ Demo {index + 1} file ID is empty."
        )
        return

    keyboard = InlineKeyboardMarkup()

    if index + 1 < len(demos):

        keyboard.add(
            InlineKeyboardButton(
                f"➡️ 𝙉𝙀𝙓𝙏 𝘿𝙀𝙈𝙊 ({index + 2}/{len(demos)})",
                callback_data=f"demonext:{plan_id}:{index + 1}"
            )
        )

    else:

        keyboard.add(
            InlineKeyboardButton(
                "✅ 𝘿𝙀𝙈𝙊 𝙊𝙑𝙀𝙍",
                callback_data=f"demoover:{plan_id}"
            )
        )

    keyboard.add(
        InlineKeyboardButton(
            "🛒 𝘽𝙐𝙔 𝙋𝘼𝘾𝙆",
            callback_data=f"buy:{plan_id}"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "⬅️ 𝘾𝙃𝘼𝙉𝙂𝙀 𝙋𝙇𝘼𝙉",
            callback_data="demo_menu"
        )
    )

    caption = (
        f"🎬 {plan['name']}\n"
        f"𝘿𝙀𝙈𝙊 {index + 1}/{len(demos)}"
    )

    try:

        if media_type.lower() == "photo":

            sent = bot.send_photo(
                chat_id,
                file_id,
                caption=caption,
                reply_markup=keyboard
            )

        else:

            sent = bot.send_video(
                chat_id,
                file_id,
                caption=caption,
                reply_markup=keyboard
            )

        demo_states[chat_id] = {
            "plan_id": plan_id,
            "index": index,
            "message_id": sent.message_id
        }

    except Exception as e:

        log.exception("Demo send failed")

        bot.send_message(
            chat_id,
            "❌ Demo send nahi ho paya.\n\n"
            "Check karo ki Telegram file_id correct hai."
        )


# ============================================================
# START DEMO
# ============================================================

@bot.callback_query_handler(func=lambda call: call.data.startswith("demo_start:"))
def demo_start(call):

    bot.answer_callback_query(call.id)

    try:
        plan_id = int(call.data.split(":")[1])
    except:
        return

    send_demo(
        call.message.chat.id,
        plan_id,
        0
    )


# ============================================================
# NEXT DEMO
# ============================================================

@bot.callback_query_handler(func=lambda call: call.data.startswith("demonext:"))
def demo_next(call):

    try:

        parts = call.data.split(":")

        plan_id = int(parts[1])
        next_index = int(parts[2])

    except:
        bot.answer_callback_query(call.id)
        return

    bot.answer_callback_query(call.id)

    # Delete previous demo
    try:
        bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )
    except Exception:
        pass

    send_demo(
        call.message.chat.id,
        plan_id,
        next_index
    )


# ============================================================
# DEMO OVER
# ============================================================

@bot.callback_query_handler(func=lambda call: call.data.startswith("demoover:"))
def demo_over_button(call):

    bot.answer_callback_query(call.id)

    try:
        plan_id = int(call.data.split(":")[1])
    except:
        return

    try:
        bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )
    except Exception:
        pass

    send_demo_over(
        call.message.chat.id,
        plan_id
    )


def send_demo_over(chat_id, plan_id):

    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            "🛒 𝘽𝙐𝙔 𝙋𝘼𝘾𝙆",
            callback_data=f"buy:{plan_id}"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "🔄 𝘾𝙃𝘼𝙉𝙂𝙀 𝙋𝙇𝘼𝙉",
            callback_data="demo_menu"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "💬 𝙎𝙐𝙋𝙋𝙊𝙍𝙏",
            url=SUPPORT_LINK
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "🏠 𝙃𝙊𝙈𝙀",
            callback_data="home"
        )
    )

    bot.send_message(
        chat_id,
        "✅ 𝘿𝙀𝙈𝙊 𝙊𝙑𝙀𝙍\n\n"
        "🔥 Interested in this pack?\n"
        "Choose an option below.",
        reply_markup=keyboard
    )


# ============================================================
# BUY
# ============================================================

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy:"))
def buy_plan(call):

    bot.answer_callback_query(call.id)

    try:
        plan_id = int(call.data.split(":")[1])
    except:
        return

    plan = get_plan(plan_id)

    if not plan:
        return

    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            "💬 𝘾𝙊𝙉𝙏𝘼𝘾𝙏 𝙎𝙐𝙋𝙋𝙊𝙍𝙏",
            url=SUPPORT_LINK
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "⬅️ 𝘽𝘼𝘾𝙆",
            callback_data=f"plan:{plan_id}"
        )
    )

    bot.edit_message_text(
        f"🛒 𝘽𝙐𝙔 — {plan['name']}\n\n"
        f"💰 Price: ₹{plan['price']}\n"
        f"⏳ Validity: {plan['validity']}\n\n"
        "💬 Contact support to complete your purchase.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=keyboard
    )


# ============================================================
# HOME CALLBACK
# ============================================================

@bot.callback_query_handler(func=lambda call: call.data == "home")
def home_callback(call):

    bot.answer_callback_query(call.id)

    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            "📚 𝙑𝙄𝙀𝙒 𝙋𝙇𝘼𝙉𝙎",
            callback_data="plans"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "🎬 𝘿𝙀𝙈𝙊",
            callback_data="demo_menu"
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            "💬 𝙎𝙐𝙋𝙋𝙊𝙍𝙏",
            url=SUPPORT_LINK
        )
    )

    bot.edit_message_text(
        "🎓 𝙎𝙎𝙈 𝘾𝙊𝙐𝙍𝙎𝙀\n\n"
        "✨ Choose an option below:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=keyboard
    )


# ============================================================
# RUN BOT
# ============================================================

print("🚀 Bot started successfully")
print("🛠️ Maintenance mode:", MAINTENANCE_MODE)

bot.infinity_polling(
    skip_pending=True,
    timeout=30,
    long_polling_timeout=30
)
