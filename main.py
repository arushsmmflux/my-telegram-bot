import os
import sqlite3
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
DB_PATH = os.getenv("DB_PATH", "bot.db")

if not TOKEN or not ADMIN_ID:
    raise RuntimeError("BOT_TOKEN aur ADMIN_ID environment variables set karo.")

bot = telebot.TeleBot(TOKEN)


def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def setup_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    with db() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price TEXT NOT NULL,
                description TEXT DEFAULT '',
                image_id TEXT DEFAULT '',
                qr_id TEXT DEFAULT '',
                qr_caption TEXT DEFAULT '',
                active INTEGER DEFAULT 1
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan_id INTEGER NOT NULL,
                screenshot_id TEXT DEFAULT '',
                status TEXT DEFAULT 'awaiting_payment',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def get_setting(key, default=""):
    with db() as con:
        row = con.execute(
            "SELECT value FROM settings WHERE key = ?", (key,)
        ).fetchone()
    return row["value"] if row else default


def set_setting(key, value):
    with db() as con:
        con.execute("""
            INSERT INTO settings(key, value) VALUES(?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (key, value))


def is_admin(user_id):
    return user_id == ADMIN_ID


def plans_keyboard():
    kb = InlineKeyboardMarkup()
    colors = ["danger", "success", "primary"]

    with db() as con:
        plans = con.execute(
            "SELECT id, name, price FROM plans WHERE active = 1 ORDER BY id"
        ).fetchall()

    for i, plan in enumerate(plans):
        label = f"{plan['name']} — ₹{plan['price']}"
        try:
            button = InlineKeyboardButton(
                label,
                callback_data=f"plan:{plan['id']}",
                style=colors[i % 3]
            )
        except (TypeError, ValueError):
            button = InlineKeyboardButton(
                label, callback_data=f"plan:{plan['id']}"
            )
        kb.add(button)

    demo_link = get_setting("demo_link")
    if demo_link.startswith(("https://", "http://")):
        kb.add(InlineKeyboardButton("Demo Channel", url=demo_link))

    return kb


def show_start(chat_id):
    welcome_caption = get_setting("welcome_caption")
    welcome_image = get_setting("welcome_image")

    with db() as con:
        count = con.execute(
            "SELECT COUNT(*) AS n FROM plans WHERE active = 1"
        ).fetchone()["n"]

    if not welcome_caption and not welcome_image and count == 0:
        bot.send_message(chat_id, "Bot not ready")
        return

    if welcome_image:
        bot.send_photo(
            chat_id,
            welcome_image,
            caption=welcome_caption or "Welcome!"
        )
    else:
        bot.send_message(chat_id, welcome_caption or "Welcome!")

    if count:
        bot.send_message(
            chat_id,
            "Available plans:",
            reply_markup=plans_keyboard()
        )


@bot.message_handler(commands=["start"])
def start(message):
    show_start(message.chat.id)


@bot.message_handler(commands=["admin"])
def admin(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "Access denied.")
        return

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Pending Orders", callback_data="pending"))
    kb.add(InlineKeyboardButton("Set Welcome Caption", callback_data="set_welcome"))
    kb.add(InlineKeyboardButton("Set Welcome Image", callback_data="set_welcome_image"))
    kb.add(InlineKeyboardButton("Set Demo Link", callback_data="set_demo"))
    kb.add(InlineKeyboardButton("Add Plan", callback_data="add_plan"))
    kb.add(InlineKeyboardButton("List Plans", callback_data="admin_plans"))

    bot.send_message(message.chat.id, "Admin panel:", reply_markup=kb)


# Simple admin conversation states for this starter
admin_state = {}


@bot.callback_query_handler(func=lambda c: c.data == "set_welcome")
def set_welcome_callback(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Access denied.")
        return
    admin_state[call.from_user.id] = "welcome_caption"
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Welcome caption bhej.")


@bot.callback_query_handler(func=lambda c: c.data == "set_welcome_image")
def set_welcome_image_callback(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Access denied.")
        return
    admin_state[call.from_user.id] = "welcome_image"
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Welcome image bhej.")


@bot.callback_query_handler(func=lambda c: c.data == "set_demo")
def set_demo_callback(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Access denied.")
        return
    admin_state[call.from_user.id] = "demo_link"
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Demo channel ka https:// link bhej.")


@bot.message_handler(
    content_types=["text", "photo"],
    func=lambda m: is_admin(m.from_user.id)
    and m.from_user.id in admin_state
)
def handle_admin_input(message):
    state = admin_state.get(message.from_user.id)

    if state == "welcome_caption" and message.content_type == "text":
        set_setting("welcome_caption", message.text)
        admin_state.pop(message.from_user.id, None)
        bot.reply_to(message, "Welcome caption saved.")

    elif state == "welcome_image" and message.content_type == "photo":
        set_setting("welcome_image", message.photo[-1].file_id)
        admin_state.pop(message.from_user.id, None)
        bot.reply_to(message, "Welcome image saved.")

    elif state == "demo_link" and message.content_type == "text":
        link = message.text.strip()
        if not link.startswith(("https://", "http://")):
            bot.reply_to(message, "Valid https:// link bhej.")
            return
        set_setting("demo_link", link)
        admin_state.pop(message.from_user.id, None)
        bot.reply_to(message, "Demo link saved.")

    else:
        bot.reply_to(message, "Is step ke liye sahi text ya photo bhej.")


@bot.callback_query_handler(func=lambda c: c.data.startswith("plan:"))
def open_plan(call):
    try:
        plan_id = int(call.data.split(":")[1])
    except (ValueError, IndexError):
        bot.answer_callback_query(call.id, "Invalid plan.")
        return

    with db() as con:
        plan = con.execute(
            "SELECT * FROM plans WHERE id = ? AND active = 1",
            (plan_id,)
        ).fetchone()

    bot.answer_callback_query(call.id)

    if not plan:
        bot.send_message(call.message.chat.id, "Plan unavailable.")
        return

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Buy Now", callback_data=f"buy:{plan_id}"))
    kb.add(InlineKeyboardButton("Back", callback_data="back"))

    caption = (
        f"{plan['name']} — ₹{plan['price']}\n\n"
        f"{plan['description'] or ''}"
    )

    if plan["image_id"]:
        bot.send_photo(
            call.message.chat.id,
            plan["image_id"],
            caption=caption,
            reply_markup=kb
        )
    else:
        bot.send_message(
            call.message.chat.id, caption, reply_markup=kb
        )


@bot.callback_query_handler(func=lambda c: c.data.startswith("buy:"))
def buy_plan(call):
    try:
        plan_id = int(call.data.split(":")[1])
    except (ValueError, IndexError):
        bot.answer_callback_query(call.id, "Invalid plan.")
        return

    with db() as con:
        plan = con.execute(
            "SELECT * FROM plans WHERE id = ? AND active = 1",
            (plan_id,)
        ).fetchone()

        if plan:
            con.execute(
                "INSERT INTO orders(user_id, plan_id) VALUES(?, ?)",
                (call.from_user.id, plan_id)
            )

    bot.answer_callback_query(call.id)

    if not plan:
        bot.send_message(call.message.chat.id, "Plan unavailable.")
        return

    if not plan["qr_id"]:
        bot.send_message(
            call.message.chat.id,
            "Payment QR abhi configured nahi hai. Admin se contact karo."
        )
        return

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(
        "Submit Payment Screenshot",
        callback_data=f"submit:{plan_id}"
    ))
    kb.add(InlineKeyboardButton("Back", callback_data=f"plan:{plan_id}"))

    bot.send_photo(
        call.message.chat.id,
        plan["qr_id"],
        caption=plan["qr_caption"] or f"Pay ₹{plan['price']} using this QR.",
        reply_markup=kb
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("submit:"))
def submit_payment(call):
    try:
        plan_id = int(call.data.split(":")[1])
    except (ValueError, IndexError):
        bot.answer_callback_query(call.id, "Invalid plan.")
        return

    with db() as con:
        order = con.execute("""
            SELECT id FROM orders
            WHERE user_id = ? AND plan_id = ? AND status = 'awaiting_payment'
            ORDER BY id DESC LIMIT 1
        """, (call.from_user.id, plan_id)).fetchone()

    if not order:
        bot.answer_callback_query(call.id, "Order not found.")
        return

    admin_state[call.from_user.id] = f"payment:{order['id']}"
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "Ab payment ka screenshot photo ke roop mein bhej."
    )


@bot.message_handler(content_types=["photo"])
def receive_payment_screenshot(message):
    state = admin_state.get(message.from_user.id, "")
    if not state.startswith("payment:"):
        return

    try:
        order_id = int(state.split(":")[1])
    except ValueError:
        admin_state.pop(message.from_user.id, None)
        return

    screenshot_id = message.photo[-1].file_id

    with db() as con:
        con.execute("""
            UPDATE orders
            SET screenshot_id = ?, status = 'pending'
            WHERE id = ? AND user_id = ?
        """, (screenshot_id, order_id, message.from_user.id))

    admin_state.pop(message.from_user.id, None)

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("Approve", callback_data=f"approve:{order_id}"),
        InlineKeyboardButton("Reject", callback_data=f"reject:{order_id}")
    )

    bot.send_message(
        message.chat.id,
        "Screenshot received. Admin verification ke baad update milega."
    )

    bot.send_photo(
        ADMIN_ID,
        screenshot_id,
        caption=f"Payment order #{order_id}\nUser ID: {message.from_user.id}",
        reply_markup=kb
    )


@bot.callback_query_handler(
    func=lambda c: c.data.startswith(("approve:", "reject:"))
)
def review_order(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Access denied.")
        return

    action, order_text = call.data.split(":", 1)
    order_id = int(order_text)
    new_status = "approved" if action == "approve" else "rejected"

    with db() as con:
        order = con.execute("""
            SELECT user_id FROM orders
            WHERE id = ? AND status = 'pending'
        """, (order_id,)).fetchone()

        if order:
            con.execute(
                "UPDATE orders SET status = ? WHERE id = ?",
                (new_status, order_id)
            )

    bot.answer_callback_query(call.id)

    if not order:
        bot.send_message(call.message.chat.id, "Order already reviewed or missing.")
        return

    bot.send_message(
        order["user_id"],
        "Payment approved! ✅" if new_status == "approved"
        else "Payment rejected. Admin se contact karo."
    )
    bot.send_message(
        call.message.chat.id,
        f"Order #{order_id}: {new_status}"
    )


@bot.callback_query_handler(func=lambda c: c.data == "pending")
def show_pending(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Access denied.")
        return

    with db() as con:
        orders = con.execute("""
            SELECT id, user_id, plan_id FROM orders
            WHERE status = 'pending' ORDER BY id DESC LIMIT 20
        """).fetchall()

    bot.answer_callback_query(call.id)

    if not orders:
        bot.send_message(call.message.chat.id, "No pending orders.")
        return

    for order in orders:
        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton("Approve", callback_data=f"approve:{order['id']}"),
            InlineKeyboardButton("Reject", callback_data=f"reject:{order['id']}")
        )
        with db() as con:
            row = con.execute(
                "SELECT screenshot_id FROM orders WHERE id = ?",
                (order["id"],)
            ).fetchone()

        caption = (
            f"Order #{order['id']}\n"
            f"User ID: {order['user_id']}\n"
            f"Plan ID: {order['plan_id']}"
        )

        if row and row["screenshot_id"]:
            bot.send_photo(
                call.message.chat.id, row["screenshot_id"],
                caption=caption, reply_markup=kb
            )
        else:
            bot.send_message(
                call.message.chat.id, caption, reply_markup=kb
            )


@bot.callback_query_handler(func=lambda c: c.data == "back")
def back_to_plans(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "Available plans:",
        reply_markup=plans_keyboard()
    )


@bot.callback_query_handler(func=lambda c: c.data == "add_plan")
def add_plan_placeholder(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Access denied.")
        return
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "Plan creation UI is not included in this starter yet."
    )


@bot.callback_query_handler(func=lambda c: c.data == "admin_plans")
def admin_plans_placeholder(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Access denied.")
        return

    with db() as con:
        plans = con.execute(
            "SELECT id, name, price, active FROM plans ORDER BY id"
        ).fetchall()

    bot.answer_callback_query(call.id)

    if not plans:
        bot.send_message(
            call.message.chat.id,
            "Abhi koi plan nahi hai. Plan creation UI next step mein add karenge."
        )
        return

    text = "\n".join(
        f"#{p['id']} — {p['name']} — ₹{p['price']} "
        f"({'active' if p['active'] else 'inactive'})"
        for p in plans
    )
    bot.send_message(call.message.chat.id, text)


if __name__ == "__main__":
    setup_db()
    print("Bot starting...")
    bot.infinity_polling(skip_pending=True)
