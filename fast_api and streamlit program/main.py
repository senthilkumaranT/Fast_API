from fastapi import FastAPI, Response
from calculator import calculator
from pydantic import BaseModel
import uvicorn
from fastapi.responses import StreamingResponse
import json

app = FastAPI()


class CalculatorInput(BaseModel):
    x: float
    y: float
    operation: str

@app.post("/calculator")
async def calculator_api(input: CalculatorInput, response: Response):
    result = calculator(input.x, input.y, input.operation)
    response.headers["Content-Type"] = "application/json"
    
    async def generate():
        yield json.dumps({"result": result})

    return StreamingResponse(generate(), media_type="application/json")
