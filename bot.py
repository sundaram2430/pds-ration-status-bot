import os
import telebot

TOKEN = "8704647095:AAGwRDbbznCaSL6v9bCEw7TdhGMyqI-1J90"
bot = telebot.TeleBot(TOKEN)

# ============================================================
# RATION DATA
# ============================================================
ration_data = {
    "CARD001": {"name": "Vibishan",  "month": "April 2026", "aRice": 5, "rRice": 5, "aWheat": 3, "rWheat": 3},
    "CARD002": {"name": "Tapaswi",   "month": "April 2026", "aRice": 5, "rRice": 3, "aWheat": 3, "rWheat": 1},
    "CARD003": {"name": "Gajodhar",  "month": "April 2026", "aRice": 5, "rRice": 0, "aWheat": 3, "rWheat": 0},
    "CARD004": {"name": "Bheem",     "month": "April 2026", "aRice": 5, "rRice": 3, "aWheat": 3, "rWheat": 2},
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "Welcome to PDS Ration Checker!\n\n"
        "Send your Card Number to check status.\n\n"
        "Example: CARD001\n\n"
        "PDS Helpline: 1967"
    )

@bot.message_handler(func=lambda message: True)
def check_ration(message):
    card = message.text.strip().upper()
    
    if card not in ration_data:
        bot.reply_to(message,
            f"Card '{card}' not found.\n"
            "Please check and try again.\n"
            "Example: CARD001"
        )
        return
    
    d = ration_data[card]
    r_short = d["aRice"]  - d["rRice"]
    w_short = d["aWheat"] - d["rWheat"]
    
    if r_short <= 0 and w_short <= 0:
        status = "FULL - Complete entitlement received!"
    elif d["rRice"] == 0 and d["rWheat"] == 0:
        status = "PENDING - Nothing distributed yet."
    else:
        status = "PARTIAL - You received less than entitled!"
    
    reply = (
        "============================\n"
        "PDS RATION STATUS REPORT\n"
        "============================\n"
        f"Name   : {d['name']}\n"
        f"Card   : {card}\n"
        f"Month  : {d['month']}\n"
        "----------------------------\n"
        "RICE\n"
        f"  Entitled : {d['aRice']} kg\n"
        f"  Received : {d['rRice']} kg\n"
        f"  Shortfall: {max(0, r_short)} kg\n"
        "----------------------------\n"
        "WHEAT\n"
        f"  Entitled : {d['aWheat']} kg\n"
        f"  Received : {d['rWheat']} kg\n"
        f"  Shortfall: {max(0, w_short)} kg\n"
        "============================\n"
        f"Status: {status}\n"
        "============================\n"
        "Helpline: 1967"
    )
    bot.reply_to(message, reply)

print("Bot is running...")
bot.polling()
