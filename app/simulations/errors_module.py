from app.data_modul import Data, Config
import random

class States():
    def __init__(self, data: Data, cfg: Config) -> None:
        self.data = data
        self.cfg = cfg

    def main(self) -> None:
        self.fan_error()
        self.casting_state()

    def fan_error(self) -> None:
        if self.data.cooling:
            self.data.chance_fan_error += self.data.fan_error_round_add * self.data.cooling_efficienty
        
        if random.random() < self.data.chance_fan_error and not self.data.fan_error:
            self.data.fan_error = True

        if self.data.fan_error:
            self.data.strength_fan_error -= self.data.fan_error_round_add
    
    def casting_state(self):
        self.data.casting_def_chance = ((self.data.score * 0.2) + self.data.median_oil_temp + (self.data.num_round * 0.1)) / 1000
        if random.random() <= self.data.casting_def_chance:
            self.data.casting_def = True
        else: self.data.casting_def = False



        