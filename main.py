mport os
import re
import json
import sqlite3
import logging
from contextlib import contextmanager
from urllib.parse import urlparse

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, MessageEntity

# Railway Variables:
# BOT_TOKEN, ADMIN_ID, DB_PATH=/data/bot.db
TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_RAW = os.getenv("ADMIN_ID", "").strip()
DB_PATH = os.getenv("DB_PATH", "/data/bot.db")

if not TOKEN:
    raise RuntimeError("Set BOT_TOKEN in Railway Variables.")
if not ADMIN_RAW.isdigit():
    raise RuntimeError("Set ADMIN_ID to your numeric Telegram user ID.")
ADMIN_ID = int(ADMIN_RAW)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("planbot")
bot = telebot.TeleBot(TOKEN)
states = {}
COLORS = ("danger", "success", "primary")


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


def setup_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS settings(
            key TEXT PRIMARY KEY, value TEXT NOT NULL DEFAULT '')""")
        con.execute("""CREATE TABLE IF NOT EXISTS plans(
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
            price TEXT NOT NULL, description TEXT NOT NULL DEFAULT '',
            description_entities TEXT NOT NULL DEFAULT '[]',
            image_id TEXT NOT NULL DEFAULT '', qr_id TEXT NOT NULL DEFAULT '',
            qr_caption TEXT NOT NULL DEFAULT '', qr_entities TEXT NOT NULL DEFAULT '[]',
            active INTEGER NOT NULL DEFAULT 1)""")
        con.execute("""CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
            plan_id INTEGER NOT NULL, screenshot_id TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'awaiting_payment',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        # Safe migrations for older versions of this bot.
        for table, needed in {
            "plans": {
                "name": "TEXT NOT NULL DEFAULT ''", "price": "TEXT NOT NULL DEFAULT ''",
                "description": "TEXT NOT NULL DEFAULT ''", "description_entities": "TEXT NOT NULL DEFAULT '[]'",
                "image_id": "TEXT NOT NULL DEFAULT ''", "qr_id": "TEXT NOT NULL DEFAULT ''",
                "qr_caption": "TEXT NOT NULL DEFAULT ''", "qr_entities": "TEXT NOT NULL DEFAULT '[]'",
                "active": "INTEGER NOT NULL DEFAULT 1"},
            "orders": {
                "user_id": "INTEGER NOT NULL DEFAULT 0", "plan_id": "INTEGER NOT NULL DEFAULT 0",
                "screenshot_id": "TEXT NOT NULL DEFAULT ''",
                "status": "TEXT NOT NULL DEFAULT 'awaiting_payment'",
                "created_at": "TIMESTAMP"}
        }.items():
            existing = {r["name"] for r in con.execute(f"PRAGMA table_info({table})")}
            for col, spec in needed.items():
                if col not in existing:
                    con.execute(f"ALTER TABLE {table} ADD COLUMN {col} {spec}")


def setting(key, default=""):
    with db() as con:
        row = con.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    return row["value"] if row else default


def set_setting(key, value):
    with db() as con:
        con.execute("""INSERT INTO settings(key,value) VALUES(?,?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value""", (key, value))


def is_admin(uid):
    return uid == ADMIN_ID


def valid_url(value):
    try:
        p = urlparse((value or "").strip())
        return p.scheme in ("https", "http") and bool(p.netloc)
    except Exception:
        return False


def entity_data(entities):
    out = []
    for e in entities or []:
        if getattr(e, "type", None) == "custom_emoji" and getattr(e, "custom_emoji_id", None):
            out.append({
                "type": "custom_emoji", "offset": e.offset, "length": e.length,
                "custom_emoji_id": e.custom_emoji_id
            })
    return out


def entities_from_json(raw):
    result = []
    try:
        for e in json.loads(raw or "[]"):
            result.append(MessageEntity(
                type="custom_emoji", offset=int(e["offset"]), length=int(e["length"]),
                custom_emoji_id=str(e["custom_emoji_id"])
            ))
    except Exception:
        log.exception("Could not restore message entities")
    return result


def btn(text, data=None, url=None, style=None, icon_id=None):
    args = {"text": text}
    if data is not None:
        args["callback_data"] = data
    if url is not None:
        args["url"] = url
    # Custom emoji icons are optional Bot API support; fall back gracefully.
    if icon_id:
        try:
            return InlineKeyboardButton(**args, style=style, icon_custom_emoji_id=icon_id)
        except (TypeError, ValueError):
            pass
    if style:
        try:
            return InlineKeyboardButton(**args, style=style)
        except (TypeError, ValueError):
            pass
    return InlineKeyboardButton(**args)


