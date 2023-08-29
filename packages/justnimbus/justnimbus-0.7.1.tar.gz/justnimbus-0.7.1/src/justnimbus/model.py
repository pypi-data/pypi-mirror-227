import dataclasses
from datetime import datetime


@dataclasses.dataclass
class JustNimbusModel:
    api_version: float
    system_last_update: datetime
    system_flow: str
    reservoir_capacity: float
    reservoir_content: float
    reservoir_temp: float
    pump_type: str
    pump_pressure: float
    water_saved: float
    water_used: float

    @classmethod
    def from_dict(cls, data: dict):
        return JustNimbusModel(
            api_version=float(data["api_version"]),
            system_last_update=datetime.fromisoformat(data["system_last_update"]),
            system_flow=data["system_flow"],
            reservoir_capacity=float(data["reservoir_capacity"]),
            reservoir_content=float(data["reservoir_content"]),
            reservoir_temp=float(data["reservoir_temp"]),
            pump_type=str(data["pump_type"]),
            pump_pressure=float(data["pump_pressure"]),
            water_saved=float(data["water_saved"]),
            water_used=float(data["water_used"]),
        )
