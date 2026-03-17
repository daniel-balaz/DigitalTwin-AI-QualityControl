from roboflow import Roboflow
from app.data_modul import Data, Config
import os
import cv2
import logging

class CV_Model():
    def __init__(self, data: Data, cfg: Config):
        self.rf = Roboflow(api_key=os.getenv("ROBOFLOW_API"))
        self.project = self.rf.workspace().project("maturita_project")
        self.model = self.project.version(2).model
        
        logging.debug("AI Model byl úspěšně připraven!")
        
    async def analyze(self, image_path):
            try:
                prediction_data = self.model.predict(image_path).json() # type: ignore
                
                img = cv2.imread(image_path)
                print(image_path)
                if img is None: return False

                label = "unknown"
                confidence = 0.0

                if 'predictions' in prediction_data and len(prediction_data['predictions']) > 0:
                    data_hlavni_uroven = prediction_data['predictions'][0]
                    
                    label = data_hlavni_uroven.get('top', 'unknown')
                    confidence = data_hlavni_uroven.get('confidence', 0.0)

                is_defect = (label == "def_front")
                color = (0, 0, 255) if is_defect else (0, 255, 0)
                
                text = f"AI: {label} ({round(confidence * 100, 1)}%)"
                cv2.putText(img, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
                cv2.imshow("Kontrola kvality - AI", img)
                cv2.waitKey(1)
                
                logging.debug(f"AI DETEKCE: {label} ({confidence}%)")

                return is_defect

            except Exception as e:
                error = f"Chyba: {e}"
                logging.error(error)
                return False