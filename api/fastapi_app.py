from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Air Supply System Monitoring API")

class AirSystemReadings(BaseModel):
    """
    Schema for compressed air system monitoring. 
    Focuses on pressure drops and flow rates to detect leaks and clogged filters.
    """
    runtime_hours: float = Field(..., ge=0, description="Compressor run time")
    line_pressure_bar: float = Field(..., ge=0, le=15, description="Main line pressure")
    filter_delta_p: float = Field(..., ge=0, le=5, description="Pressure drop across filters")
    leak_rate_cfm: float = Field(..., ge=0, description="Flow measured during idle periods")

def air_heuristic_predict(leak_rate: float, delta_p: float) -> int:
    """
    Logic: If leak rate is high (> 5.0 CFM) OR filter pressure drop 
    is excessive (> 1.2 Bar), maintenance is required.
    """
    return int((leak_rate > 5.0) or (delta_p > 1.2))

@app.post("/predict")
def predict_maintenance(readings: AirSystemReadings):
    y_pred = air_heuristic_predict(readings.leak_rate_cfm, readings.filter_delta_p)
    
    if y_pred == 1:
        action = (
            "MAINTENANCE REQUIRED. Detected excessive air leaks (>5 CFM) "
            "or high pressure drop (>1.2 Bar) across filtration. "
            "Inspect system for leaks and replace filter elements."
        )
    else:
        action = "SYSTEM EFFICIENT. Pressure and leak rates within normal operating range."

    return {
        "prediction": y_pred,
        "action_required": action,
        "inputs": readings.model_dump()
    }
