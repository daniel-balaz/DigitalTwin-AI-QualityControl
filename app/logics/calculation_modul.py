import statistics
from app.data_modul import Data, Config

class Calculation():
    def __init__(self, data: Data, cfg: Config) -> None:
        self.data = data
        self.cfg = cfg
    
    def main(self) -> None:
        self.get_list()
        self.get_metrics()

    def get_list(self) -> None:
        self.data.list_oil_temp.append(self.data.current_oil_temp)

    def get_metrics(self) -> None:
        self.data.median_oil_temp = statistics.median(self.data.list_oil_temp)
        self.data.avg_oil_temp = sum(self.data.list_oil_temp) / len(self.data.list_oil_temp)