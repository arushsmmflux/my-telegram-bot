import os
import logging
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Railway Variables required: BOT_TOKEN, ADMIN_ID
TOKEN = os.getenv('BOT_TOKEN', '').strip()
ADMIN_RAW = os.getenv('ADMIN_ID', '').strip()
if not TOKEN:
    raise RuntimeError('Set BOT_TOKEN in Railway Variables')
if not ADMIN_RAW.isdigit():
    raise RuntimeError('Set ADMIN_ID to your numeric Telegram user ID')
ADMIN_ID = int(ADMIN_RAW)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('course_bot')
bot = telebot.TeleBot(TOKEN)

# ===================== EDIT YOUR CONTENT HERE =====================
# Telegram photo file_id values can be obtained by sending each image to the bot
# and reading message.photo[-1].file_id, or use a public direct image URL.
AGE_IMAGE = 'https://ibb.co/5ghpxM6Z'
AGE_CAPTION = '𝘽𝙚𝙛𝙤𝙧𝙚 𝙘𝙤𝙣𝙩𝙞𝙣𝙪𝙞𝙣𝙜, 𝙥𝙡𝙚𝙖𝙨𝙚 𝙘𝙤𝙣𝙛𝙞𝙧𝙢 𝙮𝙤𝙪 𝙖𝙧𝙚 18 𝙤𝙧 𝙤𝙡𝙙𝙚𝙧.'
DENIED_CAPTION = '𝘼𝙘𝙘𝙚𝙨𝙨 𝙙𝙚𝙣𝙞𝙚𝙙. 𝘽𝙤𝙩 𝙞𝙨 𝙤𝙣𝙡𝙮 𝙛𝙤𝙧 18+.'
WELCOME_IMAGE = 'https://myimgs.org/storage/images/48905/1000200263.jpg'
WELCOME_CAPTION = '''𝙃𝙀𝙔 👋🏻, 𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 𝙤𝙪𝙧 𝙫𝙞𝙥 𝙗𝙤𝙩 😍
𝙏𝙃𝙄𝙎 𝘽𝙊𝙏 𝘾𝙊𝙉𝘼𝙏𝘼𝙄𝙉 𝙁𝙊𝙇𝙇𝙊𝙒𝙄𝙉𝙂 𝙋𝙇𝘼𝙉𝙎 ✅ 
𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂 𝙋𝙍𝙄𝘾𝙀 𝙄𝙎 𝙅𝙐𝙎𝙏 ₹39 ‼️

| 🔥𝘾𝙃𝙄!𝙇𝘿 𝙑𝙄𝘿𝙀𝙊𝙎 ( 𝘾𝙋 ) ( 𝘾𝙃𝙊𝙏𝙀 𝘽𝘼𝘾𝘾𝙃𝙀 ) 
| 🔥𝘽𝙃𝘼𝘽𝙃𝙄 𝙑𝙄𝘿𝙀0𝙎 
| 🔥𝙈0𝙈 𝘼𝙉𝘿 𝙎𝙊#𝙉 
| 🔥𝙍!@𝙋𝙀 𝙑𝙄𝘿𝙀0𝙎
| 🔥𝘽𝘼#𝙋 𝘽𝙀𝙏𝙄 
| 🔥𝗜𝗡𝗦𝗧𝗚𝗥𝗔𝗠 𝗠𝗠#𝗦 𝗔𝗟𝗟 
| 🔥𝙂𝙄𝙍𝙇𝙎 𝙒𝙄𝙏𝙃 𝘼𝙉𝙄𝙈!𝘼𝙇 
| 🔥 𝙈𝙄𝙓 𝙂𝙍𝙊𝙐𝙋 70𝙆 𝙑𝙄𝘿𝙀𝙊 
| 🔥𝘽𝙃𝘼𝙄 𝘽𝙀𝙃𝘼𝙉
| 🔥𝗔𝗟𝗟 𝗩𝗜𝗣 𝗠𝗘𝗚𝗔 𝗣𝗔𝗖𝗞 

𝘽𝙀𝙉𝙄𝙁𝙄𝙏𝙎 𝙊𝙁 𝙊𝙐𝙍 𝘽𝙊𝙏 ✅
1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙑𝙄𝘿𝙀𝙊𝙎 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅
2. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝘿𝙊𝙒𝙉𝙇𝙊𝘼𝘿 𝙁𝙍𝙀𝙀 ✅
3. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ✅
4. 𝘿𝙄𝙍𝙀𝘾𝙏 𝙒𝘼𝙏𝘾𝙃 𝙑𝙄𝘿𝙀𝙊𝙎 ✅
𝙏𝙊 𝘽𝙐𝙔 𝙋𝙇𝘼𝙉𝙎 𝘾𝙃𝙀𝘾𝙇 𝘽𝙐𝙏𝙏𝙊𝙉𝙎 𝘽𝙀𝙇𝙊𝙒 𝘼𝙉𝘿 𝘾𝙃𝙀𝘾𝙆 𝘿𝙀𝙈𝙊 𝘼𝙇𝙎𝙊 😍🔥.'''