def custom_button_id():
    return setting("button_emoji_id", "")


def admin_kb():
    kb = InlineKeyboardMarkup()
    kb.row(btn("➕ Add plan", "a:add", style="success"),
           btn("✏️ Edit plan", "a:edit", style="primary"))
    kb.row(btn("🗑 Remove plan", "a:remove", style="danger"),
           btn("📋 List plans", "a:list"))
    kb.row(btn("🖼 Welcome", "a:welcome"),
           btn("🔗 Demo link", "a:demo"))
    kb.row(btn("✨ Save Premium emoji text", "a:emoji"),
           btn("💳 Pending payments", "a:pending", style="success"))
    kb.add(btn("❌ Cancel current step", "a:cancel", style="danger"))
    return kb


def send_admin(chat_id):
    bot.send_message(chat_id, "⚙️ ADMIN PANEL\nChoose an action:", reply_markup=admin_kb())


def get_plan(pid, active_only=False):
    q = "SELECT * FROM plans WHERE id=?"
    if active_only:
        q += " AND active=1"
    with db() as con:
        return con.execute(q, (pid,)).fetchone()


def list_plan_keyboard(action, active_only=True):
    q = "SELECT id,name,price,active FROM plans"
    if active_only:
        q += " WHERE active=1"
    q += " ORDER BY id DESC LIMIT 80"
    with db() as con:
        rows = con.execute(q).fetchall()
    kb = InlineKeyboardMarkup()
    for row in rows:
        kb.add(btn(f"#{row['id']} {row['name']} — ₹{row['price']}"[:60],
                   f"a:{action}:{row['id']}"))
    kb.add(btn("⬅ Admin menu", "a:home"))
    return kb, rows


def user_plans_kb():
    kb = InlineKeyboardMarkup()
    with db() as con:
        rows = con.execute("SELECT id,name,price FROM plans WHERE active=1 ORDER BY id").fetchall()
    icon = custom_button_id()
    for i, row in enumerate(rows):
        kb.add(btn(f"{row['name']} — ₹{row['price']}", f"u:plan:{row['id']}",
                   style=COLORS[i % 3], icon_id=icon))
    demo = setting("demo_link")
    if valid_url(demo):
        kb.add(btn("🎬 Demo Channel", url=demo))
    kb.add(btn("⬅ Main menu", "u:home"))
    return kb


def send_home(chat_id):
    caption = setting("welcome_caption", "Welcome! Choose a plan below.")
    photo = setting("welcome_image")
    entities = entities_from_json(setting("welcome_entities", "[]"))
    if photo:
        try:
            bot.send_photo(chat_id, photo, caption=caption, caption_entities=entities or None)
        except Exception:
            log.exception("Welcome photo send failed; sending text instead")
            bot.send_message(chat_id, caption, entities=entities or None)
    else:
        bot.send_message(chat_id, caption, entities=entities or None)
    with db() as con:
        count = con.execute("SELECT COUNT(*) n FROM plans WHERE active=1").fetchone()["n"]
    if count:
        bot.send_message(chat_id, "✨ Available plans:", reply_markup=user_plans_kb())
    else:
        bot.send_message(chat_id, "Bot not ready — admin has not added plans yet.")


def send_plan(chat_id, pid):
    p = get_plan(pid, True)
    if not p:
        bot.send_message(chat_id, "Plan unavailable.")
        return
    caption = f"{p['name']} — ₹{p['price']}\n\n{p['description']}".strip()
    entities = entities_from_json(p["description_entities"])
    # Entities from description are for description-only text; combined prefix shifts offsets.
    # Keep custom entities for exact text by storing and sending the description as its own message if needed.
    kb = InlineKeyboardMarkup()
    kb.add(btn("💳 Buy now", f"u:buy:{pid}", style="success", icon_id=custom_button_id()))
    kb.add(btn("⬅ Back to plans", "u:plans"))
    if p["image_id"]:
        # Avoid applying stale offsets after prefix is added.
        bot.send_photo(chat_id, p["image_id"], caption=caption, reply_markup=kb)
    else:
        bot.send_message(chat_id, caption, reply_markup=kb)


