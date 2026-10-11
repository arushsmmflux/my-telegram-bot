import os
import io
import sqlite3
import asyncio
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from datetime import datetime, timezone
from urllib.parse import urlencode

import qrcode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters,
)

UPI_ID = "xsdevvv889@fam"


def generate_upi_qr(amount, order_id):
    """Generate a UPI QR with this order's exact INR amount."""
    amount = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if amount <= 0:
        raise ValueError("Amount must be positive")

    params = {
        "pa": UPI_ID,
        "pn": "FLUX SMM",
        "am": f"{amount:.2f}",
        "cu": "INR",
        "tn": f"FLUX SMM Order {order_id}",
    }
    upi_link = "upi://pay?" + urlencode(params)
    qr = qrcode.make(upi_link)
    image_buffer = io.BytesIO()
    image_buffer.name = f"flux_smm_order_{order_id}.png"
    qr.save(image_buffer, format="PNG")
    image_buffer.seek(0)
    return image_buffer

# ============================================================
# FLUX SMM BOT
# Python + python-telegram-bot 22.x
#
# Put BOT_TOKEN and ADMIN_ID in your environment.
# Edit CONFIG below to change plans, prices, text, images, QR,
# and support link without changing the main logic.
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

ADMIN_RAW = os.getenv("ADMIN_ID", "").strip()
if not ADMIN_RAW.isdigit():
    raise RuntimeError("ADMIN_ID is missing or invalid. Set your numeric Telegram user ID.")
ADMIN_ID = int(ADMIN_RAW)

# Paste your hosted direct image URLs below (or Telegram photo file_ids).
# Welcome image appears on /start and when users return to the home menu.
START_IMAGE = "https://ibb.co/7NZLR5SK"

# One image per platform's plan page. These images appear only on the
# platform selection page, not inside individual service/order screens.
PLAN_IMAGES = {
    "instagram": "https://ibb.co/Q7NWhyCp",
    "facebook": "https://ibb.co/xtjSNYnh",
    "youtube": "https://ibb.co/q3cg2Sbv",
    "telegram": "https://ibb.co/PBm8yqP",
    "freefire": "https://ibb.co/0jYJpK1Z",
}

# Support link is kept in code, not Railway variables.
SUPPORT_URL = "https://t.me/xylerigcc"


class _ImageMetaParser(HTMLParser):
    """Find the actual image URL embedded in an ImgBB share page."""
    def __init__(self):
        super().__init__()
        self.image_url = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "meta":
            return
        attrs = dict(attrs)
        key = (attrs.get("property") or attrs.get("name") or "").lower()
        if key in ("og:image", "twitter:image", "twitter:image:src") and attrs.get("content"):
            self.image_url = attrs["content"]

def load_hosted_image(url: str):
    """Download an image from either a direct URL or an ImgBB page URL.

    Telegram cannot use an ImgBB webpage URL directly as a photo, so this
    fetches the page, reads its og:image metadata, then downloads the image.
    Returns a Telegram-compatible BytesIO object.
    """
    headers = {"User-Agent": "Mozilla/5.0 (compatible; FluxSMMBot/1.0)"}
    req = Request(url, headers=headers)
    with urlopen(req, timeout=15) as response:
        content_type = response.headers.get("Content-Type", "").lower()
        body = response.read(12 * 1024 * 1024 + 1)
        final_url = response.geturl()
    if len(body) > 12 * 1024 * 1024:
        raise ValueError("Image is larger than 12 MB")

    if content_type.startswith("image/"):
        image_bytes = body
    else:
        parser = _ImageMetaParser()
        parser.feed(body.decode("utf-8", errors="replace"))
        if not parser.image_url:
            raise ValueError("Could not find the actual image in this hosting page")
        image_url = urljoin(final_url, parser.image_url)
        image_req = Request(image_url, headers=headers)
        with urlopen(image_req, timeout=15) as response:
            image_type = response.headers.get("Content-Type", "").lower()
            image_bytes = response.read(12 * 1024 * 1024 + 1)
        if len(image_bytes) > 12 * 1024 * 1024:
            raise ValueError("Image is larger than 12 MB")
        if not image_type.startswith("image/"):
            raise ValueError("ImgBB did not return an image file")

    photo = io.BytesIO(image_bytes)
    photo.name = "flux_smm_image.jpg"
    photo.seek(0)
    return photo

