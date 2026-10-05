
import os
import sqlite3
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ============== CONFIG ==============

BOT_TOKEN = os.getenv("BOT_TOKEN", "PASTE_BOT_TOKEN_HERE")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))

DB_PATH = os.getenv("DB_PATH", "/data/bot.db")

WELCOME_IMAGE = "https://placehold.co/1200x700/png?text=Welcome"
QR_IMAGE = "https://placehold.co/800x800/png?text=Payment+QR"
TEMP_IMAGE = "https://placehold.co/1200x700/png?text={}"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


# ============== 5 PLANS ==============

PLANS = [
    {
        "name": "YouTube",
        "price": 49,
        "image": TEMP_IMAGE.format("YouTube+Plan"),
        "caption": "<b>YouTube Plan</b>\n\nPrice: ₹49\n\nPlan details coming soon.",
        "demos": [
            "https://example.com/demo1",
            "https://example.com/demo2",
            "https://example.com/demo3"
        ]
    },
    {
        "name": "Instagram",
        "price": 49,
        "image": TEMP_IMAGE.format("Instagram+Plan"),
        "caption": "<b>Instagram Plan</b>\n\nPrice: ₹49\n\nPlan details coming soon.",
        "demos": [
            "https://example.com/demo1",
            "https://example.com/demo2",
            "https://example.com/demo3"
        ]
    },
    {
        "name": "Facebook",
        "price": 49,
        "image": TEMP_IMAGE.format("Facebook+Plan"),
        "caption": "<b>Facebook Plan</b>\n\nPrice: ₹49\n\nPlan details coming soon.",
        "demos": [
            "https://example.com/demo1",
            "https://example.com/demo2",
            "https://example.com/demo3"
        ]
    },
    {
        "name": "Plan 4",
        "price": 49,
        "image": TEMP_IMAGE.format("Plan+4"),
        "caption": "<b>Plan 4</b>\n\nPrice: ₹49\n\nPlan details coming soon.",
        "demos": [
            "https://example.com/demo1",
            "https://example.com/demo2",
            "https://example.com/demo3"
        ]
    },
    {
        "name": "Plan 5",
        "price": 49,
        "image": TEMP_IMAGE.format("Plan+5"),
        "caption": "<b>Plan 5</b>\n\nPrice: ₹49\n\nPlan details coming soon.",
        "demos": [
            "https://example.com/demo1",
            "https://example.com/demo2",
            "https://example.com/demo3"
        ]
    }
]


# ============== DATABASE ==============

def get_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            plan_index INTEGER NOT NULL,
            status TEXT DEFAULT 'awaiting_payment',
            screenshot_file_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    return conn


# ============== PLAN BUTTONS ==============

def plans_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)

    for i, plan in enumerate(PLANS):
        kb.add(
            InlineKeyboardButton(
                f"{plan['name']} ₹{plan['price']}",
                callback_data=f"plan:{i}"
            )
        )

    return kb


def plan_keyboard(index, demo_page=False):
    kb = InlineKeyboardMarkup(row_width=2)
    plan = PLANS[index]

    if demo_page:
        kb.row(
            InlineKeyboardButton("Demo 1", url=plan["demos"][0]),
            InlineKeyboardButton("Demo 2", url=plan["demos"][1]),
            InlineKeyboardButton("Demo 3", url=plan["demos"][2])
        )

        kb.row(
            InlineKeyboardButton(
                "🟢 Buy Now",
                callback_data=f"buy:{index}"
            )
        )

        kb.row(
            InlineKeyboardButton(
                "🔙 Back",
                callback_data=f"plan:{index}"
            )
        )

    else:
        kb.row(
            InlineKeyboardButton(
                "🟢 Buy Now",
                callback_data=f"buy:{index}"
            ),
            InlineKeyboardButton(
                "🔵 View Demo",
                callback_data=f"demos:{index}"
            )
        )

        kb.row(
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="plans"
            )
        )

    return kb


# ============== DISPLAY PLAN ==============

def show_plan(chat_id, message_id, index, demo_page=False):
    plan = PLANS[index]

    # Delete previous message
    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass

    # Same image and caption; only buttons change
    bot.send_photo(
        chat_id,
        plan["image"],
        caption=plan["caption"],
        reply_markup=plan_keyboard(index, demo_page)
    )


# ============== START / AGE GATE ==============

@bot.message_handler(commands=["start"])
def start(message):
    kb = InlineKeyboardMarkup()

    kb.row(
        InlineKeyboardButton(
            "✅ I am 18+",
            callback_data="age_yes"
        )
    )

    kb.row(
        InlineKeyboardButton(
            "❌ Under 18",
            callback_data="age_no"
        )
    )

    try:
        bot.send_photo(
            message.chat.id,
            WELCOME_IMAGE,
            caption="Welcome!\nPlease confirm your age to continue.",
            reply_markup=kb
        )
    except Exception:
        bot.send_message(
            message.chat.id,
            "Welcome!\nPlease confirm your age to continue.",
            reply_markup=kb
        )


@bot.callback_query_handler(func=lambda c: c.data == "age_yes")
def age_yes(call):
    bot.answer_callback_query(call.id)

    bot.send_message(
        call.message.chat.id,
        "📦 <b>Choose your plan</b>",
        reply_markup=plans_keyboard()
    )


@bot.callback_query_handler(func=lambda c: c.data == "age_no")
def age_no(call):
    bot.answer_callback_query(
        call.id,
        "You cannot continue.",
        show_alert=True
    )


# ============== BACK TO PLANS ==============