def prompt(chat_id, uid, state, message, **extra):
    states[uid] = {"state": state, **extra}
    bot.send_message(chat_id, message + "\n\nSend /cancel to cancel.")


def admin_callback(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "Access denied.", show_alert=True)
        return False
    return True


@bot.message_handler(commands=["start"])
def start(message):
    states.pop(message.from_user.id, None)
    send_home(message.chat.id)


@bot.message_handler(commands=["admin"])
def admin(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "⛔ Access denied.")
        return
    states.pop(message.from_user.id, None)
    send_admin(message.chat.id)


@bot.message_handler(commands=["cancel"])
def cancel(message):
    states.pop(message.from_user.id, None)
    bot.reply_to(message, "Cancelled.")
    if is_admin(message.from_user.id):
        send_admin(message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data == "u:home")
def user_home(call):
    bot.answer_callback_query(call.id)
    states.pop(call.from_user.id, None)
    send_home(call.message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data == "u:plans")
def user_plans(call):
    bot.answer_callback_query(call.id)
    states.pop(call.from_user.id, None)
    with db() as con:
        n = con.execute("SELECT COUNT(*) n FROM plans WHERE active=1").fetchone()["n"]
    if n:
        bot.send_message(call.message.chat.id, "✨ Available plans:", reply_markup=user_plans_kb())
    else:
        bot.send_message(call.message.chat.id, "No plans available yet.")


@bot.callback_query_handler(func=lambda c: c.data.startswith("u:plan:"))
def user_plan(call):
    bot.answer_callback_query(call.id)
    try:
        send_plan(call.message.chat.id, int(call.data.rsplit(":", 1)[1]))
    except ValueError:
        bot.send_message(call.message.chat.id, "Invalid plan.")


@bot.callback_query_handler(func=lambda c: c.data.startswith("u:buy:"))
def user_buy(call):
    bot.answer_callback_query(call.id)
    try:
        pid = int(call.data.rsplit(":", 1)[1])
    except ValueError:
        return
    p = get_plan(pid, True)
    if not p:
        bot.send_message(call.message.chat.id, "Plan unavailable.")
        return
    if not p["qr_id"]:
        bot.send_message(call.message.chat.id, "Payment QR is not set. Contact admin.")
        return
    with db() as con:
        cur = con.execute("INSERT INTO orders(user_id,plan_id,status) VALUES(?,?,?)",
                          (call.from_user.id, pid, "awaiting_payment"))
        oid = cur.lastrowid
    kb = InlineKeyboardMarkup()
    kb.add(btn("📸 Submit payment screenshot", f"u:submit:{oid}", style="success"))
    kb.add(btn("⬅ Back to plan", f"u:plan:{pid}"))
    bot.send_photo(call.message.chat.id, p["qr_id"],
                   caption=p["qr_caption"] or f"Pay ₹{p['price']} using this QR. Order #{oid}",
                   caption_entities=entities_from_json(p["qr_entities"]) or None,
                   reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith("u:submit:"))
def user_submit(call):
    bot.answer_callback_query(call.id)
    try:
        oid = int(call.data.rsplit(":", 1)[1])
    except ValueError:
        return
    with db() as con:
        row = con.execute("SELECT id FROM orders WHERE id=? AND user_id=? AND status='awaiting_payment'",
                          (oid, call.from_user.id)).fetchone()
    if not row:
        bot.send_message(call.message.chat.id, "Order not found or already submitted.")
        return
    states[call.from_user.id] = {"state": "payment_screenshot", "order_id": oid}
    bot.send_message(call.message.chat.id, "Payment screenshot ko PHOTO ke roop mein bhejo. Admin payment manually verify karega.")


@bot.callback_query_handler(func=lambda c: c.data == "a:home")
def admin_home_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    states.pop(call.from_user.id, None)
    send_admin(call.message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data == "a:cancel")
def admin_cancel_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    states.pop(call.from_user.id, None)
    send_admin(call.message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data == "a:add")
def add_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    states[call.from_user.id] = {"state": "add_name", "data": {}}
    bot.send_message(call.message.chat.id, "➕ Add plan: plan name bhejo.")


@bot.callback_query_handler(func=lambda c: c.data == "a:edit")
def edit_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    kb, rows = list_plan_keyboard("editpick", False)
    bot.send_message(call.message.chat.id, "Choose a plan to edit:", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data == "a:remove")