# Add/edit exactly 10 plan entries here. Leave unused entries with active=False.
PLANS = [
    {
        'id': 1, 'name': '𝙈𝙊𝙈 𝘼𝙉𝘿 𝙎𝙊𝙉 😍🔥 ', 'price': '49',
        'validity': '180 days', 'videos': 'As described',
        'image': 'https://ibb.co/ZRqKVvRQ', 'qr': 'https://ibb.co/fYsgpT3c',
        'demos': [
'https://t.me/studyof12th/27',
'https://t.me/studyof12th/30',
'https://t.me/studyof12th/47',
'https://t.me/studyof12th/65'
        ],
   'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 𝙁𝙍𝙄𝘿𝘼𝙔 ✅.'
),
'active': True
    },
      {
        'id': 4, 'name': '𝙍!@𝙋𝙀 𝙑𝙄𝘿𝙀𝙊𝙎 💦👀 ', 'price': '69',
        'validity': '180 days', 'videos': '40000',
        'image': 'https://ibb.co/QF2v05qK', 'qr': 'https://ibb.co/gbLMg58r',
        'demos': [   
'https://t.me/studyof12th/42',
'https://t.me/studyof12th/37',
'https://t.me/studyof12th/20',
'https://t.me/studyof12th/12',
'https://t.me/studyof12th/15',
'https://t.me/studyof12th/40',
'https://t.me/studyof12th/40'
        ],
      'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 SATURDAY ✅.'
),
'active': True
    },
      {
        'id': 5, 'name': '𝘾𝙃𝙄!𝙇𝘿 𝙑𝙄𝘿!𝙀𝙊 ( 𝘾.𝙋)  🔥👀', 'price': '49',
        'validity': '180 days', 'videos': '70000+',
        'image': 'https://ibb.co/21H7BGM2', 'qr': 'https://ibb.co/fYsgpT3c',
        'demos': [          
'https://t.me/studyof12th/51',
'https://t.me/studyof12th/41',
'https://t.me/studyof12th/28',
'https://t.me/studyof12th/26',
'https://t.me/studyof12th/25',
'https://t.me/studyof12th/24',
'https://t.me/studyof12th/6'
        ],
       'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 SUNDAY✅.'
),
'active': True
    },
      {
        'id': 6, 'name': '𝘽𝙃𝘼𝙄 𝘽𝙀𝙃𝘼𝙉 🔥🥵 ', 'price': '49',
        'validity': '180 days', 'videos': '67000+',
        'image': 'https://ibb.co/9kKCd6ZF', 'qr': 'https://ibb.co/fYsgpT3c',
        'demos': [
'https://t.me/studyof12th/53',
'https://t.me/studyof12th/10',
'https://t.me/studyof12th/55',
'https://t.me/studyof12th/7',
'https://t.me/studyof12th/34',
'https://t.me/studyof12th/49',
'https://t.me/studyof12th/54'
        ],
      'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 MONDAY ✅.'
),
'active': True
    },
      {
        'id': 7, 'name': '𝘽𝙃𝘼𝘽𝙃𝙄 𝙑𝙄𝘿𝙀𝙊𝙎 💦👅 ', 'price': '39',
        'validity': '180 days', 'videos': '56000+',
        'image': 'https://ibb.co/HLw36KQ4', 'qr': 'https://ibb.co/4n9q8mK2',
        'demos': [
'https://t.me/studyof12th/48',
'https://t.me/studyof12th/62',
'https://t.me/studyof12th/21',
'https://t.me/studyof12th/23',
'https://t.me/studyof12th/29',
'https://t.me/studyof12th/36'
        ],
      'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 TUESDAY ✅.'
),
'active': True
    },
      {
        'id': 8, 'name': '𝘽𝘼𝘼𝙋 𝘽𝙀𝙏𝙄 🔥💦 ', 'price': '58',
        'validity': '180 days', 'videos': '30000+',
        'image': 'https://ibb.co/5X0hc5dd', 'qr': 'https://ibb.co/xK77FFDK',
        'demos': [
'https://t.me/studyof12th/60',
'https://t.me/studyof12th/59',
'https://t.me/studyof12th/58'
        ],
       'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 WEDNESDAY ✅.'
),
'active': True
    },
      {
        'id': 9, 'name': '𝙂𝙄𝙍𝙇𝙎 𝙒𝙄𝙏𝙃 𝘼𝙉!𝙈@𝙇🔥', 'price': '49',
        'validity': '180 days', 'videos': '18000+',
        'image': 'https://ibb.co/C5KZBm7f', 'qr': 'https://ibb.co/fYsgpT3c',
        'demos': [
'https://t.me/studyof12th/61'
        ],
       'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 THURSDAY ✅.'
),
'active': True
    },
      {
        'id': 10, 'name': '𝗜𝗡𝗦𝗧𝗚𝗥𝗔𝗠 𝗠𝗠𝗦 𝗔𝗟𝗟 😍🔥 ', 'price': '49',
        'validity': '180 days', 'videos': '50000+',
        'image': 'https://ibb.co/Fb6S1mYg', 'qr': 'https://ibb.co/fYsgpT3c',
        'demos': [
'https://t.me/studyof12th/35',
'https://t.me/studyof12th/50',
'https://t.me/studyof12th/63',
'https://t.me/studyof12th/56',
'https://t.me/studyof12th/52'
        ],
       'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 𝙁𝙍𝙄𝘿𝘼𝙔 ✅.'
),
'active': True
    },
    {
        'id': 2, 'name': '𝙈𝙄𝙓 𝙂𝙍𝙊𝙐𝙋 70𝙆 𝙑𝙄𝘿𝙀𝙊𝙎 🥵 ', 'price': '63',
        'validity': '180 days', 'videos': '70000+',
        'image': 'https://ibb.co/qFhKnzcH', 'qr': 'https://ibb.co/tMVzjb0D',
        'demos': [
'https://t.me/studyof12th/31',
'https://t.me/studyof12th/57'
       ],
       'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 SATURDAY ✅.'
),
'active': True
    },
    {
        'id': 3, 'name': '🔥𝗔𝗟𝗟 𝗩𝗜𝗣 𝗠𝗘𝗚𝗔 𝗣𝗔𝗖𝗞 😍', 'price': '169',
        'validity': '180 days', 'videos': '1 lakh+ ',
        'image': 'https://ibb.co/84598K8j', 'qr': 'https://ibb.co/MDWVSzF8',
       'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 SUNDAY ✅.'
),
'active': True
    },
]
# =================== END OF EDITABLE CONTENT =====================
# ============================================================
# BUTTON STYLE
# ============================================================