@bot.callback_query_handler(func=lambda c: c.data == "plans")
def back_to_plans(call):
    bot.answer_callback_query(call.id)

    try:
        bot.edit_message_text(
            "📦 <b>Choose your plan</b>",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=plans_keyboard()
        )
    except Exception:
        bot.send_message(
            call.message.chat.id,
            "📦 <b>Choose your plan</b>",
            reply_markup=plans_keyboard()
        )


# ============== OPEN PLAN ==============

@bot.callback_query_handler(func=lambda c: c.data.startswith("plan:"))
def open_plan(call):
    bot.answer_callback_query(call.id)

    index = int(call.data.split(":")[1])

    show_plan(
        call.message.chat.id,
        call.message.message_id,
        index,
        demo_page=False
    )


# ============== VIEW DEMOS ==============

@bot.callback_query_handler(func=lambda c: c.data.startswith("demos:"))
def open_demos(call):
    bot.answer_callback_query(call.id)

    index = int(call.data.split(":")[1])

    show_plan(
        call.message.chat.id,
        call.message.message_id,
        index,
        demo_page=True
    )


# ============== BUY NOW / PAYMENT ==============

@bot.callback_query_handler(func=lambda c: c.data.startswith("buy:"))
def buy_now(call):
    bot.answer_callback_query(call.id)

    index = int(call.data.split(":")[1])
    plan = PLANS[index]

    conn = get_db()

    cursor = conn.execute(
        """
        INSERT INTO orders (user_id, plan_index, status)
        VALUES (?, ?, ?)
        """,
        (call.from_user.id, index, "awaiting_payment")
    )

    order_id = cursor.lastrowid

    conn.commit()
    conn.close()

    kb = InlineKeyboardMarkup()

    kb.row(
        InlineKeyboardButton(
            "✅ I Paid",
            callback_data=f"paid:{order_id}"
        )
    )

    kb.row(
        InlineKeyboardButton(
            "🔙 Back",
            callback_data=f"plan:{index}"
        )
    )

    caption = (
        "🧾 <b>Payment Details</b>\n\n"
        f"Plan: {plan['name']}\n"
        f"Amount: ₹{plan['price']}\n"
        f"Order ID: #{order_id}\n\n"
        "Payment karne ke baad I Paid dabao "
        "aur payment screenshot bhejo."
    )

    try:
        bot.send_photo(
            call.message.chat.id,
            QR_IMAGE,
            caption=caption,
            reply_markup=kb
        )
    except Exception:
        bot.send_message(
            call.message.chat.id,
            caption,
            reply_markup=kb
        )


# ============== I PAID ==============

@bot.callback_query_handler(func=lambda c: c.data.startswith("paid:"))
def paid(call):
    bot.answer_callback_query(call.id)

    order_id = int(call.data.split(":")[1])

    msg = bot.send_message(
        call.message.chat.id,
        f"Order #{order_id}\n\nAb payment screenshot photo ke roop mein bhejo."
    )

    bot.register_next_step_handler(
        msg,
        receive_screenshot,
        order_id
    )


# ============== RECEIVE SCREENSHOT ==============

def receive_screenshot(message, order_id):
    if not message.photo:
        bot.send_message(
            message.chat.id,
            "Screenshot photo ke roop mein bhejo. "
            "Phir I Paid button dobara dabao."
        )
        return

    file_id = message.photo[-1].file_id

    conn = get_db()

    conn.execute(
        """
        UPDATE orders
        SET status = 'review', screenshot_file_id = ?
        WHERE id = ? AND user_id = ?
        """,
        (file_id, order_id, message.from_user.id)
    )

    conn.commit()
    conn.close()

    kb = InlineKeyboardMarkup()

    kb.row(
        InlineKeyboardButton(
            "✅ Approve",
            callback_data=f"approve:{order_id}"
        ),
        InlineKeyboardButton(
            "❌ Reject",
            callback_data=f"reject:{order_id}"
        )
    )

    try:
        bot.send_photo(
            ADMIN_ID,
            file_id,
            caption=(
                "Payment screenshot received\n"
                f"Order ID: #{order_id}\n"
                f"User ID: {message.from_user.id}"
            ),
            reply_markup=kb
        )

        bot.send_message(
            message.chat.id,
            "Screenshot admin ko bhej diya gaya hai. "
            "Approval ka wait karo."
        )

    except Exception as error:
        print("Admin notification error:", error)

        bot.send_message(
            message.chat.id,
            "Screenshot bhejne mein problem aayi. "
            "Admin ID aur bot settings check karo."
        )


# ============== ADMIN APPROVE / REJECT ==============

@bot.callback_query_handler(
    func=lambda c: (
        c.data.startswith("approve:")
        or c.data.startswith("reject:")
    )
)
def review_order(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(
            call.id,
            "Only admin can do this.",
            show_alert=True
        )
        return

    action, raw_id = call.data.split(":")
    order_id = int(raw_id)

    status = "approved" if action == "approve" else "rejected"

    conn = get_db()

    row = conn.execute(
        "SELECT user_id FROM orders WHERE id = ?",
        (order_id,)
    ).fetchone()

    conn.execute(
        "UPDATE orders SET status = ? WHERE id = ?",
        (status, order_id)
    )

    conn.commit()
    conn.close()

    bot.answer_callback_query(
        call.id,
        f"Order {status}."
    )

    if row:
        bot.send_message(
            row[0],
            f"Order #{order_id} {status}."
        )

    try:
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=None
        )
    except Exception:
        pass


# ============== RUN BOT ==============

if __name__ == "__main__":
    if BOT_TOKEN == "PASTE_BOT_TOKEN_HERE":
        raise SystemExit(
            "Please set BOT_TOKEN in your Railway Variables."
        )

    get_db().close()

    print("Bot started successfully.")

    bot.infinity_polling(
        skip_pending=True,
        timeout=30,
        long_polling_timeout=30
    )
```