def remove_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    kb, rows = list_plan_keyboard("removepick", True)
    bot.send_message(call.message.chat.id, "Choose plan to deactivate:", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data == "a:list")
def list_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    with db() as con:
        rows = con.execute("SELECT id,name,price,active FROM plans ORDER BY id DESC LIMIT 80").fetchall()
    if not rows:
        bot.send_message(call.message.chat.id, "No plans yet. Tap Add plan.")
    for p in rows:
        bot.send_message(call.message.chat.id, f"#{p['id']} {p['name']} — ₹{p['price']} — {'active' if p['active'] else 'inactive'}")


@bot.callback_query_handler(func=lambda c: c.data == "a:welcome")
def welcome_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    kb = InlineKeyboardMarkup()
    kb.add(btn("Set welcome caption + emoji", "a:welcometext"))
    kb.add(btn("Set welcome image", "a:welcomeimage"))
    kb.add(btn("Clear welcome image", "a:clearwelcome"))
    kb.add(btn("⬅ Admin menu", "a:home"))
    bot.send_message(call.message.chat.id, "Welcome settings:", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data == "a:welcometext")
def welcome_text_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    prompt(call.message.chat.id, call.from_user.id, "welcome_text",
           "Send the full welcome text with Premium custom emoji(s). The bot saves custom emoji IDs automatically.")


@bot.callback_query_handler(func=lambda c: c.data == "a:welcomeimage")
def welcome_image_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    prompt(call.message.chat.id, call.from_user.id, "welcome_image", "Welcome image PHOTO bhejo.")


@bot.callback_query_handler(func=lambda c: c.data == "a:clearwelcome")
def clear_welcome_cb(call):
    if not admin_callback(call):
        return
    set_setting("welcome_image", "")
    bot.answer_callback_query(call.id, "Cleared")
    bot.send_message(call.message.chat.id, "Welcome image cleared.")


@bot.callback_query_handler(func=lambda c: c.data == "a:demo")
def demo_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    kb = InlineKeyboardMarkup()
    kb.add(btn("Set/change link", "a:setdemo"))
    kb.add(btn("Clear link", "a:cleardemo"))
    kb.add(btn("⬅ Admin menu", "a:home"))
    bot.send_message(call.message.chat.id, "Demo link settings:", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data == "a:setdemo")
def setdemo_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    prompt(call.message.chat.id, call.from_user.id, "demo_link", "Full demo URL bhejo (https://t.me/...).")


@bot.callback_query_handler(func=lambda c: c.data == "a:cleardemo")
def cleardemo_cb(call):
    if not admin_callback(call):
        return
    set_setting("demo_link", "")
    bot.answer_callback_query(call.id, "Cleared")
    bot.send_message(call.message.chat.id, "Demo link cleared.")


@bot.callback_query_handler(func=lambda c: c.data == "a:emoji")
def emoji_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    prompt(call.message.chat.id, call.from_user.id, "button_emoji",
           "Ab ek message bhejo jisme custom Premium emoji ho. Bot us message ki pehli custom emoji ID save karega aur future supported button icons mein use karega.")


@bot.callback_query_handler(func=lambda c: c.data.startswith("a:editpick:"))
def editpick_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    try:
        pid = int(call.data.rsplit(":", 1)[1])
    except ValueError:
        return
    p = get_plan(pid)
    if not p:
        bot.send_message(call.message.chat.id, "Plan not found.")
        return
    kb = InlineKeyboardMarkup()
    for label, field in [
        ("Name", "name"), ("Price", "price"), ("Description + custom emoji", "description"),
        ("Plan image", "image"), ("Payment QR", "qr"), ("QR caption + emoji", "qrcaption"),
        ("Activate/deactivate", "active")]:
        kb.add(btn(label, f"a:field:{pid}:{field}"))
    kb.add(btn("⬅ Admin menu", "a:home"))
    bot.send_message(call.message.chat.id, f"Editing #{pid} {p['name']}. Choose field:", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith("a:removepick:"))
def removepick_cb(call):
    if not admin_callback(call):
        return
    try:
        pid = int(call.data.rsplit(":", 1)[1])
    except ValueError:
        bot.answer_callback_query(call.id, "Invalid plan.")
        return
    with db() as con:
        con.execute("UPDATE plans SET active=0 WHERE id=?", (pid,))
    bot.answer_callback_query(call.id, "Plan deactivated")
    bot.send_message(call.message.chat.id, f"Plan #{pid} deactivated; old orders preserved.")


