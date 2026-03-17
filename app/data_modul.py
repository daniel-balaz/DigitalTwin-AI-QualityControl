from dataclasses import dataclass, field
from collections import deque
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
# Machine Info
    MACHINE_ID = os.getenv("machine_id", "default_machine")
    HALL = os.getenv("hall", "default_hall")

    # Temp a Pressure
    optimal_oil_temp: float = float(os.getenv("optimal_oil_temp", "40.0"))
    critical_oil_temp: float = float(os.getenv("critical_oil_temp", "80.0"))
    optimal_pressure:float = float(os.getenv("optimal_pressure", "150.0") )

    pressure_loss_coefficient: float = 0.004
    step_temp: float = 5.0

# Data
    noise: float = 1.0

    # Cooling Strength
    cooling_strength: float = 10.0

    # Lists
    lists_len: int = 10

    # Status
    notice: int = 40
    warning: int = 50
    critical: int = 80  

    NORMAL: str = "NORMAL"
    NOTICE: str = "NOTICE"
    WARNING: str = "WARNING"
    CRITICAL: str = "CRITICAL"

#-----------------------------------------------------------------------------------------------------------------------------

@dataclass
class Data:
# Teplota
    ambient_temp: float = 25.0
    current_oil_temp: float = 25.0

    # Avg Temp
    avg_oil_temp: float = 25.0

    # Median Temp
    median_oil_temp: float = 25.0

    # Oil Temp List
    list_oil_temp: deque = field(default_factory=lambda: deque(maxlen=10))

    # Cooling Efficienty
    cooling_efficienty: float = 0.0

# Pressure
    current_pressure: float = 150.0

# Data
    is_running: bool = True
    state: str = "NORMAL"
    cooling: bool = False
    msg: str = ""
    num_round: int = 0
    critical_round: int = 0
    
# Point System
    score: float = 0.0

# CV
    casting_def_chance: float = 0.0
    casting_def: bool = False
    is_defect_confirmed: bool = False

# Status
    is_notice: bool = False
    is_warned: bool = False
    is_critical: bool = False

# Errors
    # Fan Error
    chance_fan_error: float = 0.5
    fan_error_round_add: float = 0.001
    strength_fan_error: float = 1.0
    fan_error: bool = False