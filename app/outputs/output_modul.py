from app.data_modul import Data, Config
import httpx
import os
import logging 

class Output():
    def __init__(self, data: Data, cfg: Config, temp_gauge, pressure_gauge, score_gauge) -> None:
        self.data = data
        self.cfg = cfg

        self.TEMP_GAUGE = temp_gauge
        self.PRESSURE_GAUGE = pressure_gauge
        self.SCORE_GAUGE = score_gauge

    def main(self):
        self.do_logging()

    def do_logging(self) -> None:
        if self.data.state != self.cfg.NORMAL:
            if self.data.state == self.cfg.CRITICAL and not self.data.is_critical:
                logging.critical(f"Oil temp: [{self.data.current_oil_temp}°C]")
                self.data.msg = f"{self.data.state} | Oil temp: [{round(self.data.current_oil_temp, 1)}°C]"
                self.data.is_critical = True

            elif self.data.state == self.cfg.WARNING and not self.data.is_warned:
                logging.warning(f"Oil temp: [{self.data.current_oil_temp}°C]")
                self.data.msg = f"{self.data.state} | Oil temp: [{round(self.data.current_oil_temp, 1)}°C]"
                self.data.is_warned = True

            elif self.data.state == self.cfg.NOTICE and not self.data.is_notice:
                logging.error(f"Oil temp: [{self.data.current_oil_temp}°C]")
                self.data.msg = f"{self.data.state} | Oil temp: [{round(self.data.current_oil_temp, 1)}°C]"
                self.data.is_notice = True
            
        else:
            self.data.is_notice = False
            self.data.is_warned = False
            self.data.is_critical = False

    async def prometheus_output(self) -> None:
        self.TEMP_GAUGE.set(self.data.current_oil_temp)
        self.PRESSURE_GAUGE.set(self.data.current_pressure)
        self.SCORE_GAUGE.set(self.data.score)

    async def send_telegram_async(self):
        TOKEN = os.getenv("TOKEN")
        CHAT_ID = os.getenv("CHAT_ID")

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": f"ID: [{self.cfg.MACHINE_ID}] | HALL: [{self.cfg.HALL}]\n{self.data.msg}",
        }
        
        async with httpx.AsyncClient() as client:
            try:
                r = await client.post(url, data=payload)
                self.data.msg = ""
                if r.status_code != 200:
                    logging.error(f"Chyba při snaze spojit se s telegramem | Chyba: {r.text} | Kod chyby: {r.status_code}")

            except Exception as e:
                print(f"output_module | Error: {e}")
