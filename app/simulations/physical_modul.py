from app.data_modul import Data, Config

class PhysicalModel():
    def __init__(self, data: Data, cfg: Config) -> None:
        self.data = data
        self.cfg = cfg
    
    def get_pressure(self) -> None:
        self.data.current_pressure = self.cfg.optimal_pressure * (1 - self.cfg.pressure_loss_coefficient * (self.data.current_oil_temp - self.cfg.optimal_oil_temp))

    def get_warmer(self) -> None:
        self.data.current_oil_temp += self.cfg.step_temp * ((self.cfg.optimal_oil_temp / self.data.current_oil_temp) * (self.data.ambient_temp / self.data.current_oil_temp))