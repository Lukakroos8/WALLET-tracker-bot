import requests
import time
import os
from config import Config

config = Config()

def get_latest_signature():
    url = f"https://api.helius.xyz/v0/addresses/{config.wallet_address}/transactions?limit=1&api-key={config.helius_api_key}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if data:
        return data[0]['signature']
    return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": config.telegram_chat_id,
        "text": message
    }
    requests.post(url, json=payload)

def load_last_signature():
    if os.path.exists(config.last_signature_file):
        with open(config.last_signature_file, 'r') as file:
            return file.read().strip()
    return None

def save_last_signature(signature):
    with open(config.last_signature_file, 'w') as file:
        file.write(signature)

def monitor_wallet():
    while True:
        try:
            latest = get_latest_signature()
            last_saved = load_last_signature()
            if latest and latest != last_saved:
                send_telegram_message(f"💸 Transaksi baru terdeteksi di wallet!\n\nSignature: {latest}")
                save_last_signature(latest)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(config.polling_interval)

if __name__ == "__main__":
    monitor_wallet()