# ===== EDITABLE CONTENT KE NICHE SE CODE =====
age_verified = set()
STYLE_SERIES = [
    '𝙎𝙐𝙋𝙋𝙇𝙔',
    '𝙎𝙋𝙀𝘾𝙄𝘼𝙇',
    '𝙋𝙍𝙀𝙈𝙄𝙐𝙈',
    '𝙀𝙓𝘾𝙇𝙐𝙎𝙄𝙑𝙀'
]

SUPPORT_LINK = 'https://t.me/xylerigcc'
def button(text, callback_data=None, url=None):
    if url:
        return InlineKeyboardButton(text, url=url)
    return InlineKeyboardButton(text, callback_data=callback_data)


def add_styled(kb, text, callback_data=None, url=None, index=0):
    style = STYLE_SERIES[index % len(STYLE_SERIES)]
    kb.add(button(f'{text}', callback_data, url))


def get_plan(pid):
    for p in PLANS:
        if p.get('id') == pid and p.get('active', True):
            return p
    return None


def send_photo_or_text(chat_id, photo, caption):
    try:
        if photo:
            bot.send_photo(chat_id, photo, caption=caption)
        else:
            bot.send_message(chat_id, caption)
    except Exception:
        bot.send_message(chat_id, caption)


# ===== AGE GATE =====