@bot.callback_query_handler(func=lambda c: c.data.startswith("a:field:"))
def field_cb(call):
    if not admin_callback(call):
        return
    parts = call.data.split(":")
    if len(parts) != 4:
        bot.answer_callback_query(call.id, "Invalid field.")
        return
    try:
        pid = int(parts[2])
    except ValueError:
        bot.answer_callback_query(call.id, "Invalid plan.")
        return
    field = parts[3]
    map_fields = {
        "name": ("edit_name", "New plan name bhejo."),
        "price": ("edit_price", "New price bhejo, e.g. 199."),
        "description": ("edit_description", "New caption/description custom emoji ke saath bhejo."),
        "image": ("edit_image", "New plan image PHOTO bhejo."),
        "qr": ("edit_qr", "New payment QR PHOTO bhejo."),
        "qrcaption": ("edit_qrcaption", "New QR caption custom emoji ke saath bhejo."),
        "active": ("edit_active", "Send 1 to activate or 0 to deactivate.")
    }
    if field not in map_fields:
        bot.answer_callback_query(call.id, "Invalid field.")
        return
    bot.answer_callback_query(call.id)
    st, text = map_fields[field]
    prompt(call.message.chat.id, call.from_user.id, st, text, plan_id=pid)


@bot.callback_query_handler(func=lambda c: c.data == "a:pending")
def pending_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    with db() as con:
        rows = con.execute("SELECT id FROM orders WHERE status='pending' ORDER BY id DESC LIMIT 30").fetchall()
    if not rows:
        bot.send_message(call.message.chat.id, "No pending payments.")
    for r in rows:
        send_order_admin(call.message.chat.id, r["id"])


def send_order_admin(chat_id, oid):
    with db() as con:
        o = con.execute("""SELECT o.*,p.name,p.price FROM orders o LEFT JOIN plans p ON p.id=o.plan_id WHERE o.id=?""", (oid,)).fetchone()
    if not o:
        return
    caption = f"Order #{oid}\nUser ID: {o['user_id']}\nPlan: {o['name'] or 'Unavailable'}\nAmount: ₹{o['price'] or '?'}\nStatus: {o['status']}"
    kb = InlineKeyboardMarkup()
    if o["status"] == "pending":
        kb.row(btn("✅ Approve", f"a:approve:{oid}", style="success"),
               btn("❌ Reject", f"a:reject:{oid}", style="danger"))
    if o["screenshot_id"]:
        bot.send_photo(chat_id, o["screenshot_id"], caption=caption, reply_markup=kb if o["status"] == "pending" else None)
    else:
        bot.send_message(chat_id, caption, reply_markup=kb if o["status"] == "pending" else None)


@bot.callback_query_handler(func=lambda c: c.data.startswith("a:approve:") or c.data.startswith("a:reject:"))
def review_cb(call):
    if not admin_callback(call):
        return
    parts = call.data.split(":")
    action = parts[1]
    try:
        oid = int(parts[2])
    except (ValueError, IndexError):
        bot.answer_callback_query(call.id, "Invalid order.")
        return
    status = "approved" if action == "approve" else "rejected"
    with db() as con:
        o = con.execute("SELECT user_id,status FROM orders WHERE id=?", (oid,)).fetchone()
        if not o or o["status"] != "pending":
            bot.answer_callback_query(call.id, "Already reviewed or missing.", show_alert=True)
            return
        con.execute("UPDATE orders SET status=? WHERE id=?", (status, oid))
    bot.answer_callback_query(call.id, "Saved")
    try:
        bot.send_message(o["user_id"], "✅ Payment approved!" if status == "approved" else "❌ Payment rejected. Contact admin if you think this is a mistake.")
    except Exception:
        log.exception("Could not notify user")
    bot.send_message(call.message.chat.id, f"Order #{oid} marked {status}.")


def capture_custom_entities(message):
    return entity_data(getattr(message, "entities", None))


