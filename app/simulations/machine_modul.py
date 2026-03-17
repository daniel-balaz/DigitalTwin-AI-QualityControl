from app.data_modul import Data, Config
from app.logics.calculation_modul import Calculation
from app.logics.logic_modul import Logic
from app.outputs.output_modul import Output
from app.simulations.physical_modul import PhysicalModel
import random

class Machine():
    def __init__(self, data: Data, cfg: Config, calculation: Calculation, logic: Logic, output: Output, physical_model: PhysicalModel) -> None:
        self.data = data
        self.cfg = cfg
        self.calculation = calculation
        self.logic = logic
        self.output = output
        self.physical_model = physical_model

    def main(self) -> None:
        self.check()  
        if self.data.state != self.cfg.CRITICAL:
            self.press()
        else: 
            self.cooling()
            self.data.critical_round += 1

        if self.data.critical_round >= 5:
            self.data.is_running = False

    def cooling(self) -> None:
        self.data.cooling = self.data.median_oil_temp >= self.cfg.optimal_oil_temp
        if self.data.cooling:
            self.data.cooling_efficienty = max((self.data.score / 100) * self.data.strength_fan_error, 0.01)
            self.data.current_oil_temp -= (self.cfg.cooling_strength * self.data.cooling_efficienty) + random.uniform(-self.cfg.noise, self.cfg.noise)

    def check(self) -> None:
        self.calculation.main()
        self.logic.main()
        self.output.main()

    def press(self):
        self.physical_model.get_pressure()
        self.physical_model.get_warmer()
        self.cooling()