# ---------- Styled text ----------
def f(text: str) -> str:
    """Return readable plain text; avoids mangled caption formatting."""
    return text

def money(value):
    value = Decimal(str(value))
    return f"₹{value.quantize(Decimal('0.01'))}"

# ---------- Editable bot content ----------
START_CAPTION = """🚀 WELCOME TO FLUX SMM

Fast & Affordable Social Media Services
Instagram • Facebook • YouTube • Telegram
High Quality • Easy Ordering • Quick Support

Choose a platform below and select a service.
Prices are shown clearly before payment.
After payment, send your screenshot and UTR.
Admin will verify your payment manually.
Please enter correct details while ordering.

Thank you for choosing FLUX SMM ❤️"""

SERVICE_CAPTION = """🚀 FLUX SMM SERVICE

Select a service below to place your order.
Choose the quantity you need.
The bot will calculate your total automatically.
Then complete payment using the QR code.
Send your payment screenshot and UTR for approval."""

PAYMENT_TEXT = """💳 PAYMENT DETAILS

Scan the QR code and pay the exact amount shown.
After payment, send your payment screenshot here.
Then send your UTR / transaction number.
Your order will be sent to admin for verification.
Do not send a fake or edited payment screenshot."""

# service format:
# {"name": "...", "price": Decimal/string, "unit": "...", "fixed": False}
# fixed=True means the listed price is the complete package price.
PLANS = {
    "instagram": {
        "name": f("INSTAGRAM"),
        "services": [
            {"name": f("LIKES NON DROP"), "price": "20", "unit": "1K", "fixed": False},
            {"name": f("FOLLOWERS NON DROP"), "price": "34", "unit": "1K", "fixed": False},
            {"name": f("VIEWS"), "price": "10", "unit": "1K", "fixed": False},
            {"name": f("COMMENTS"), "price": "23", "unit": "1K", "fixed": False},
            {"name": f("LIKES (20% DROP)"), "price": "10", "unit": "1K", "fixed": False},
            {"name": f("FOLLOWERS (20% DROP)"), "price": "19", "unit": "1K", "fixed": False},
            {"name": f("STORY VIEW & LIKE"), "price": "26", "unit": "1K", "fixed": False},
        ],
    },
    "facebook": {
        "name": f("FACEBOOK"),
        "services": [
            {"name": f("FOLLOWERS DROP"), "price": "20", "unit": "1K", "fixed": False},
            {"name": f("FOLLOWERS NON DROP"), "price": "34", "unit": "1K", "fixed": False},
            {"name": f("LIKE DROP"), "price": "10", "unit": "1K", "fixed": False},
            {"name": f("LIKE NON DROP"), "price": "20", "unit": "1K", "fixed": False},
            {"name": f("COMMENTS"), "price": "23", "unit": "1K", "fixed": False},
            {"name": f("VIEWS"), "price": "10", "unit": "1K", "fixed": False},
        ],
    },
    "youtube": {
        "name": f("YOUTUBE"),
        "services": [
            {"name": f("SUBSCRIBERS NO DROP"), "price": "39", "unit": "1K", "fixed": False},
            {"name": f("SUBSCRIBERS DROP"), "price": "23", "unit": "1K", "fixed": False},
            {"name": f("LIKES DROP"), "price": "15", "unit": "1K", "fixed": False},
            {"name": f("LIKES NON DROP"), "price": "24", "unit": "1K", "fixed": False},
            {"name": f("COMMENTS"), "price": "30", "unit": "1K", "fixed": False},
            {"name": f("4000 HOURS WATCH TIME"), "price": "99", "unit": "PACKAGE", "fixed": True},
        ],
    },
    "telegram": {
        "name": f("TELEGRAM"),
        "services": [
            {"name": f("CHANNEL MEMBERS NON DROP"), "price": "20", "unit": "1K", "fixed": False},
            {"name": f("CHANNEL MEMBER DROP"), "price": "10", "unit": "1K", "fixed": False},
            {"name": f("POST VIEWS"), "price": "25", "unit": "5K", "fixed": False},
            {"name": f("REACTION (GOOD)"), "price": "20", "unit": "1K", "fixed": False},
            {"name": f("REACTION (BAD)"), "price": "18", "unit": "1K", "fixed": False},
        ],
    },
    "freefire": {
        "name": f("FREE FIRE LIKES"),
        "services": [
            {"name": f("10K FF LIKES"), "price": "29", "unit": "PACKAGE", "fixed": True},
            {"name": f("50K FF LIKES"), "price": "67", "unit": "PACKAGE", "fixed": True},
            {"name": f("100K FF LIKES"), "price": "126", "unit": "PACKAGE", "fixed": True},
        ],
    },
}

