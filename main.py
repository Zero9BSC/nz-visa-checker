import os
import sys
import requests

URL = "https://onlineservices.immigration.govt.nz/WorkingHoliday/"
KEYWORD = '<span id="ContentPlaceHolder1_countryRepeater_countryStatus_0">OPEN</span>'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(msg):
    if TOKEN and CHAT_ID:
        endpoint = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(endpoint, json={"chat_id": CHAT_ID, "text": msg})

def check_visa():
    try:
        res = requests.get(URL, headers=HEADERS, timeout=15)
        res.raise_for_status()
        
        if KEYWORD in res.text:
            send_telegram_alert("🚨 ¡ATENCIÓN Franco! La Working Holiday de Argentina pasó a estado OPEN. Entra ya a la web.")
        else:
            print("Sigue cerrada. Chequeo OK.")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión omitido: {e}")
        sys.exit(0)

if __name__ == "__main__":
    check_visa()