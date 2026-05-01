# DigitalTwin-AI-QualityControl

Tento projekt simuluje a monitoruje provoz vstřikovacího lisu v rámci průmyslu 4.0. Systém kombinuje fyzikální simulaci stroje, logiku prediktivní údržby, počítačové vidění pro detekci vad a moderní monitorovací stack (Prometheus, Grafana).

## Klíčové vlastnosti
* **Fyzikální simulace:** Modelování vztahu mezi teplotou oleje a tlakem.
* **AI Kontrola kvality:** Integrace s Roboflow pro detekci vad na výliscích pomocí Computer Vision.
* **Pokročilý Scoring:** Algoritmus vyhodnocující "zdraví" stroje na základě aktuální a průměrné teploty[cite: 1].
* **Simulace poruch:** Modelování opotřebení ventilátoru a jeho vlivu na chlazení.
* **Monitoring & Alerting:** Export metrik do Prometheus/Grafana a odesílání kritických stavů na Telegram.

## Architektura systému
Projekt je rozdělen do modulů pro snadnou údržbu a škálovatelnost:
* `machine_modul.py`: Hlavní řídicí jednotka stroje (stavy, chlazení).
* `logic_modul.py`: Rozhodovací logika a bodový systém[cite: 1].
* `physical_modul.py`: Výpočet fyzikálních veličin (teplota, tlak).
* `cv_modul.py`: AI analýza obrazu z "kamerového feedu".
* `output_modul.py`: Komunikace s externími API a logování.

## Technologický stack
* **Jazyk:** Python 3.x (Asyncio)
* **Kontejnerizace:** Docker & Docker Compose
* **Sběr dat:** Prometheus
* **Vizualizace:** Grafana
* **AI/ML:** Roboflow (Object Detection)
* **Komunikace:** Telegram Bot API (httpx)

## Rychlé spuštění
Projekt je plně kontejnerizován. Pro spuštění celého stacku stačí mít nainstalovaný Docker a spustit:

```bash
docker-compose up --build