# ============================================================
# Database
# ============================================================
DB_PATH = "orders.db"

def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = db()
    con.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            plan_key TEXT NOT NULL,
            service_name TEXT NOT NULL,
            quantity TEXT,
            target TEXT,
            custom_text TEXT,
            amount TEXT NOT NULL,
            screenshot_file_id TEXT,
            utr TEXT,
            status TEXT NOT NULL DEFAULT 'WAITING_PAYMENT',
            created_at TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()

def create_order(data):
    con = db()
    cur = con.execute("""
        INSERT INTO orders
        (user_id, username, plan_key, service_name, quantity, target,
         custom_text, amount, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'WAITING_PAYMENT', ?)
    """, (
        data["user_id"], data.get("username"), data["plan_key"],
        data["service_name"], data.get("quantity"), data.get("target"),
        data.get("custom_text"), str(data["amount"]),
        datetime.now(timezone.utc).isoformat()
    ))
    order_id = cur.lastrowid
    con.commit()
    con.close()
    return order_id

def update_order(order_id, **fields):
    allowed = {
        "screenshot_file_id", "utr", "status", "target", "custom_text",
        "quantity", "amount"
    }
    fields = {k: v for k, v in fields.items() if k in allowed}
    if not fields:
        return
    con = db()
    sets = ", ".join(f"{k}=?" for k in fields)
    con.execute(f"UPDATE orders SET {sets} WHERE id=?", (*fields.values(), order_id))
    con.commit()
    con.close()

def get_order(order_id):
    con = db()
    row = con.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    con.close()
    return row

# ============================================================
# UI helpers
def button(text, *, callback_data=None, url=None, style="primary"):
    """Create a styled inline button. Telegram supports primary/blue, success/green, danger/red."""
    return InlineKeyboardButton(
        text,
        callback_data=callback_data,
        url=url,
        style=style,
    )

def back_button(style="primary"):
    return [button(f("🔙 BACK"), callback_data="home", style=style)]

def main_keyboard():
    return InlineKeyboardMarkup([
        [button(f("📸 INSTAGRAM"), callback_data="plan:instagram", style="primary"),
         button(f("📘 FACEBOOK"), callback_data="plan:facebook", style="success")],
        [button(f("▶️ YOUTUBE"), callback_data="plan:youtube", style="danger"),
         button(f("✈️ TELEGRAM"), callback_data="plan:telegram", style="primary")],
        [button(f("🎮 FREE FIRE LIKES"), callback_data="plan:freefire", style="success")],
        [button(f("💬 SUPPORT"), url=SUPPORT_URL, style="danger")],
    ])

def plan_keyboard(plan_key):
    services = PLANS[plan_key]["services"]
    styles = ["primary", "success", "danger"]
    rows = []
    for i, svc in enumerate(services):
        rows.append([button(
            f"{i+1}. {svc['name']} • ₹{svc['price']}/{svc['unit']}",
            callback_data=f"service:{plan_key}:{i}",
            style=styles[i % len(styles)],
        )])
    rows.append([button(f("🔙 BACK TO PLANS"), callback_data="home", style="primary")])
    return InlineKeyboardMarkup(rows)

def order_keyboard(order_id):
    return InlineKeyboardMarkup([
        [button(f("💳 PAY NOW"), callback_data=f"pay:{order_id}", style="success")],
        [button(f("❌ CANCEL"), callback_data="home", style="danger")]
    ])

