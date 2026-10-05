import asyncio
import csv
import os
import random
from datetime import datetime

from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.model import predict_anomaly


app = FastAPI(
    title="AI Safety Predictive Anomaly System",
    version="1.0"
)


# ---------------------------------------
# FRONTEND
# ---------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)


# ---------------------------------------
# LOG DIRECTORY
# ---------------------------------------

os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/anomaly_logs.csv"


if not os.path.exists(LOG_FILE):

    with open(
        LOG_FILE,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "air_temperature",
            "process_temperature",
            "rotational_speed",
            "torque",
            "tool_wear",
            "status",
            "anomaly_score"
        ])


# ---------------------------------------
# HOME
# ---------------------------------------

@app.get("/")
async def home():

    return FileResponse(
        "frontend/index.html"
    )


# ---------------------------------------
# HEALTH CHECK
# ---------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "online",
        "system": "AI Safety Predictive Anomaly Detection"
    }


# ---------------------------------------
# WEBSOCKET
# ---------------------------------------

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    await websocket.accept()

    print("Live monitoring client connected.")

    try:

        while True:

            # --------------------------------
            # LIVE SENSOR DATA
            # --------------------------------

            air_temperature = round(
                random.uniform(295, 305),
                2
            )

            process_temperature = round(
                random.uniform(305, 315),
                2
            )

            rotational_speed = round(
                random.uniform(1200, 1800),
                2
            )

            torque = round(
                random.uniform(20, 60),
                2
            )

            tool_wear = round(
                random.uniform(0, 250),
                2
            )


            # --------------------------------
            # OCCASIONAL ABNORMAL CONDITION
            # --------------------------------

            if random.random() < 0.08:

                air_temperature = round(
                    random.uniform(310, 320),
                    2
                )

                process_temperature = round(
                    random.uniform(320, 330),
                    2
                )

                rotational_speed = round(
                    random.uniform(500, 900),
                    2
                )

                torque = round(
                    random.uniform(70, 100),
                    2
                )

                tool_wear = round(
                    random.uniform(220, 300),
                    2
                )


            # --------------------------------
            # AI PREDICTION
            # --------------------------------

            result = predict_anomaly(

                air_temperature,

                process_temperature,

                rotational_speed,

                torque,

                tool_wear

            )


            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )


            # --------------------------------
            # LOG DATA
            # --------------------------------

            with open(
                LOG_FILE,
                "a",
                newline=""
            ) as file:

                writer = csv.writer(file)

                writer.writerow([

                    timestamp,

                    air_temperature,

                    process_temperature,

                    rotational_speed,

                    torque,

                    tool_wear,

                    result["status"],

                    result["anomaly_score"]

                ])


            # --------------------------------
            # SEND TO FRONTEND
            # --------------------------------

            response = {

                "timestamp": timestamp,

                "air_temperature":
                    air_temperature,

                "process_temperature":
                    process_temperature,

                "rotational_speed":
                    rotational_speed,

                "torque":
                    torque,

                "tool_wear":
                    tool_wear,

                "status":
                    result["status"],

                "prediction":
                    result["prediction"],

                "anomaly_score":
                    result["anomaly_score"]

            }


            await websocket.send_json(
                response
            )


            # Send new reading every second

            await asyncio.sleep(1)


    except Exception as error:

        print(
            "WebSocket disconnected:",
            error
        )