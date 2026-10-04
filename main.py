
import os
import sqlite3
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
DB_PATH = os.getenv("DB_PATH", "/data/bot.db")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing!")
if ADMIN_ID <= 0:
    raise RuntimeError("Set ADMIN_ID to your numeric Telegram user ID!")

# Create the database directory if needed.
os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)

bot = telebot.TeleBot(TOKEN)
db_lock = threading.RLock()
user_states = {}


def db():
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with db_lock, db() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            duration TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            active INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            plan_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'awaiting_payment',
            screenshot_id TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(plan_id) REFERENCES plans(id)
        );
        """)


def setting(key, default=""):
    with db_lock, db() as con:
        row = con.execute(
            "SELECT value FROM settings WHERE key=?", (key,)
        ).fetchone()
    return row["value"] if row else default


def set_setting(key, value):
    with db_lock, db() as con:
        con.execute("""
            INSERT INTO settings(key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """, (key, value))


def is_admin(user_id):
    return user_id == ADMIN_ID


def admin_only(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "⛔ You are not authorized.")
        return False
    return True


def menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🛍️ View Plans", callback_data="plans"),
        InlineKeyboardButton("📦 My Orders", callback_data="myorders"),
    )
    return kb


def admin_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("➕ Add Plan", callback_data="a_add"),
        InlineKeyboardButton("➖ Remove Plan", callback_data="a_remove"),
        InlineKeyboardButton("📝 Welcome Caption", callback_data="a_caption"),
        InlineKeyboardButton("🖼️ Welcome Image", callback_data="a_image"),
        InlineKeyboardButton("💳 Set UPI QR", callback_data="a_qr"),
        InlineKeyboardButton("📄 Payment Instructions", callback_data="a_instructions"),
        InlineKeyboardButton("📋 List Plans", callback_data="a_list"),
        InlineKeyboardButton("⏳ Pending Orders", callback_data="a_pending"),
    )
    return kb


def show_welcome(chat_id):
    caption = setting(
        "welcome_caption",
        "👋 Welcome!\n\nChoose a plan below to continue."
    )
    image_id = setting("welcome_image")
    if image_id:
        bot.send_photo(
            chat_id, image_id, caption=caption,
            reply_markup=menu()
        )
    else:
        bot.send_message(chat_id, caption, reply_markup=menu())


def add_order_buttons(order_id):
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton(
            "✅ Approve", callback_data=f"approve:{order_id}"
        ),
        InlineKeyboardButton(
            "❌ Reject", callback_data=f"reject:{order_id}"
        ),
    )
    return kb


@bot.message_handler(commands=["start"])
def start(message):
    user_states.pop(message.from_user.id, None)
    show_welcome(message.chat.id)


@bot.message_handler(commands=["admin"])
def admin(message):
    if not admin_only(message):
        return
    bot.send_message(
        message.chat.id, "🛠️ Admin Control Panel",
        reply_markup=admin_menu()
    )


@bot.message_handler(commands=["addplan"])
def addplan_command(message):
    if not admin_only(message):
        return
    user_states[message.from_user.id] = "add_plan"
    bot.reply_to(
        message,
        "Send the plan in ONE message, this format:\n\n"
        "Name | Price | Duration | Description\n\n"
        "Example:\n"
        "Premium | 199 | 30 days | Premium access"
    )


@bot.message_handler(commands=["removeplan"])
def removeplan_command(message):
    if not admin_only(message):
        return
    show_plans_for_removal(message.chat.id)


def show_plans_for_removal(chat_id):
    with db_lock, db() as con:
        rows = con.execute(
            "SELECT id, name, price FROM plans WHERE active=1 ORDER BY id"
        ).fetchall()
    if not rows:
        bot.send_message(chat_id, "No active plans.")
        return
    kb = InlineKeyboardMarkup()
    for row in rows:
        kb.add(InlineKeyboardButton(
            f"🗑️ {row['name']} — {row['price']}",
            callback_data=f"remove:{row['id']}"
        ))
    bot.send_message(chat_id, "Choose a plan to deactivate:", reply_markup=kb)


def show_plans(chat_id):
    with db_lock, db() as con:
        rows = con.execute(
            "SELECT * FROM plans WHERE active=1 ORDER BY id"
        ).fetchall()
    if not rows:
        bot.send_message(chat_id, "No plans available right now.")
        return

    for row in rows:
        text = (
            f"✨ {row['name']}\n"
            f"💰 Price: {row['price']}\n"
            f"⏳ Duration: {row['duration']}\n"
            f"📝 {row['description']}"
        )
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton(
            "🛒 Select Plan",
            callback_data=f"buy:{row['id']}"
        ))
        bot.send_message(chat_id, text, reply_markup=kb)


def show_pending(chat_id):
    with db_lock, db() as con:
        rows = con.execute("""
            SELECT o.id, o.user_id, o.screenshot_id, p.name, p.price
            FROM orders o JOIN plans p ON p.id=o.plan_id
            WHERE o.status='pending'
            ORDER BY o.id
        """).fetchall()

    if not rows:
        bot.send_message(chat_id, "✅ No pending orders.")
        return

    for row in rows:
        text = (
            f"Order #{row['id']}\n"
            f"User ID: {row['user_id']}\n"
            f"Plan: {row['name']}\n"
            f"Price: {row['price']}"
        )
        bot.send_message(
            chat_id, text, reply_markup=add_order_buttons(row["id"])
        )
        if row["screenshot_id"]:
            bot.send_photo(chat_id, row["screenshot_id"])


@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    uid = call.from_user.id
    data = call.data or ""

    # Admin actions are always authorized by Telegram numeric user ID.
    if data.startswith(("a_", "remove:", "approve:", "reject:")):
        if not is_admin(uid):
            bot.answer_callback_query(call.id, "Not authorized.", show_alert=True)
            return

    bot.answer_callback_query(call.id)

    if data == "plans":
        show_plans(call.message.chat.id)
        return

    if data == "myorders":
        with db_lock, db() as con:
            rows = con.execute("""
                SELECT o.id, o.status, p.name, p.price
                FROM orders o JOIN plans p ON p.id=o.plan_id
                WHERE o.user_id=? ORDER BY o.id DESC LIMIT 10
            """, (uid,)).fetchall()
        if not rows:
            bot.send_message(call.message.chat.id, "You have no orders yet.")
        else:
            for row in rows:
                bot.send_message(
                    call.message.chat.id,
                    f"Order #{row['id']} — {row['name']} ({row['price']})\n"
                    f"Status: {row['status']}"
                )
        return

    if data.startswith("buy:"):
        try:
            plan_id = int(data.split(":")[1])
        except ValueError:
            return
        with db_lock, db() as con:
            plan = con.execute(
                "SELECT * FROM plans WHERE id=? AND active=1",
                (plan_id,)
            ).fetchone()
            if not plan:
                bot.send_message(call.message.chat.id, "Plan not available.")
                return
            cur = con.execute(
                "INSERT INTO orders(user_id, plan_id) VALUES (?, ?)",
                (uid, plan_id)
            )
            order_id = cur.lastrowid

        text = (
            f"🧾 Order #{order_id}\n"
            f"Plan: {plan['name']}\n"
            f"Price: {plan['price']}\n\n"
            f"{setting('payment_instructions', 'Pay using the QR below.')}\n\n"
            "After payment, tap the button and send your payment screenshot."
        )
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton(
            "📸 Submit Payment Screenshot",
            callback_data=f"paid:{order_id}"
        ))
        qr_id = setting("payment_qr")
        if qr_id:
            bot.send_photo(call.message.chat.id, qr_id, caption=text, reply_markup=kb)
        else:
            bot.send_message(call.message.chat.id, text, reply_markup=kb)
        return

    if data.startswith("paid:"):
        try:
            order_id = int(data.split(":")[1])
        except ValueError:
            return
        with db_lock, db() as con:
            row = con.execute(
                "SELECT * FROM orders WHERE id=? AND user_id=?",
                (order_id, uid)
            ).fetchone()
            if not row or row["status"] != "awaiting_payment":
                bot.send_message(call.message.chat.id, "This order can't accept a screenshot.")
                return
        user_states[uid] = f"screenshot:{order_id}"
        bot.send_message(
            call.message.chat.id,
            "📸 Now send your payment screenshot as a photo."
        )
        return

    if data.startswith("remove:"):
        try:
            plan_id = int(data.split(":")[1])
        except ValueError:
            return
        with db_lock, db() as con:
            con.execute("UPDATE plans SET active=0 WHERE id=?", (plan_id,))
        bot.send_message(call.message.chat.id, "✅ Plan deactivated.")
        return

    if data == "a_add":
        user_states[uid] = "add_plan"
        bot.send_message(
            call.message.chat.id,
            "Send: Name | Price | Duration | Description"
        )
    elif data == "a_remove":
        show_plans_for_removal(call.message.chat.id)
    elif data == "a_caption":
        user_states[uid] = "welcome_caption"
        bot.send_message(call.message.chat.id, "Send the new welcome caption.")
    elif data == "a_image":
        user_states[uid] = "welcome_image"
        bot.send_message(call.message.chat.id, "Send the new welcome image as a photo.")
    elif data == "a_qr":
        user_states[uid] = "payment_qr"
        bot.send_message(call.message.chat.id, "Send your UPI QR as a photo.")
    elif data == "a_instructions":
        user_states[uid] = "payment_instructions"
        bot.send_message(call.message.chat.id, "Send new payment instructions.")
    elif data == "a_list":
        with db_lock, db() as con:
            rows = con.execute(
                "SELECT * FROM plans WHERE active=1 ORDER BY id"
            ).fetchall()
        if not rows:
            bot.send_message(call.message.chat.id, "No active plans.")
        for row in rows:
            bot.send_message(
                call.message.chat.id,
                f"ID: {row['id']} | {row['name']} | {row['price']} | "
                f"{row['duration']}\n{row['description']}"
            )
    elif data == "a_pending":
        show_pending(call.message.chat.id)
    elif data.startswith(("approve:", "reject:")):
        action, raw_id = data.split(":", 1)
        try:
            order_id = int(raw_id)
        except ValueError:
            return

        new_status = "approved" if action == "approve" else "rejected"
        with db_lock, db() as con:
            order = con.execute(
                "SELECT * FROM orders WHERE id=?", (order_id,)
            ).fetchone()
            if not order or order["status"] != "pending":
                bot.send_message(call.message.chat.id, "Order already processed or missing.")
                return
            con.execute(
                "UPDATE orders SET status=? WHERE id=?",
                (new_status, order_id)
            )

        try:
            bot.send_message(
                order["user_id"],
                f"Order #{order_id}: {new_status.upper()}."
            )
        except Exception:
            pass
        bot.send_message(call.message.chat.id, f"Order #{order_id}: {new_status}.")


@bot.message_handler(content_types=["photo"])
def handle_photos(message):
    uid = message.from_user.id
    state = user_states.get(uid)

    if state in ("welcome_image", "payment_qr"):
        if not is_admin(uid):
            return
        file_id = message.photo[-1].file_id
        key = "welcome_image" if state == "welcome_image" else "payment_qr"
        set_setting(key, file_id)
        user_states.pop(uid, None)
        bot.reply_to(message, "✅ Saved successfully.")
        return

    if state and state.startswith("screenshot:"):
        try:
            order_id = int(state.split(":")[1])
        except ValueError:
            user_states.pop(uid, None)
            return

        with db_lock, db() as con:
            order = con.execute(
                "SELECT * FROM orders WHERE id=? AND user_id=?",
                (order_id, uid)
            ).fetchone()
            if not order or order["status"] != "awaiting_payment":
                user_states.pop(uid, None)
                bot.reply_to(message, "This order can't accept a screenshot.")
                return
            con.execute("""
                UPDATE orders
                SET screenshot_id=?, status='pending'
                WHERE id=?
            """, (message.photo[-1].file_id, order_id))
            plan = con.execute(
                "SELECT name, price FROM plans WHERE id=?",
                (order["plan_id"],)
            ).fetchone()

        user_states.pop(uid, None)
        bot.reply_to(message, "✅ Screenshot received. Your order is pending admin verification.")
        bot.send_message(
            ADMIN_ID,
            f"⏳ Payment review required\nOrder #{order_id}\n"
            f"User ID: {uid}\nPlan: {plan['name']}\nPrice: {plan['price']}",
            reply_markup=add_order_buttons(order_id)
        )
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id)
        return

    if is_admin(uid):
        bot.reply_to(message, "Open /admin and choose Welcome Image or Set UPI QR first.")


@bot.message_handler(content_types=["text"])
def handle_text(message):
    uid = message.from_user.id
    state = user_states.get(uid)
    if not state:
        return

    if state in (
        "add_plan", "welcome_caption",
        "payment_instructions"
    ) and not is_admin(uid):
        user_states.pop(uid, None)
        return

    if state == "add_plan":
        parts = [p.strip() for p in message.text.split("|", 3)]
        if len(parts) != 4 or not all(parts[:3]):
            bot.reply_to(
                message,
                "Format: Name | Price | Duration | Description"
            )
            return
        with db_lock, db() as con:
            con.execute(
                "INSERT INTO plans(name, price, duration, description) "
                "VALUES (?, ?, ?, ?)", tuple(parts)
            )
        user_states.pop(uid, None)
        bot.reply_to(message, "✅ Plan added.")
    elif state == "welcome_caption":
        set_setting("welcome_caption", message.text)
        user_states.pop(uid, None)
        bot.reply_to(message, "✅ Welcome caption updated.")
    elif state == "payment_instructions":
        set_setting("payment_instructions", message.text)
        user_states.pop(uid, None)
        bot.reply_to(message, "✅ Payment instructions updated.")
    else:
        bot.reply_to(message, "Please send a photo for this setting.")


init_db()
print("Bot is running...")
bot.infinity_polling(skip_pending=True)