def admin_keyboard(order_id):
    return InlineKeyboardMarkup([
        [button(f("✅ APPROVE"), callback_data=f"admin:approve:{order_id}", style="success")],
        [button(f("❌ REJECT"), callback_data=f"admin:reject:{order_id}", style="danger")]
    ])

async def send_start(chat, bot):
    kb = main_keyboard()
    if START_IMAGE and not START_IMAGE.startswith(("START_IMAGE_", "PASTE_")):
        try:
            photo = await asyncio.to_thread(load_hosted_image, START_IMAGE)
            await bot.send_photo(chat_id=chat.id, photo=photo,
                                 caption=START_CAPTION, reply_markup=kb)
            return
        except Exception as exc:
            print(f"Welcome image failed; sending text fallback: {exc!r}")
    await bot.send_message(chat_id=chat.id, text=START_CAPTION, reply_markup=kb)

# ============================================================
# Handlers
# ============================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await send_start(update.effective_chat, context.bot)

async def home_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    context.user_data.clear()
    await send_start(q.message.chat, context.bot)

async def support_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    text = f"""💬 {f("SUPPORT")}

{f("Need help? Contact our support team.")}
{f("SUPPORT LINK:")} {SUPPORT_URL or "[ADD YOUR SUPPORT LINK IN CONFIG]"}"""
    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup([back_button()]))

async def plan_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    _, plan_key = q.data.split(":", 1)
    plan = PLANS.get(plan_key)
    if not plan:
        await q.message.reply_text("Sorry, this platform was not found. Please use /start.")
        return

    caption = f"""{plan["name"]} 🚀

Select the service you want to order.
All prices are displayed on the buttons.
Tap a service to continue."""

    kb = plan_keyboard(plan_key)
    plan_image = PLAN_IMAGES.get(plan_key, "")
    if plan_image and not plan_image.startswith(("PASTE_", "PLAN_IMAGE_")):
        try:
            photo = await asyncio.to_thread(load_hosted_image, plan_image)
            await q.message.reply_photo(photo=photo, caption=caption, reply_markup=kb)
            return
        except Exception as exc:
            print(f"Plan image failed for {plan_key}; using text fallback: {exc!r}")
    await q.edit_message_text(caption, reply_markup=kb)

async def service_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    _, plan_key, idx = q.data.split(":")
    idx = int(idx)
    service = PLANS[plan_key]["services"][idx]

    context.user_data["plan_key"] = plan_key
    context.user_data["service_index"] = idx
    context.user_data["service_name"] = service["name"]
    context.user_data["price"] = service["price"]
    context.user_data["unit"] = service["unit"]
    context.user_data["fixed"] = service["fixed"]

    # Requested special selector for the 7th Instagram button.
    # Both options use the listed ₹26/1K price.
    if plan_key == "instagram" and idx == 6:
        await q.edit_message_text(
            f"""{f("SELECT TYPE")}

{f("Choose the comment type you want.")}

{f("RANDOM COMMENTS")} — ₹26/1K
{f("CUSTOM COMMENTS")} — ₹26/1K""",
            reply_markup=InlineKeyboardMarkup([
                [button(
                    f("💬 RANDOM COMMENTS • ₹26/1K"),
                    callback_data="comment_type:random",
                    style="primary"
                )],
                [button(
                    f("✍️ CUSTOM COMMENTS • ₹26/1K"),
                    callback_data="comment_type:custom",
                    style="success"
                )],
                [button(f("🔙 BACK"), callback_data=f"plan:{plan_key}", style="primary")]
            ])
        )
        return

    if service["fixed"]:
        amount = Decimal(service["price"])
        context.user_data["amount"] = str(amount)
        context.user_data["quantity"] = service["unit"]
        await q.edit_message_text(
            f"""{service["name"]}

{f("Package Price:")} {money(amount)}

{f("Tap ORDER NOW to continue.")}""",
            reply_markup=InlineKeyboardMarkup([
                [button(f("🛒 ORDER NOW"), callback_data="create:fixed", style="success")],
                [button(f("🔙 BACK"), callback_data=f"plan:{plan_key}", style="primary")]
            ])
        )
        return

    await q.edit_message_text(
        f"""{service["name"]}

{f("Price:")} ₹{service["price"]}/{service["unit"]}

{f("Enter the quantity you want.")}
{f("Example:")} 1000
{f("Minimum recommended entry: 1000")}""",
        reply_markup=InlineKeyboardMarkup([back_button()])
    )
    context.user_data["state"] = "quantity"


