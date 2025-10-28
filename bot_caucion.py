import requests
from bs4 import BeautifulSoup
import schedule
import time
import smtplib
from email.mime.text import MIMEText

def obtener_tasa_caucion():
    url = "https://iol.invertironline.com/mercado/cotizaciones/argentina/cauciones"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) "
            "Gecko/20100101 Firefox/130.0"
        ),
        "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,*/*;q=0.8"
        ),
    }

    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200:
            print(f"[IOL] Error {r.status_code}")
            return None

        soup = BeautifulSoup(r.text, "html.parser")

        for tr in soup.select("table#cotizaciones tbody tr"):
            cols = [c.get_text(strip=True) for c in tr.find_all("td")]
            if len(cols) >= 6 and cols[0] == "1" and cols[1].upper() == "PESOS":
                tasa_str = cols[5]
                return float(tasa_str.replace("%", "").replace(",", "."))
    except Exception as e:
        print("[IOL] Excepción:", e)

    return None

def obtener_tasa_billetera():
    url = "https://billeterasvirtuales.com.ar/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) "
            "Gecko/20100101 Firefox/130.0"
        ),
        "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
    }

    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200:
            print(f"[Billeteras] Error {r.status_code}")
            return None

        soup = BeautifulSoup(r.text, "html.parser")
        tasas = []

        for node in soup.find_all(string=True):
            text = node.strip()
            if text.endswith("%"):
                try:
                    valor = float(text.replace("%", "").replace(",", "."))
                    tasas.append(valor)
                except ValueError:
                    pass

        return max(tasas) if tasas else None
    except Exception as e:
        print("[Billeteras] Excepción:", e)
        return None

def enviar_mail(asunto, cuerpo):
    remitente = "tumail@mail.com"
    destinatario = "destinatario@mail.com"
    password = "tu password"

    msg = MIMEText(cuerpo)
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(remitente, password)
            server.sendmail(remitente, destinatario, msg.as_string())
        print(f"Enviado: {asunto}")
    except Exception as e:
        print("Error al enviar mail:", e)

def verificar_tasas():
    caucion = obtener_tasa_caucion()
    billetera = obtener_tasa_billetera()
    print(f"Caución: {caucion}%  |  Billetera top: {billetera}%")

    if caucion and billetera:
        if caucion > billetera:
            enviar_mail(
                "Caución superior a billeteras",
                f"La caución ({caucion}%) supera la billetera ({billetera}%).",
            )
        if caucion > 70:
            enviar_mail(
                "ALERTA: Caución alta",
                f"La caución tomadora está en {caucion}% TNA.",
            )

def main():
    print("Bot de tasas iniciado...")
    verificar_tasas()
    schedule.every(30).minutes.do(verificar_tasas)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
