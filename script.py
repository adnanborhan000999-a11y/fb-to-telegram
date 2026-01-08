import requests
import os
import re

FB_PAGE = "https://mbasic.facebook.com/ACSFutureSchool"
STATE_FILE = "last_post.txt"

BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
CHAT_ID = os.environ["TG_CHAT_ID"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(FB_PAGE, headers=headers, timeout=20).text

# Find first post link
match = re.search(r'href="(/story\.php\?[^"]+)"', html)
if not match:
    print("No post found")
    exit()

post_link = "https://mbasic.facebook.com" + match.group(1).replace("&amp;", "&")

last_post = ""
if os.path.exists(STATE_FILE):
    last_post = open(STATE_FILE).read().strip()

if post_link == last_post:
    print("No new post")
    exit()

# Save new post
with open(STATE_FILE, "w") as f:
    f.write(post_link)

message = f"📢 New Facebook post\n\n{post_link.replace('mbasic.', '')}"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": False
    }
)

print("Posted to Telegram")