async def comment_type_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    choice = q.data.split(":")[1]
    context.user_data["comment_type"] = choice
    context.user_data["service_name"] = (
        f("RANDOM COMMENTS") if choice == "random" else f("CUSTOM COMMENTS")
    )
    context.user_data["price"] = "26"
    context.user_data["unit"] = "1K"
    context.user_data["fixed"] = False

    if choice == "custom":
        context.user_data["state"] = "custom_text"
        await q.edit_message_text(
            f"""{f("CUSTOM COMMENTS")}

{f("Send the comment text you want to use.")}

{f("Example: Great post! 🔥")}
{f("You can send multiple comments separated by new lines.")}

{f("After that, the bot will ask for quantity.")}""",
            reply_markup=InlineKeyboardMarkup([back_button()])
        )
    else:
        context.user_data["state"] = "quantity"
        await q.edit_message_text(
            f"""{f("RANDOM COMMENTS")}

{f("Price:")} ₹26/1K

{f("Enter the quantity you want.")}
{f("Example:")} 1000""",
            reply_markup=InlineKeyboardMarkup([back_button()])
        )

async def create_fixed_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if "service_name" not in context.user_data:
        return

    order_data = {
        "user_id": q.from_user.id,
        "username": q.from_user.username,
        "plan_key": context.user_data["plan_key"],
        "service_name": context.user_data["service_name"],
        "quantity": context.user_data.get("quantity"),
        "target": None,
        "custom_text": None,
        "amount": Decimal(context.user_data["amount"]),
    }
    order_id = create_order(order_data)
    context.user_data["order_id"] = order_id
    context.user_data["state"] = "target"

    await q.edit_message_text(
        f"""{f("ORDER #")}{order_id}

{f("Service:")} {order_data["service_name"]}
{f("Amount:")} {money(order_data["amount"])}

{"Send your numeric Free Fire Player UID in the next message." if order_data["plan_key"] == "freefire" else "Now send your target/link in the next message."}

{"Example: 12345678901 (Free Fire UID)." if order_data["plan_key"] == "freefire" else "Example: Instagram profile link, YouTube channel link, or Telegram post link."}"""
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state")

    if state == "quantity":
        raw = update.message.text.strip().replace(",", "")
        try:
            qty = Decimal(raw)
            if qty <= 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            await update.message.reply_text(f("Please enter a valid quantity, for example 1000."))
            return

        unit = context.user_data["unit"]
        # Price is per 1K or per 5K. For 1K: qty/1000.
        if unit == "1K":
            multiplier = qty / Decimal("1000")
        elif unit == "5K":
            multiplier = qty / Decimal("5000")
        else:
            multiplier = Decimal("1")

        amount = Decimal(context.user_data["price"]) * multiplier
        context.user_data["quantity"] = str(qty)
        context.user_data["amount"] = str(amount)

        await update.message.reply_text(
            f"""{f("ORDER SUMMARY")} 🛒

{f("Service:")} {context.user_data["service_name"]}
{f("Quantity:")} {qty}
{f("Price:")} ₹{context.user_data["price"]}/{unit}
{f("Total:")} {money(amount)}

{f("Tap ORDER NOW to continue.")}""",
            reply_markup=InlineKeyboardMarkup([
                [button(f("🛒 ORDER NOW"), callback_data="create:variable", style="success")],
                [button(f("❌ CANCEL"), callback_data="home", style="danger")]
            ])
        )
        context.user_data["state"] = "confirm"
        return

    if state == "target":
        order_id = context.user_data.get("order_id")
        if not order_id:
            return
        target = update.message.text.strip()
        if len(target) < 2:
            await update.message.reply_text("Please send a valid target, link, or UID.")
            return
        current_order = get_order(order_id)
        if current_order and current_order["plan_key"] == "freefire":
            if not target.isdigit() or not (5 <= len(target) <= 15):
                await update.message.reply_text(
                    "Please send your numeric Free Fire Player UID only (5–15 digits). Do not send your nickname."
                )
                return

        update_order(order_id, target=target)
        context.user_data["state"] = "payment"

        await update.message.reply_text(
            f"""{f("ORDER #")}{order_id}

{f("Target saved successfully.")}

{f("Now tap PAY NOW to see the QR code and payment instructions.")}""",
            reply_markup=InlineKeyboardMarkup([
                [button(f("💳 PAY NOW"), callback_data=f"pay:{order_id}", style="success")],
                [button(f("❌ CANCEL"), callback_data="home", style="danger")]
            ])
        )
        return

    if state == "custom_text":
        context.user_data["custom_text"] = update.message.text.strip()
        context.user_data["state"] = "quantity"
        await update.message.reply_text(
            f"""{f("Custom comment text saved.")}

{f("Now enter the quantity.")}
{f("Example:")} 1000""",
            reply_markup=InlineKeyboardMarkup([back_button()])
        )
        return

    if state == "utr":
        order_id = context.user_data.get("order_id")
        if not order_id:
            await update.message.reply_text(f("No active order found. Use /start."))
            return

        utr = update.message.text.strip()
        if len(utr) < 4:
            await update.message.reply_text(f("Please send a valid UTR / transaction number."))
            return

        update_order(order_id, utr=utr, status="PENDING_ADMIN")
        await notify_admin(update, context, order_id)

        context.user_data["state"] = "waiting_admin"
        await update.message.reply_text(
            f"""✅ {f("PAYMENT SUBMITTED")}

{f("Order:")} #{order_id}
{f("UTR received successfully.")}
{f("Your payment is now waiting for admin approval.")}

{f("Please wait for the approval message.")}"""
        )
        return

    await update.message.reply_text(f("Use /start to open FLUX SMM."))

async def create_variable_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    order_data = {
        "user_id": q.from_user.id,
        "username": q.from_user.username,
        "plan_key": context.user_data["plan_key"],
        "service_name": context.user_data["service_name"],
        "quantity": context.user_data["quantity"],
        "target": None,
        "custom_text": context.user_data.get("custom_text"),
        "amount": Decimal(context.user_data["amount"]),
    }
    order_id = create_order(order_data)
    context.user_data["order_id"] = order_id
    context.user_data["state"] = "target"

    await q.edit_message_text(
        f"""🧾 {f("ORDER #")}{order_id}

{f("Service:")} {order_data["service_name"]}
{f("Quantity:")} {order_data["quantity"]}
{f("Total:")} {money(order_data["amount"])}

{"Send your numeric Free Fire Player UID in the next message." if order_data["plan_key"] == "freefire" else "Now send your target/link in the next message."}"""
    )

async def pay_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    try:
        order_id = int(q.data.split(":")[1])
    except Exception:
        return

    order = get_order(order_id)
    if not order or order["user_id"] != q.from_user.id:
        await q.message.reply_text(f("Order not found."))
        return

    context.user_data["order_id"] = order_id
    context.user_data["state"] = "screenshot"

    caption = f"""{PAYMENT_TEXT}

🧾 {f("ORDER:")} #{order_id}
💰 {f("AMOUNT:")} {money(order["amount"])}

{f("After payment, send your payment screenshot here.")}"""

    # Create a fresh QR for the exact saved order amount.
    try:
        qr_image = generate_upi_qr(order["amount"], order_id)
        await q.message.reply_photo(photo=qr_image, caption=caption)
    except Exception as exc:
        print(f"QR generation/send failed for order #{order_id}: {exc!r}")
        await q.message.reply_text(
            caption + "\n\n" + f("QR could not be generated. Please contact support."),
        )

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("state") != "screenshot":
        return

    order_id = context.user_data.get("order_id")
    if not order_id:
        return

    photo = update.message.photo[-1]
    update_order(order_id, screenshot_file_id=photo.file_id, status="SCREENSHOT_RECEIVED")
    context.user_data["state"] = "utr"

    await update.message.reply_text(
        f"""📸 {f("SCREENSHOT RECEIVED")}

{f("Now send your UTR / transaction number.")}

{f("Example: 123456789012")}"""
    )

async def document_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("state") != "screenshot":
        return

    order_id = context.user_data.get("order_id")
    if not order_id:
        return

    doc = update.message.document
    update_order(order_id, screenshot_file_id=doc.file_id, status="SCREENSHOT_RECEIVED")
    context.user_data["state"] = "utr"

    await update.message.reply_text(
        f"""📎 {f("PAYMENT FILE RECEIVED")}

{f("Now send your UTR / transaction number.")}"""
    )

async def notify_admin(update, context, order_id):
    order = get_order(order_id)
    user = update.effective_user

    caption = f"""🔔 {f("NEW PAYMENT FOR APPROVAL")}

🧾 {f("Order:")} #{order_id}
👤 {f("User:")} {user.first_name}
🆔 {f("User ID:")} {user.id}
🔗 {f("Username:")} @{user.username if user.username else "N/A"}

📦 {f("Service:")} {order["service_name"]}
🔢 {f("Quantity:")} {order["quantity"] or "-"}
🎯 {f("Target:")} {order["target"] or "-"}
💰 {f("Amount:")} {money(order["amount"])}
🧾 {f("UTR:")} {order["utr"]}

{f("Verify the payment before approving.")}"""

    if order["screenshot_file_id"]:
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=order["screenshot_file_id"],
            caption=caption,
            reply_markup=admin_keyboard(order_id)
        )
    else:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=caption,
            reply_markup=admin_keyboard(order_id)
        )