def send_age_gate(chat_id):
    kb = InlineKeyboardMarkup()
    kb.row(
        button('🔞 18+ YES', 'age_yes'),
        button('❌ NO', 'age_no')
    )
    send_photo_or_text(chat_id, AGE_IMAGE, AGE_CAPTION)
    bot.send_message(chat_id, 'Please select:', reply_markup=kb)


def send_home(chat_id):
    kb = InlineKeyboardMarkup()

    for i, plan in enumerate(PLANS):
        if plan.get('active', True):
            add_styled(
                kb,
                plan['name'],
                f"plan:{plan['id']}",
                index=i
            )

    add_styled(
        kb,
        '🎬 𝘿𝙚𝙢𝙤',
        'demo_menu',
        index=len(PLANS)
    )

    add_styled(
        kb,
        '🆘 𝙎𝙪𝙥𝙥𝙤𝙧𝙩',
        url=SUPPORT_LINK,
        index=len(PLANS) + 1
    )

    send_photo_or_text(chat_id, WELCOME_IMAGE, WELCOME_CAPTION)
    bot.send_message(
        chat_id,
        '👇 Select an option:',
        reply_markup=kb
    )


def send_plans(chat_id):
    kb = InlineKeyboardMarkup()

    for i, plan in enumerate(PLANS):
        if plan.get('active', True):
            add_styled(
                kb,
                plan['name'],
                f"plan:{plan['id']}",
                index=i
            )

    add_styled(
        kb,
        '🎬 𝘿𝙚𝙢𝙤',
        'demo_menu',
        index=len(PLANS)
    )

    add_styled(
        kb,
        '🆘 𝙎𝙪𝙥𝙥𝙤𝙧𝙩',
        url=SUPPORT_LINK,
        index=len(PLANS) + 1
    )

    bot.send_message(
        chat_id,
        '📦 𝙎𝙚𝙡𝙚𝙘𝙩 𝙋𝙡𝙖𝙣:',
        reply_markup=kb
    )


def send_demo_menu(chat_id):
    kb = InlineKeyboardMarkup()

    for i, plan in enumerate(PLANS):
        if plan.get('active', True) and plan.get('demos'):
            add_styled(
                kb,
                f"🎬 {plan['name']}",
                f"demo:{plan['id']}",
                index=i
            )

    kb.add(button('🔙 𝘽𝙖𝙘𝙠', 'home'))

    bot.send_message(
        chat_id,
        '🎬 𝘿𝙚𝙢𝙤 𝙎𝙚𝙘𝙩𝙞𝙤𝙣\n\nSelect a plan to view its demo:',
        reply_markup=kb
    )


def send_plan(chat_id, pid):
    plan = get_plan(pid)

    if not plan:
        bot.send_message(chat_id, '❌ Plan not found.')
        return

    caption = plan.get('caption', plan['name'])

    kb = InlineKeyboardMarkup()

    # DEMO BUTTON YAHAN RAHEGA
    if plan.get('demos'):
        kb.add(
            button(
                '🎬 𝘿𝙚𝙢𝙤',
                f"demo:{plan['id']}"
            )
        )

    kb.add(
        button(
            '💳 𝘽𝙪𝙮 𝙉𝙤𝙬',
            f"buy:{plan['id']}"
        )
    )

    kb.add(
        button(
            '🔙 𝘽𝙖𝙘𝙠',
            'plans'
        )
    )

    send_photo_or_text(
        chat_id,
        plan.get('image'),
        caption
    )

    bot.send_message(
        chat_id,
        '👇 Select an option:',
        reply_markup=kb
    )


def send_demo(chat_id, pid):
    plan = get_plan(pid)

    if not plan:
        bot.send_message(chat_id, '❌ Plan not found.')
        return

    demos = plan.get('demos', [])

    if not demos:
        bot.send_message(chat_id, '❌ Demo available nahi hai.')
        return

    for demo in demos:
        if isinstance(demo, dict):
            video = demo.get('video')
            caption = demo.get('caption', '')
        else:
            video = demo
            caption = ''

        try:
            bot.send_video(
                chat_id,
                video,
                caption=caption
            )
        except Exception:
            bot.send_message(
                chat_id,
                '❌ Demo load nahi ho paya.'
            )

    kb = InlineKeyboardMarkup()
    kb.add(
        button(
            '💳 𝘽𝙪𝙮 𝙉𝙤𝙬',
            f"buy:{pid}"
        )
    )
    kb.add(
        button(
            '🔙 𝘽𝙖𝙘𝙠',
            f"plan:{pid}"
        )
    )

    bot.send_message(
        chat_id,
        '👇 Demo dekhne ke baad:',
        reply_markup=kb
    )


