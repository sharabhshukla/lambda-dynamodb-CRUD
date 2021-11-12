from pydantic import BaseModel
from datetime import date


class InputData(BaseModel):
    Country: str
    dt: date
    AverageTemperature: str
    AverageTemperatureUncertainty: str
