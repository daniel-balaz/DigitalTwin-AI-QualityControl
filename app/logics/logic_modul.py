from app.data_modul import Data, Config

class Logic():
    def __init__(self, data: Data, cfg: Config) -> None:
        self.data = data
        self.cfg = cfg

    def main(self) -> None:
        self.point_system()
        self.data.state = self.brain()

    def point_system(self) -> None:
        range = self.cfg.critical_oil_temp - self.cfg.optimal_oil_temp
        self.data.score = ((((self.data.current_oil_temp - self.cfg.optimal_oil_temp) / range) * 100) + (((self.data.avg_oil_temp - self.cfg.optimal_oil_temp) / range) * 50))

    def brain(self) -> str:
        if self.data.score >= self.cfg.critical:
            return self.cfg.CRITICAL
        elif self.data.score >= self.cfg.warning:
            return self.cfg.WARNING
        elif self.data.score >= self.cfg.notice:
            return self.cfg.NOTICE

        else:
            return self.cfg.NORMAL 