# ===== PAYMENT LOCK SYSTEM =====

LOCK_SECONDS = 2 * 60 * 60

plan_locks = {}
active_payment_plan = {}
pending_screenshots = {}
user_waiting_screenshot = set()


def lock_key(user_id, plan_id):
    return f'{user_id}:{plan_id}'


def is_plan_locked(user_id, plan_id):
    key = lock_key(user_id, plan_id)
    locked_until = plan_locks.get(key, 0)

    if locked_until > time.time():
        return True

    if key in plan_locks:
        del plan_locks[key]

    return False


def lock_plan(user_id, plan_id):
    plan_locks[lock_key(user_id, plan_id)] = (
        time.time() + LOCK_SECONDS
    )


def unlock_plan(user_id, plan_id):
    plan_locks.pop(lock_key(user_id, plan_id), None)


def send_payment(chat_id, pid):
    plan = get_plan(pid)

    if not plan:
        bot.send_message(chat_id, '❌ Plan not found.')
        return

    user_id = chat_id

    if is_plan_locked(user_id, pid):
        bot.send_message(
            chat_id,
            '⏳ Is plan ka screenshot already submit ho chuka hai.\n'
            'Same plan dobara 2 hours baad submit kar sakte ho.'
        )
        return

    active_payment_plan[user_id] = pid

    kb = InlineKeyboardMarkup()

    kb.add(
        button(
            '✅ 𝙄 𝙋𝘼𝙄𝘿',
            f"paid:{pid}"
        )
    )

    kb.add(
        button(
            '🔙 𝘽𝙖𝙘𝙠',
            f"plan:{pid}"
        )
    )

    caption = plan.get(
        'payment_caption',
        f"💳 Payment for {plan['name']}"
    )

    send_photo_or_text(
        chat_id,
        plan.get('qr'),
        caption
    )

    bot.send_message(
        chat_id,
        'Payment karne ke baad neeche button dabao.\n'
        'Screenshot bhi directly bhej sakte ho.',
        reply_markup=kb
    )


# ===== START =====

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if user_id not in age_verified:
        send_age_gate(message.chat.id)
        return

    send_home(message.chat.id)


# ===== AGE CALLBACKS =====

@bot.callback_query_handler(func=lambda call: call.data == 'age_yes')
def age_yes(call):
    age_verified.add(call.from_user.id)

    bot.answer_callback_query(call.id, 'Access granted ✅')

    try:
        bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )
    except Exception:
        pass

    send_home(call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == 'age_no')
def age_no(call):
    bot.answer_callback_query(call.id)

    bot.send_message(
        call.message.chat.id,
        DENIED_CAPTION
    )


# ===== MENU CALLBACKS =====

@bot.callback_query_handler(func=lambda call: call.data == 'home')
def home_callback(call):
    bot.answer_callback_query(call.id)
    send_home(call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == 'plans')
def plans_callback(call):
    bot.answer_callback_query(call.id)
    send_plans(call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == 'demo_menu')
def demo_menu_callback(call):
    bot.answer_callback_query(call.id)
    send_demo_menu(call.message.chat.id)


# ===== PLAN CALLBACK =====

@bot.callback_query_handler(
    func=lambda call: call.data.startswith('plan:')
)
def plan_callback(call):
    bot.answer_callback_query(call.id)

    pid = call.data.split(':', 1)[1]

    send_plan(
        call.message.chat.id,
        pid
    )


# ===== DEMO CALLBACK =====

@bot.callback_query_handler(
    func=lambda call: call.data.startswith('demo:')
)
def demo_callback(call):
    bot.answer_callback_query(call.id)

    pid = call.data.split(':', 1)[1]

    send_demo(
        call.message.chat.id,
        pid
    )


# ===== BUY CALLBACK =====

