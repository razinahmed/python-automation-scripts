import requests
from bs4 import BeautifulSoup
import time
import argparse
import os

# To use this script, set your Telegram bot token and chat ID as environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials missing. Printing to console instead:")
        print(f"🔔 ALERT: {message}")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send Telegram alert: {e}")

def check_price(url: str, target_price: float, css_selector: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.select_one(css_selector)
        
        if not price_element:
            print("Could not find the price element on the page.")
            return False
            
        # Clean price text (e.g. "$1,299.99" -> 1299.99)
        price_text = price_element.get_text().strip().replace('$', '').replace(',', '')
        current_price = float(price_text)
        
        print(f"Current price: ${current_price:.2f}")
        
        if current_price <= target_price:
            send_telegram_alert(f"🚨 <b>PRICE DROP ALERT!</b> 🚨\n\nThe item has hit your target price of ${target_price}!\nCurrent Price: ${current_price}\nLink: {url}")
            return True
        return False
        
    except Exception as e:
        print(f"Error checking price: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Headless Price Scraper Monitor")
    parser.add_argument("--url", "-u", type=str, required=True, help="URL to monitor")
    parser.add_argument("--target", "-t", type=float, required=True, help="Target price to alert at")
    parser.add_argument("--selector", "-s", type=str, required=True, help="CSS Selector for the price element")
    parser.add_argument("--interval", "-i", type=int, default=3600, help="Check interval in seconds (default 1 hour)")
    
    args = parser.parse_args()
    
    print(f"Monitoring {args.url} for price <= ${args.target}")
    
    while True:
        hit_target = check_price(args.url, args.target, args.selector)
        if hit_target:
            print("Target hit! Exiting monitor.")
            break
            
        print(f"Waiting {args.interval} seconds before next check...")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