async def admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query

    if q.from_user.id != ADMIN_ID:
        await q.answer(f("You are not authorized."), show_alert=True)
        return

    await q.answer()
    _, action, order_id_raw = q.data.split(":")
    order_id = int(order_id_raw)
    order = get_order(order_id)

    if not order:
        await q.message.reply_text(f("Order not found."))
        return

    if order["status"] not in ("PENDING_ADMIN", "SCREENSHOT_RECEIVED"):
        await q.answer(f"Order already processed.", show_alert=True)
        return

    if action == "approve":
        update_order(order_id, status="APPROVED")
        await context.bot.send_message(
            chat_id=order["user_id"],
            text=f"""✅ {f("PAYMENT APPROVED")}

🧾 {f("Order:")} #{order_id}
📦 {f("Service:")} {order["service_name"]}
💰 {f("Amount:")} {money(order["amount"])}

{f("Your payment has been verified.")}
{f("Your order is now approved.")}

{f("Thank you for using FLUX SMM 🚀")}"""
        )
        await q.edit_message_reply_markup(reply_markup=None)
        await q.message.reply_text(f"✅ Order #{order_id} approved.")
    else:
        update_order(order_id, status="REJECTED")
        await context.bot.send_message(
            chat_id=order["user_id"],
            text=f"""❌ {f("PAYMENT REJECTED")}

🧾 {f("Order:")} #{order_id}

{f("The submitted payment could not be approved.")}
{f("Please contact support if you believe this is a mistake.")}

{f("Order remains unfulfilled until payment is verified.")}"""
        )
        await q.edit_message_reply_markup(reply_markup=None)
        await q.message.reply_text(f"❌ Order #{order_id} rejected.")

# ============================================================
# Main
# ============================================================
def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is missing. Set it as an environment variable before running."
        )

    init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CallbackQueryHandler(home_callback, pattern=r"^home$"))
    app.add_handler(CallbackQueryHandler(support_callback, pattern=r"^support$"))
    app.add_handler(CallbackQueryHandler(plan_callback, pattern=r"^plan:"))
    app.add_handler(CallbackQueryHandler(service_callback, pattern=r"^service:"))
    app.add_handler(CallbackQueryHandler(comment_type_callback, pattern=r"^comment_type:(random|custom)$"))
    app.add_handler(CallbackQueryHandler(create_fixed_order, pattern=r"^create:fixed$"))
    app.add_handler(CallbackQueryHandler(create_variable_order, pattern=r"^create:variable$"))
    app.add_handler(CallbackQueryHandler(pay_callback, pattern=r"^pay:\d+$"))
    app.add_handler(CallbackQueryHandler(admin_action, pattern=r"^admin:(approve|reject):\d+$"))

    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, document_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("FLUX SMM bot is starting. Ensure only ONE running instance uses this BOT_TOKEN.")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=False)

if __name__ == "__main__":
    main()
