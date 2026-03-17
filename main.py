import logging
from prometheus_client import start_http_server, Gauge
import asyncio
from dotenv import load_dotenv
import os
import random

from app.data_modul import Data, Config
from app.logics.logic_modul import Logic
from app.outputs.output_modul import Output
from app.simulations.physical_modul import PhysicalModel
from app.logics.calculation_modul import Calculation
from app.simulations.machine_modul import Machine
from app.simulations.errors_module import States
from app.cv_modul import CV_Model

TEMP_GAUGE = Gauge('machine_oil_temperature', 'Aktuální teplota oleje v stupních C')
PRESSURE_GAUGE = Gauge('machine_oil_pressure', 'Aktuální tlak oleje')
SCORE_GAUGE = Gauge('machine_health_score', 'Stav stroje vyjádřený skóre')

load_dotenv()

#-----------------------------------------------------------------------------------------------------------------------------

async def main():
    start_http_server(8000)

    data = Data()
    cfg = Config()
    cv_model = CV_Model(data, cfg)
    calculation = Calculation(data, cfg)
    logic = Logic(data, cfg)
    output = Output(data, cfg, TEMP_GAUGE, PRESSURE_GAUGE, SCORE_GAUGE)
    physical_model = PhysicalModel(data, cfg)
    states = States(data, cfg)
    machine = Machine(data, cfg, calculation, logic, output, physical_model)

    while data.is_running:
        try:
            machine.main()
            states.main()

        # Computer Vision Check
            subfolder = "def_front" if data.casting_def else "ok_front"

            folder_path = os.path.join("app", "camera_feed", subfolder)

            if os.path.exists(folder_path):
                files = [f for f in os.listdir(folder_path) if f.endswith(('.jpeg'))]
                
                if files:
                    random_photo = os.path.join(folder_path, random.choice(files))
                    
                    data.is_defect_confirmed = await cv_model.analyze(random_photo)
            
            if data.is_defect_confirmed:
                machine.cooling()
                data.msg = "Defect was detected."
                await output.send_telegram_async()

        # Output
            await output.prometheus_output()

            if data.msg != "": await output.send_telegram_async()

            await asyncio.sleep(5)

            data.num_round += 1

        except Exception as e:
            logging.error(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())