@bot.message_handler(content_types=["text", "photo"])
def form_handler(message):
    uid = message.from_user.id
    info = states.get(uid)
    if not info:
        return
    state = info["state"]
    if message.content_type == "text" and message.text and message.text.strip().lower() == "/cancel":
        states.pop(uid, None)
        bot.reply_to(message, "Cancelled.")
        if is_admin(uid):
            send_admin(message.chat.id)
        return

    if state == "payment_screenshot":
        if message.content_type != "photo":
            bot.reply_to(message, "Screenshot ko PHOTO ke roop mein bhejo.")
            return
        oid = info["order_id"]
        file_id = message.photo[-1].file_id
        with db() as con:
            cur = con.execute("""UPDATE orders SET screenshot_id=?,status='pending'
                WHERE id=? AND user_id=? AND status='awaiting_payment'""", (file_id, oid, uid))
            order = con.execute("SELECT id FROM orders WHERE id=?", (oid,)).fetchone()
            changed = cur.rowcount
        states.pop(uid, None)
        if not changed:
            bot.reply_to(message, "Order is no longer awaiting a screenshot.")
            return
        bot.reply_to(message, "Screenshot received. Admin will verify payment manually.")
        try:
            send_order_admin(ADMIN_ID, oid)
        except Exception:
            log.exception("Could not notify admin about order")
        return

    if not is_admin(uid):
        states.pop(uid, None)
        return

    if state in ("welcome_text", "edit_description", "edit_qrcaption"):
        if message.content_type != "text":
            bot.reply_to(message, "Text message bhejo, custom emoji ke saath.")
            return
        text = message.text
        ents = capture_custom_entities(message)
        if state == "welcome_text":
            set_setting("welcome_caption", text)
            set_setting("welcome_entities", json.dumps(ents))
            states.pop(uid, None)
            bot.reply_to(message, f"✅ Welcome text saved. Custom emoji entities found: {len(ents)}")
            return
        pid = info["plan_id"]
        with db() as con:
            if state == "edit_description":
                con.execute("UPDATE plans SET description=?,description_entities=? WHERE id=?",
                            (text, json.dumps(ents), pid))
            else:
                con.execute("UPDATE plans SET qr_caption=?,qr_entities=? WHERE id=?",
                            (text, json.dumps(ents), pid))
        states.pop(uid, None)
        bot.reply_to(message, f"✅ Saved. Custom emoji entities found: {len(ents)}")
        return

    if state == "button_emoji":
        ents = capture_custom_entities(message)
        if not ents:
            bot.reply_to(message, "Is message mein custom_emoji entity nahi mili. Telegram Premium custom emoji ko direct message mein insert karke bhejo; plain emoji se ID nahi milti.")
            return
        set_setting("button_emoji_id", ents[0]["custom_emoji_id"])
        states.pop(uid, None)
        bot.reply_to(message, "✅ Custom emoji ID saved for supported button icons.")
        return

    if state == "welcome_image":
        if message.content_type != "photo":
            bot.reply_to(message, "Welcome image PHOTO bhejo.")
            return
        set_setting("welcome_image", message.photo[-1].file_id)
        states.pop(uid, None)
        bot.reply_to(message, "✅ Welcome image saved.")
        return

    if state == "demo_link":
        if message.content_type != "text" or not valid_url(message.text.strip()):
            bot.reply_to(message, "Full valid URL bhejo, e.g. https://t.me/yourchannel")
            return
        set_setting("demo_link", message.text.strip())
        states.pop(uid, None)
        bot.reply_to(message, "✅ Demo link saved.")
        return

    if state.startswith("add_"):
        data = info.setdefault("data", {})
        if state == "add_name":
            if message.content_type != "text" or not message.text.strip():
                bot.reply_to(message, "Plan name text mein bhejo.")
                return
            data["name"] = message.text.strip()[:100]
            info["state"] = "add_price"
            bot.send_message(message.chat.id, "Price bhejo (e.g. 199).")
        elif state == "add_price":
            if message.content_type != "text" or not re.fullmatch(r"\d{1,9}(?:\.\d{1,2})?", message.text.strip()):
                bot.reply_to(message, "Valid price bhejo, e.g. 199 or 199.50.")
                return
            data["price"] = message.text.strip()
            info["state"] = "add_description"
            bot.send_message(message.chat.id, "Plan caption custom emoji ke saath bhejo, ya /skip.")
        elif state == "add_description":
            if message.content_type != "text":
                bot.reply_to(message, "Caption text mein bhejo.")
                return
            if message.text.strip() == "/skip":
                data["description"], data["description_entities"] = "", "[]"
            else:
                data["description"] = message.text[:3500]
                data["description_entities"] = json.dumps(capture_custom_entities(message))
            info["state"] = "add_image"
            bot.send_message(message.chat.id, "Plan image PHOTO bhejo, ya /skip.")
        elif state == "add_image":
            if message.content_type == "photo":
                data["image_id"] = message.photo[-1].file_id
            elif message.content_type == "text" and message.text.strip() == "/skip":
                data["image_id"] = ""
            else:
                bot.reply_to(message, "Photo bhejo ya /skip.")
                return
            info["state"] = "add_qr"
            bot.send_message(message.chat.id, "Payment QR PHOTO bhejo (required).")
        elif state == "add_qr":
            if message.content_type != "photo":
                bot.reply_to(message, "Payment QR ko PHOTO ke roop mein bhejo.")
                return
            data["qr_id"] = message.photo[-1].file_id
            info["state"] = "add_qrcaption"
            bot.send_message(message.chat.id, "QR caption custom emoji ke saath bhejo, ya /skip.")
        elif state == "add_qrcaption":
            if message.content_type != "text":
                bot.reply_to(message, "QR caption text mein bhejo.")
                return
            if message.text.strip() == "/skip":
                data["qr_caption"], data["qr_entities"] = "", "[]"
            else:
                data["qr_caption"] = message.text[:1000]
                data["qr_entities"] = json.dumps(capture_custom_entities(message))
            with db() as con:
                cur = con.execute("""INSERT INTO plans
                    (name,price,description,description_entities,image_id,qr_id,qr_caption,qr_entities,active)
                    VALUES(?,?,?,?,?,?,?,?,1)""",
                    (data["name"], data["price"], data.get("description", ""),
                     data.get("description_entities", "[]"), data.get("image_id", ""),
                     data["qr_id"], data.get("qr_caption", ""), data.get("qr_entities", "[]")))
                pid = cur.lastrowid
            states.pop(uid, None)
            bot.send_message(message.chat.id, f"✅ Plan #{pid} created and saved.")
            send_admin(message.chat.id)
        return

    if state.startswith("edit_"):
        pid = info["plan_id"]
        field_map = {
            "edit_name": ("name", "text"),
            "edit_price": ("price", "text"),
            "edit_description": ("description", "text"),
            "edit_image": ("image_id", "photo"),
            "edit_qr": ("qr_id", "photo"),
            "edit_qrcaption": ("qr_caption", "text"),
            "edit_active": ("active", "text")
        }
        if state not in field_map:
            return
        field, expected = field_map[state]
        if expected == "photo":
            if message.content_type != "photo":
                bot.reply_to(message, "Is field ke liye PHOTO bhejo.")
                return
            value = message.photo[-1].file_id
        else:
            if message.content_type != "text":
                bot.reply_to(message, "Text bhejo.")
                return
            value = message.text.strip()
            if field == "price" and not re.fullmatch(r"\d{1,9}(?:\.\d{1,2})?", value):
                bot.reply_to(message, "Valid price bhejo, e.g. 199.")
                return
            if field == "active" and value not in ("0", "1"):
                bot.reply_to(message, "1 = active, 0 = inactive.")
                return
            if field == "name" and not value:
                bot.reply_to(message, "Name cannot be empty.")
                return
        with db() as con:
            if field == "description":
                con.execute("UPDATE plans SET description=?,description_entities=? WHERE id=?",
                            (value, json.dumps(capture_custom_entities(message)), pid))
            elif field == "qr_caption":
                con.execute("UPDATE plans SET qr_caption=?,qr_entities=? WHERE id=?",
                            (value, json.dumps(capture_custom_entities(message)), pid))
            else:
                if field == "active":
                    value = int(value)
                con.execute(f"UPDATE plans SET {field}=? WHERE id=?", (value, pid))
        states.pop(uid, None)
        bot.reply_to(message, f"✅ Plan #{pid} updated and saved.")
        p = get_plan(pid)
        if p:
            kb = InlineKeyboardMarkup()
            for label, f in [("Name","name"),("Price","price"),("Description + emoji","description"),
                             ("Plan image","image"),("Payment QR","qr"),("QR caption + emoji","qrcaption"),
                             ("Activate/deactivate","active")]:
                kb.add(btn(label, f"a:field:{pid}:{f}"))
            kb.add(btn("⬅ Admin menu", "a:home"))
            bot.send_message(message.chat.id, f"Editing #{pid} {p['name']}. Choose another field:", reply_markup=kb)
        return


if __name__ == "__main__":
    setup_db()
    log.info("Starting bot with database %s", DB_PATH)
    # Important: only ONE running instance may poll this token.
    bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=25)
