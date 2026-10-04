import os
import re
import sqlite3
import logging
from contextlib import contextmanager
from urllib.parse import urlparse

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# =========================
# CONFIG (set in Railway Variables)
# BOT_TOKEN, ADMIN_ID, DB_PATH
# =========================
TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_ID_RAW = os.getenv("ADMIN_ID", "").strip()
DB_PATH = os.getenv("DB_PATH", "/data/bot.db")

if not TOKEN:
    raise RuntimeError("Missing BOT_TOKEN environment variable.")
if not ADMIN_ID_RAW.isdigit():
    raise RuntimeError("ADMIN_ID must be your numeric Telegram user ID.")
ADMIN_ID = int(ADMIN_ID_RAW)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
log = logging.getLogger("telegram-plan-bot")
bot = telebot.TeleBot(TOKEN, parse_mode=None, threaded=True)

# Temporary conversation state. If the process restarts mid-form, start again.
states = {}
PAGE_SIZE = 8


# =========================
# DATABASE
# =========================
@contextmanager
def db():
    folder = os.path.dirname(DB_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def columns(con, table):
    return {r["name"] for r in con.execute(f"PRAGMA table_info({table})").fetchall()}


def setup_db():
    with db() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL DEFAULT ''
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL DEFAULT '',
                price TEXT NOT NULL DEFAULT '',
                duration TEXT NOT NULL DEFAULT '',
                description TEXT NOT NULL DEFAULT '',
                image_id TEXT NOT NULL DEFAULT '',
                qr_id TEXT NOT NULL DEFAULT '',
                qr_caption TEXT NOT NULL DEFAULT '',
                active INTEGER NOT NULL DEFAULT 1
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan_id INTEGER NOT NULL,
                screenshot_id TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'awaiting_payment',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Migrate older databases safely.
        pcols = columns(con, "plans")
        for name, sql_type in [
            ("name", "TEXT NOT NULL DEFAULT ''"),
            ("price", "TEXT NOT NULL DEFAULT ''"),
            ("duration", "TEXT NOT NULL DEFAULT ''"),
            ("description", "TEXT NOT NULL DEFAULT ''"),
            ("image_id", "TEXT NOT NULL DEFAULT ''"),
            ("qr_id", "TEXT NOT NULL DEFAULT ''"),
            ("qr_caption", "TEXT NOT NULL DEFAULT ''"),
            ("active", "INTEGER NOT NULL DEFAULT 1"),
        ]:
            if name not in pcols:
                con.execute(f"ALTER TABLE plans ADD COLUMN {name} {sql_type}")

        ocols = columns(con, "orders")
        for name, sql_type in [
            ("user_id", "INTEGER NOT NULL DEFAULT 0"),
            ("plan_id", "INTEGER NOT NULL DEFAULT 0"),
            ("screenshot_id", "TEXT NOT NULL DEFAULT ''"),
            ("status", "TEXT NOT NULL DEFAULT 'awaiting_payment'"),
            ("created_at", "TIMESTAMP"),
        ]:
            if name not in ocols:
                con.execute(f"ALTER TABLE orders ADD COLUMN {name} {sql_type}")


def get_setting(key, default=""):
    with db() as con:
        row = con.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    return row["value"] if row else default


def set_setting(key, value):
    with db() as con:
        con.execute("""
            INSERT INTO settings(key,value) VALUES(?,?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """, (key, value))


def get_plan(plan_id, active_only=False):
    query = "SELECT * FROM plans WHERE id=?"
    if active_only:
        query += " AND active=1"
    with db() as con:
        return con.execute(query, (plan_id,)).fetchone()


def is_admin(user_id):
    return user_id == ADMIN_ID


# =========================
# UI HELPERS
# =========================
def btn(text, callback_data=None, url=None, style=None):
    kwargs = {"text": text}
    if callback_data is not None:
        kwargs["callback_data"] = callback_data
    if url is not None:
        kwargs["url"] = url
    if style:
        try:
            return InlineKeyboardButton(**kwargs, style=style)
        except (TypeError, ValueError):
            pass
    return InlineKeyboardButton(**kwargs)


def safe_add(kb, button):
    kb.add(button)


def home_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(btn("🔄 View Plans", "user:plans", style="primary"))
    demo = get_setting("demo_link")
    if valid_url(demo):
        kb.add(btn("🎬 Demo Channel", url=demo))
    return kb


def valid_url(value):
    try:
        parsed = urlparse((value or "").strip())
        return parsed.scheme in ("https", "http") and bool(parsed.netloc)
    except Exception:
        return False


def user_plans_keyboard():
    kb = InlineKeyboardMarkup()
    with db() as con:
        plans = con.execute(
            "SELECT id,name,price FROM plans WHERE active=1 ORDER BY id"
        ).fetchall()
    colors = ("danger", "success", "primary")
    for i, p in enumerate(plans):
        label = f"{p['name']} — ₹{p['price']}"
        kb.add(btn(label, f"user:plan:{p['id']}", style=colors[i % 3]))
    kb.add(btn("⬅ Main Menu", "user:home"))
    return kb


def admin_home_keyboard():
    kb = InlineKeyboardMarkup()
    kb.row(btn("➕ Add Plan", "admin:add", style="success"),
           btn("📝 Edit Plan", "admin:edit", style="primary"))
    kb.row(btn("🗑 Remove Plan", "admin:remove", style="danger"),
           btn("📋 List Plans", "admin:list"))
    kb.row(btn("🖼 Welcome Settings", "admin:welcome"),
           btn("🔗 Demo Link", "admin:demo"))
    kb.row(btn("💸 Pending Payments", "admin:pending", style="success"))
    kb.row(btn("❌ Cancel Current Step", "admin:cancel", style="danger"))
    return kb


def send_admin_home(chat_id):
    bot.send_message(chat_id, "⚙️ ADMIN PANEL\nChoose an action:", reply_markup=admin_home_keyboard())


def plan_picker(action, active_only=True):
    kb = InlineKeyboardMarkup()
    query = "SELECT id,name,price,active FROM plans"
    if active_only:
        query += " WHERE active=1"
    query += " ORDER BY id DESC LIMIT 80"
    with db() as con:
        plans = con.execute(query).fetchall()
    for p in plans:
        label = f"#{p['id']} {p['name']} — ₹{p['price']}"
        if not p["active"]:
            label += " (inactive)"
        kb.add(btn(label[:60], f"admin:{action}:{p['id']}"))
    kb.add(btn("⬅ Admin Menu", "admin:home"))
    return kb, plans


def send_user_home(chat_id):
    caption = get_setting("welcome_caption", "").strip()
    image = get_setting("welcome_image", "").strip()
    if not caption and not image:
        caption = "Welcome! Choose a plan below."
    if image:
        try:
            bot.send_photo(chat_id, image, caption=caption or "Welcome!")
        except Exception:
            log.exception("Could not send welcome image")
            bot.send_message(chat_id, caption or "Welcome!")
    else:
        bot.send_message(chat_id, caption)
    with db() as con:
        count = con.execute("SELECT COUNT(*) AS n FROM plans WHERE active=1").fetchone()["n"]
    if count:
        bot.send_message(chat_id, "✨ Available Plans", reply_markup=user_plans_keyboard())
    else:
        bot.send_message(chat_id, "Bot not ready — plans have not been configured yet.")


def send_plan(chat_id, plan_id):
    p = get_plan(plan_id, active_only=True)
    if not p:
        bot.send_message(chat_id, "This plan is unavailable.")
        return
    caption = f"{p['name']} — ₹{p['price']}\n\n{p['description']}".strip()
    kb = InlineKeyboardMarkup()
    kb.add(btn("💳 Buy Now", f"user:buy:{plan_id}", style="success"))
    kb.add(btn("⬅ Back to Plans", "user:plans"))
    if p["image_id"]:
        bot.send_photo(chat_id, p["image_id"], caption=caption, reply_markup=kb)
    else:
        bot.send_message(chat_id, caption, reply_markup=kb)


# =========================
# ADMIN FORM HELPERS
# =========================
def ask(chat_id, user_id, state, prompt):
    states[user_id] = {"state": state}
    bot.send_message(chat_id, prompt + "\n\nType /cancel to cancel.")


def cancel_state(user_id):
    states.pop(user_id, None)


def current_state(message):
    return states.get(message.from_user.id, {}).get("state")


def admin_only_callback(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Access denied.", show_alert=True)
        return False
    return True


def start_add_plan(chat_id, user_id):
    states[user_id] = {"state": "add_name", "data": {}}
    bot.send_message(chat_id, "➕ ADD PLAN\nPlan ka naam bhejo.\n\n/cancel to cancel.")


def start_edit_plan(chat_id, user_id, plan_id):
    p = get_plan(plan_id)
    if not p:
        bot.send_message(chat_id, "Plan not found.")
        return
    states[user_id] = {"state": "edit_field", "plan_id": plan_id}
    kb = InlineKeyboardMarkup()
    fields = [
        ("Name", "name"), ("Price", "price"), ("Description/caption", "description"),
        ("Plan image", "image_id"), ("Payment QR image", "qr_id"),
        ("QR caption", "qr_caption"), ("Activate/Deactivate", "active")
    ]
    for label, field in fields:
        kb.add(btn(label, f"admin:editfield:{plan_id}:{field}"))
    kb.add(btn("⬅ Admin Menu", "admin:home"))
    bot.send_message(chat_id, f"Editing: {p['name']} (#{plan_id})\nChoose field:", reply_markup=kb)


def show_order_to_admin(chat_id, order_id):
    with db() as con:
        order = con.execute("""
            SELECT o.*, p.name AS plan_name, p.price AS plan_price
            FROM orders o LEFT JOIN plans p ON p.id=o.plan_id
            WHERE o.id=?
        """, (order_id,)).fetchone()
    if not order:
        return
    caption = (
        f"Payment order #{order['id']}\n"
        f"User ID: {order['user_id']}\n"
        f"Plan: {order['plan_name'] or 'Deleted plan'}\n"
        f"Amount: ₹{order['plan_price'] or '?'}\n"
        f"Status: {order['status']}"
    )
    kb = InlineKeyboardMarkup()
    if order["status"] == "pending":
        kb.row(btn("✅ Approve", f"admin:approve:{order_id}", style="success"),
               btn("❌ Reject", f"admin:reject:{order_id}", style="danger"))
    if order["screenshot_id"]:
        bot.send_photo(chat_id, order["screenshot_id"], caption=caption, reply_markup=kb if order["status"] == "pending" else None)
    else:
        bot.send_message(chat_id, caption, reply_markup=kb if order["status"] == "pending" else None)


# =========================
# COMMANDS
# =========================
@bot.message_handler(commands=["start"])
def cmd_start(message):
    cancel_state(message.from_user.id)
    send_user_home(message.chat.id)


@bot.message_handler(commands=["admin"])
def cmd_admin(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "⛔ Access denied.")
        return
    cancel_state(message.from_user.id)
    send_admin_home(message.chat.id)


@bot.message_handler(commands=["cancel"])
def cmd_cancel(message):
    cancel_state(message.from_user.id)
    bot.reply_to(message, "Cancelled.")
    if is_admin(message.from_user.id):
        send_admin_home(message.chat.id)


# =========================
# CALLBACKS
# =========================
@bot.callback_query_handler(func=lambda c: c.data == "user:home")
def cb_user_home(call):
    bot.answer_callback_query(call.id)
    cancel_state(call.from_user.id)
    send_user_home(call.message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data == "user:plans")
def cb_user_plans(call):
    bot.answer_callback_query(call.id)
    cancel_state(call.from_user.id)
    with db() as con:
        count = con.execute("SELECT COUNT(*) AS n FROM plans WHERE active=1").fetchone()["n"]
    if not count:
        bot.send_message(call.message.chat.id, "No plans are available yet.")
    else:
        bot.send_message(call.message.chat.id, "✨ Available Plans", reply_markup=user_plans_keyboard())


@bot.callback_query_handler(func=lambda c: c.data.startswith("user:plan:"))
def cb_user_plan(call):
    bot.answer_callback_query(call.id)
    cancel_state(call.from_user.id)
    try:
        plan_id = int(call.data.rsplit(":", 1)[1])
        send_plan(call.message.chat.id, plan_id)
    except (ValueError, IndexError):
        bot.send_message(call.message.chat.id, "Invalid plan.")


@bot.callback_query_handler(func=lambda c: c.data.startswith("user:buy:"))
def cb_user_buy(call):
    bot.answer_callback_query(call.id)
    try:
        plan_id = int(call.data.rsplit(":", 1)[1])
    except (ValueError, IndexError):
        bot.send_message(call.message.chat.id, "Invalid plan.")
        return
    p = get_plan(plan_id, active_only=True)
    if not p:
        bot.send_message(call.message.chat.id, "This plan is unavailable.")
        return
    if not p["qr_id"]:
        bot.send_message(call.message.chat.id, "Payment QR is not set yet. Please contact the admin.")
        return
    with db() as con:
        cur = con.execute(
            "INSERT INTO orders(user_id,plan_id,status) VALUES(?,?,?)",
            (call.from_user.id, plan_id, "awaiting_payment")
        )
        order_id = cur.lastrowid
    kb = InlineKeyboardMarkup()
    kb.add(btn("📸 Submit Payment Screenshot", f"user:submit:{order_id}", style="success"))
    kb.add(btn("⬅ Back to Plan", f"user:plan:{plan_id}"))
    bot.send_photo(
        call.message.chat.id,
        p["qr_id"],
        caption=p["qr_caption"] or f"Pay ₹{p['price']} using this QR.\nOrder #{order_id}",
        reply_markup=kb
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("user:submit:"))
def cb_user_submit(call):
    bot.answer_callback_query(call.id)
    try:
        order_id = int(call.data.rsplit(":", 1)[1])
    except (ValueError, IndexError):
        bot.send_message(call.message.chat.id, "Invalid order.")
        return
    with db() as con:
        order = con.execute(
            "SELECT id FROM orders WHERE id=? AND user_id=? AND status='awaiting_payment'",
            (order_id, call.from_user.id)
        ).fetchone()
    if not order:
        bot.send_message(call.message.chat.id, "This order is no longer awaiting a screenshot.")
        return
    states[call.from_user.id] = {"state": "payment_screenshot", "order_id": order_id}
    bot.send_message(call.message.chat.id, "Ab payment screenshot PHOTO ke roop mein bhejo. Screenshot bhejne ke baad admin manually verify karega.")


# Admin home/menu
@bot.callback_query_handler(func=lambda c: c.data == "admin:home")
def cb_admin_home(call):
    if not admin_only_callback(call):
        return
    bot.answer_callback_query(call.id)
    cancel_state(call.from_user.id)
    send_admin_home(call.message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data == "admin:cancel")
def cb_admin_cancel(call):
    if not admin_only_callback(call):
        return
    bot.answer_callback_query(call.id)
    cancel_state(call.from_user.id)
    send_admin_home(call.message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data == "admin:add")
def cb_admin_add(call):
    if not admin_only_callback(call):
        return
    bot.answer_callback_query(call.id)
    start_add_plan(call.message.chat.id, call.from_user.id)


@bot.callback_query_handler(func=lambda c: c.data == "admin:edit")
def cb_admin_edit(call):
    if not admin_only_callback(call):
        return
    bot.answer_callback_query(call.id)
    kb, plans = plan_picker("editpick", active_only=False)
    bot.send_message(call.message.chat.id, "Choose a plan to edit:", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data == "admin:remove")
def cb_admin_remove(call):
    if not admin_only_callback(call):
        return
    bot.answer_callback_query(call.id)
    kb, plans = plan_picker("removepick", active_only=True)
    if not plans:
        bot.send_message(call.message.chat.id, "No active plans.")
        return
    bot.send_message(call.message.chat.id, "Choose a plan to deactivate:", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data == "admin:list")
def cb_admin_list(call):
    if not admin_only_callback(call):
        return
    bot.answer_callback_query(call.id)
    with db() as con:
        plans = con.execute("SELECT * FROM plans ORDER BY id DESC LIMIT 80").fetchall()
    if not plans:
        bot.send_message(call.message.chat.id, "No plans yet. Use Add Plan.")
        return
    for p in plans:
        status = "ACTIVE" if p["active"] else "INACTIVE"
        bot.send_message(call.message.chat.id, f"#{p['id']} {p['name']} — ₹{p['price']} [{status}]")


@bot.callback_query_handler(func=lambda c: c.data == "admin:welcome")
def cb_admin_welcome(call):
    if not admin_only_callback(call):
        return
    bot.answer_callback_query(call.id)
    kb = InlineKeyboardMarkup()
    kb.add(btn("Set welcome caption", "admin:welcomecaption"))
    kb.add(btn("Set welcome image", "admin:welcomeimage"))
    kb.add(btn("Clear welcome image", "admin:clearwelcomeimage", style="danger"))
    kb.add(btn("⬅ Admin Menu", "admin:home"))
    bot.send_message(call.message.chat.id, "Welcome settings:", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data == "admin:welcomecaption")
def cb_welcome_caption(call):
    if not admin_only_callback(call):
        return
    bot.answer_callback_query(call.id)
    ask(call.message.chat.id, call.from_user.id, "welcome_caption", "New welcome caption bhejo (plain text).")


@bot.callback_query_handler(func=lambda c: c.data == "admin:welcomeimage")
def cb_welcome_image(call):
    if not admin_only_callback(call):
        return
    bot.answer_callback_query(call.id)
    ask(call.message.chat.id, call.from_user.id, "welcome_image", "Welcome image as a PHOTO bhejo.")


@bot.callback_query_handler(func=lambda c: c.data == "admin:clearwelcomeimage")
def cb_clear_welcome_image(call):
    if not admin_only_callback(call):
        return
    set_setting("welcome_image", "")
    bot.answer_callback_query(call.id, "Welcome image cleared.")
    bot.send_message(call.message.chat.id, "Welcome image cleared.")


@bot.callback_query_handler(func=lambda c: c.data == "admin:demo")
def cb_admin_demo(call):
    if not admin_only_callback(call):
        return
    bot.answer_callback_query(call.id)
    kb = InlineKeyboardMarkup()
    kb.add(btn("Set/change demo link", "admin:setdemo"))
    kb.add(btn("Clear demo link", "admin:cleardemo", style="danger"))
    kb.add(btn("⬅ Admin Menu", "admin:home"))
    bot.send_message(call.message.chat.id, "Demo channel settings:", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data == "admin:setdemo")
def cb_set_demo(call):
    if not admin_only_callback(call):
        return
    bot.answer_callback_query(call.id)
    ask(call.message.chat.id, call.from_user.id, "demo_link", "Demo channel ka full https:// link bhejo.")


@bot.callback_query_handler(func=lambda c: c.data == "admin:cleardemo")
def cb_clear_demo(call):
    if not admin_only_callback(call):
        return
    set_setting("demo_link", "")
    bot.answer_callback_query(call.id, "Demo link cleared.")
    bot.send_message(call.message.chat.id, "Demo link cleared.")


@bot.callback_query_handler(func=lambda c: c.data.startswith("admin:editpick:"))
def cb_edit_pick(call):
    if not admin_only_callback(call):
        return
    bot.answer_callback_query(call.id)
    try:
        plan_id = int(call.data.rsplit(":", 1)[1])
        start_edit_plan(call.message.chat.id, call.from_user.id, plan_id)
    except (ValueError, IndexError):
        bot.send_message(call.message.chat.id, "Invalid plan.")


@bot.callback_query_handler(func=lambda c: c.data.startswith("admin:removepick:"))
def cb_remove_pick(call):
    if not admin_only_callback(call):
        return
    try:
        plan_id = int(call.data.rsplit(":", 1)[1])
    except (ValueError, IndexError):
        bot.answer_callback_query(call.id, "Invalid plan.")
        return
    with db() as con:
        con.execute("UPDATE plans SET active=0 WHERE id=?", (plan_id,))
    bot.answer_callback_query(call.id, "Plan deactivated.")
    bot.send_message(call.message.chat.id, f"Plan #{plan_id} deactivated. Old orders are preserved.")


@bot.callback_query_handler(func=lambda c: c.data.startswith("admin:editfield:"))
def cb_edit_field(call):
    if not admin_only_callback(call):
        return
    parts = call.data.split(":")
    if len(parts) != 4:
        bot.answer_callback_query(call.id, "Invalid selection.")
        return
    try:
        plan_id = int(parts[2])
    except ValueError:
        bot.answer_callback_query(call.id, "Invalid plan.")
        return
    field = parts[3]
    allowed = {
        "name": ("edit_name", "New plan name bhejo."),
        "price": ("edit_price", "New price bhejo (numbers, e.g. 199)."),
        "description": ("edit_description", "New plan caption/description bhejo."),
        "image_id": ("edit_image", "New plan image as PHOTO bhejo."),
        "qr_id": ("edit_qr", "New payment QR image as PHOTO bhejo."),
        "qr_caption": ("edit_qr_caption", "New caption under QR bhejo."),
        "active": ("edit_active", "Plan activate karne ke liye 1 ya deactivate karne ke liye 0 bhejo.")
    }
    if field not in allowed:
        bot.answer_callback_query(call.id, "Invalid field.")
        return
    bot.answer_callback_query(call.id)
    state, prompt = allowed[field]
    states[call.from_user.id] = {"state": state, "plan_id": plan_id}
    bot.send_message(call.message.chat.id, prompt + "\n\n/cancel to cancel.")


@bot.callback_query_handler(func=lambda c: c.data == "admin:pending")
def cb_admin_pending(call):
    if not admin_only_callback(call):
        return
    bot.answer_callback_query(call.id)
    with db() as con:
        orders = con.execute("""
            SELECT id FROM orders WHERE status='pending' ORDER BY id DESC LIMIT 30
        """).fetchall()
    if not orders:
        bot.send_message(call.message.chat.id, "No pending payments right now.")
        return
    for row in orders:
        show_order_to_admin(call.message.chat.id, row["id"])


@bot.callback_query_handler(func=lambda c: c.data.startswith("admin:approve:") or c.data.startswith("admin:reject:"))
def cb_review_order(call):
    if not admin_only_callback(call):
        return
    action, order_id_text = call.data.split(":")[1], call.data.split(":")[2]
    try:
        order_id = int(order_id_text)
    except ValueError:
        bot.answer_callback_query(call.id, "Invalid order.")
        return
    new_status = "approved" if action == "approve" else "rejected"
    with db() as con:
        order = con.execute(
            "SELECT user_id,status FROM orders WHERE id=?", (order_id,)
        ).fetchone()
        if not order or order["status"] != "pending":
            bot.answer_callback_query(call.id, "Order missing or already reviewed.", show_alert=True)
            return
        con.execute("UPDATE orders SET status=? WHERE id=?", (new_status, order_id))
    bot.answer_callback_query(call.id, "Saved.")
    try:
        message = (
            f"✅ Payment for order #{order_id} approved."
            if new_status == "approved"
            else f"❌ Payment for order #{order_id} was rejected. Please contact the admin."
        )
        bot.send_message(order["user_id"], message)
    except Exception:
        log.exception("Could not notify user for order %s", order_id)
    bot.send_message(call.message.chat.id, f"Order #{order_id} marked {new_status}.")


# =========================
# TEXT / PHOTO FORM HANDLER
# =========================
@bot.message_handler(content_types=["text", "photo"])
def handle_form_input(message):
    user_id = message.from_user.id
    state_info = states.get(user_id)
    if not state_info:
        return

    state = state_info.get("state")
    if message.content_type == "text" and message.text and message.text.strip().lower() == "/cancel":
        cancel_state(user_id)
        bot.reply_to(message, "Cancelled.")
        if is_admin(user_id):
            send_admin_home(message.chat.id)
        return

    # Payment screenshot submission
    if state == "payment_screenshot":
        if message.content_type != "photo":
            bot.reply_to(message, "Please send the screenshot as a photo.")
            return
        order_id = state_info["order_id"]
        screenshot_id = message.photo[-1].file_id
        with db() as con:
            cur = con.execute("""
                UPDATE orders SET screenshot_id=?,status='pending'
                WHERE id=? AND user_id=? AND status='awaiting_payment'
            """, (screenshot_id, order_id, user_id))
            changed = cur.rowcount
            order = con.execute("""
                SELECT o.id,o.user_id,o.plan_id,p.name,p.price
                FROM orders o LEFT JOIN plans p ON p.id=o.plan_id WHERE o.id=?
            """, (order_id,)).fetchone()
        cancel_state(user_id)
        if not changed:
            bot.reply_to(message, "This order is no longer awaiting a screenshot. Start Buy Now again.")
            return
        bot.reply_to(message, "📨 Screenshot received. Admin will verify the payment manually.")
        try:
            caption = (
                f"💸 PAYMENT REVIEW — Order #{order_id}\n"
                f"User ID: {user_id}\n"
                f"Plan: {order['name'] or 'Unavailable'}\n"
                f"Amount: ₹{order['price'] or '?'}"
            )
            kb = InlineKeyboardMarkup()
            kb.row(btn("✅ Approve", f"admin:approve:{order_id}", style="success"),
                   btn("❌ Reject", f"admin:reject:{order_id}", style="danger"))
            bot.send_photo(ADMIN_ID, screenshot_id, caption=caption, reply_markup=kb)
        except Exception:
            log.exception("Failed to send order to admin")
            bot.send_message(message.chat.id, "Screenshot saved, but admin notification failed. Please tell the admin.")
        return

    # Only admin can change settings/plans.
    if not is_admin(user_id):
        cancel_state(user_id)
        return

    # Settings forms
    if state == "welcome_caption":
        if message.content_type != "text":
            bot.reply_to(message, "Please send the caption as text.")
            return
        set_setting("welcome_caption", message.text)
        cancel_state(user_id)
        bot.reply_to(message, "✅ Welcome caption saved to database.")
        return

    if state == "welcome_image":
        if message.content_type != "photo":
            bot.reply_to(message, "Please send the image as a photo.")
            return
        set_setting("welcome_image", message.photo[-1].file_id)
        cancel_state(user_id)
        bot.reply_to(message, "✅ Welcome image saved to database.")
        return

    if state == "demo_link":
        if message.content_type != "text" or not valid_url(message.text.strip()):
            bot.reply_to(message, "A valid full URL bhejo, e.g. https://t.me/yourchannel")
            return
        set_setting("demo_link", message.text.strip())
        cancel_state(user_id)
        bot.reply_to(message, "✅ Demo link saved.")
        return

    # Add-plan wizard
    if state.startswith("add_"):
        if message.content_type != "text" and state not in ("add_image", "add_qr"):
            bot.reply_to(message, "Please send text for this step.")
            return
        data = state_info.setdefault("data", {})
        if state == "add_name":
            value = message.text.strip()
            if not value:
                bot.reply_to(message, "Plan name cannot be empty.")
                return
            data["name"] = value[:100]
            states[user_id]["state"] = "add_price"
            bot.send_message(message.chat.id, "Plan price/amount bhejo (e.g. 199).")
        elif state == "add_price":
            value = message.text.strip()
            if not re.fullmatch(r"\d{1,9}(?:\.\d{1,2})?", value):
                bot.reply_to(message, "Valid amount bhejo, e.g. 199 or 199.50.")
                return
            data["price"] = value
            states[user_id]["state"] = "add_description"
            bot.send_message(message.chat.id, "Plan ka caption/description bhejo. Skip karne ke liye /skip.")
        elif state == "add_description":
            data["description"] = "" if message.text.strip() == "/skip" else message.text[:3500]
            states[user_id]["state"] = "add_image"
            bot.send_message(message.chat.id, "Plan image PHOTO bhejo, ya skip karne ke liye /skip.")
        elif state == "add_image":
            if message.content_type == "photo":
                data["image_id"] = message.photo[-1].file_id
            elif message.content_type == "text" and message.text.strip() == "/skip":
                data["image_id"] = ""
            else:
                bot.reply_to(message, "Plan image PHOTO bhejo ya /skip.")
                return
            states[user_id]["state"] = "add_qr"
            bot.send_message(message.chat.id, "Is plan ka payment QR PHOTO bhejo.")
        elif state == "add_qr":
            if message.content_type != "photo":
                bot.reply_to(message, "Payment QR ko PHOTO ke roop mein bhejo.")
                return
            data["qr_id"] = message.photo[-1].file_id
            states[user_id]["state"] = "add_qr_caption"
            bot.send_message(message.chat.id, "QR ke neeche dikhne wala caption bhejo, ya /skip.")
        elif state == "add_qr_caption":
            data["qr_caption"] = "" if message.text.strip() == "/skip" else message.text[:1000]
            with db() as con:
                cur = con.execute("""
                    INSERT INTO plans(name,price,duration,description,image_id,qr_id,qr_caption,active)
                    VALUES(?,?,?, ?,?,?,?,1)
                """, (
                    data["name"], data["price"], data.get("duration", ""), data.get("description", ""),
                    data.get("image_id", ""), data["qr_id"], data.get("qr_caption", "")
                ))
                plan_id = cur.lastrowid
            cancel_state(user_id)
            bot.send_message(message.chat.id, f"✅ Plan created and saved! Plan ID: #{plan_id}")
            send_admin_home(message.chat.id)
        return

    # Edit existing plan
    if state.startswith("edit_"):
        plan_id = state_info.get("plan_id")
        p = get_plan(plan_id)
        if not p:
            cancel_state(user_id)
            bot.reply_to(message, "Plan not found. Please start again.")
            return
        if state == "edit_name":
            if message.content_type != "text" or not message.text.strip():
                bot.reply_to(message, "Send a non-empty plan name.")
                return
            value = message.text.strip()[:100]
            field = "name"
        elif state == "edit_price":
            if message.content_type != "text" or not re.fullmatch(r"\d{1,9}(?:\.\d{1,2})?", message.text.strip()):
                bot.reply_to(message, "Send a valid amount, e.g. 199.")
                return
            value = message.text.strip()
            field = "price"
        elif state == "edit_description":
            if message.content_type != "text":
                bot.reply_to(message, "Send the caption as text.")
                return
            value = message.text[:3500]
            field = "description"
        elif state == "edit_image":
            if message.content_type != "photo":
                bot.reply_to(message, "Send the new plan image as a PHOTO.")
                return
            value = message.photo[-1].file_id
            field = "image_id"
        elif state == "edit_qr":
            if message.content_type != "photo":
                bot.reply_to(message, "Send the new QR as a PHOTO.")
                return
            value = message.photo[-1].file_id
            field = "qr_id"
        elif state == "edit_qr_caption":
            if message.content_type != "text":
                bot.reply_to(message, "Send QR caption as text.")
                return
            value = message.text[:1000]
            field = "qr_caption"
        elif state == "edit_active":
            if message.content_type != "text" or message.text.strip() not in ("0", "1"):
                bot.reply_to(message, "Send 1 to activate or 0 to deactivate.")
                return
            value = int(message.text.strip())
            field = "active"
        else:
            return
        with db() as con:
            con.execute(f"UPDATE plans SET {field}=? WHERE id=?", (value, plan_id))
        cancel_state(user_id)
        bot.reply_to(message, f"✅ Plan #{plan_id} updated and saved.")
        start_edit_plan(message.chat.id, user_id, plan_id)
        return


# Skip command is processed inside the wizard; handler for text reaches form handler.
@bot.message_handler(commands=["skip"])
def cmd_skip(message):
    info = states.get(message.from_user.id)
    if not info or info.get("state") not in ("add_description", "add_image", "add_qr_caption"):
        bot.reply_to(message, "Nothing to skip right now.")
        return
    # For QR, skipping would make checkout unusable, so do not allow it.
    if info["state"] == "add_qr_caption":
        bot.reply_to(message, "QR caption skip is available: send /skip again in the current QR-caption step.")
        # This command handler intentionally leaves state intact. Text form handler normally handles /skip.
        # We set empty caption and save the plan here so the command does not get swallowed by command routing.
        data = info.get("data", {})
        with db() as con:
            cur = con.execute("""
                INSERT INTO plans(name,price,duration,description,image_id,qr_id,qr_caption,active)
                VALUES(?,?,?, ?,?,?,?,1)
            """, (data.get("name",""), data.get("price",""), data.get("duration",""), data.get("description",""),
                  data.get("image_id",""), data.get("qr_id",""), ""))
            plan_id = cur.lastrowid
        cancel_state(message.from_user.id)
        bot.send_message(message.chat.id, f"✅ Plan created and saved! Plan ID: #{plan_id}")
        send_admin_home(message.chat.id)
        return
    # Let the regular handler's logic be applied directly for other skip steps.
    if info["state"] == "add_description":
        info.setdefault("data", {})["description"] = ""
        info["state"] = "add_image"
        bot.reply_to(message, "Description skipped. Plan image PHOTO bhejo, ya /skip.")
    elif info["state"] == "add_image":
        info.setdefault("data", {})["image_id"] = ""
        info["state"] = "add_qr"
        bot.reply_to(message, "Plan image skipped. Ab payment QR PHOTO bhejo.")


if __name__ == "__main__":
    setup_db()
    log.info("Bot starting. DB_PATH=%s", DB_PATH)
    # Run exactly one polling instance for this bot token.
    bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=25)