@bot.callback_query_handler(
    func=lambda call: call.data.startswith('buy:')
)
def buy_callback(call):
    bot.answer_callback_query(call.id)

    pid = call.data.split(':', 1)[1]

    if is_plan_locked(
        call.from_user.id,
        pid
    ):
        bot.send_message(
            call.message.chat.id,
            '⏳ Is plan ka screenshot already submit ho chuka hai.\n'
            '2 hours baad same plan dobara submit kar sakte ho.'
        )
        return

    send_payment(
        call.message.chat.id,
        pid
    )


# ===== PAID CALLBACK =====

@bot.callback_query_handler(
    func=lambda call: call.data.startswith('paid:')
)
def paid_callback(call):
    bot.answer_callback_query(call.id)

    pid = call.data.split(':', 1)[1]

    if is_plan_locked(
        call.from_user.id,
        pid
    ):
        bot.send_message(
            call.message.chat.id,
            '⏳ Same plan ka screenshot already submit ho chuka hai.'
        )
        return

    active_payment_plan[
        call.from_user.id
    ] = pid

    user_waiting_screenshot.add(
        call.from_user.id
    )

    bot.send_message(
        call.message.chat.id,
        '📸 Ab payment ka screenshot bhejo.'
    )


# ===== SCREENSHOT HANDLER =====

@bot.message_handler(
    content_types=['photo']
)
def screenshot_handler(message):
    user_id = message.from_user.id

    # Agar user ne payment plan select kiya hai
    pid = active_payment_plan.get(user_id)

    # Agar I PAID press kiya tha to bhi chalega
    # Aur agar screenshot directly bheja hai to bhi chalega
    if not pid:
        bot.send_message(
            message.chat.id,
            '❌ Pehle koi plan select karke payment page open karo.'
        )
        return

    if is_plan_locked(
        user_id,
        pid
    ):
        bot.send_message(
            message.chat.id,
            '⏳ Is plan ka screenshot already submit ho chuka hai.'
        )
        return

    photo_id = message.photo[-1].file_id

    pending_screenshots[user_id] = {
        'plan_id': pid,
        'photo_id': photo_id,
        'username': message.from_user.username,
        'name': message.from_user.first_name
    }

    user_waiting_screenshot.discard(user_id)

    caption = (
        '📥 𝙉𝙀𝙒 𝙋𝘼𝙔𝙈𝙀𝙉𝙏 𝙎𝘾𝙍𝙀𝙀𝙉𝙎𝙃𝙊𝙏\n\n'
        f'👤 User ID: {user_id}\n'
        f'👤 Username: @{message.from_user.username or "N/A"}\n'
        f'📦 Plan: {pid}'
    )

    kb = InlineKeyboardMarkup()

    kb.row(
        button(
            '✅ Approve',
            f"approve:{user_id}:{pid}"
        ),
        button(
            '❌ Reject',
            f"reject:{user_id}:{pid}"
        )
    )

    bot.send_photo(
        ADMIN_ID,
        photo_id,
        caption=caption,
        reply_markup=kb
    )

    bot.send_message(
        message.chat.id,
        '✅ Screenshot admin ko bhej diya gaya hai.\n'
        'Approval ka wait karo.'
    )


# ===== ADMIN REVIEW =====

@bot.callback_query_handler(
    func=lambda call: call.data.startswith('approve:')
    or call.data.startswith('reject:')
)
def review_callback(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(
            call.id,
            '❌ Not allowed.',
            show_alert=True
        )
        return

    parts = call.data.split(':')

    action = parts[0]
    user_id = int(parts[1])
    pid = parts[2]

    if action == 'approve':
        lock_plan(
            user_id,
            pid
        )

        bot.answer_callback_query(
            call.id,
            'Approved ✅'
        )

        bot.send_message(
            user_id,
            f'✅ Payment approved!\n'
            f'📦 Plan: {pid}'
        )

    else:
        unlock_plan(
            user_id,
            pid
        )

        bot.answer_callback_query(
            call.id,
            'Rejected ❌'
        )

        bot.send_message(
            user_id,
            f'❌ Payment rejected.\n'
            f'📦 Plan: {pid}\n\n'
            'Agar payment ki hai to correct screenshot dobara bhejo.'
        )

    pending_screenshots.pop(
        user_id,
        None
    )


# ===== POLLING =====

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO
    )

    bot.infinity_polling(
        skip_pending=True
    )
