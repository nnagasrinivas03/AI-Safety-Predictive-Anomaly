import random
import time


def generate_sensor_data():

    return {

        "air_temperature":
            round(
                random.uniform(
                    295,
                    305
                ),
                2
            ),

        "process_temperature":
            round(
                random.uniform(
                    305,
                    315
                ),
                2
            ),

        "rotational_speed":
            round(
                random.uniform(
                    1200,
                    1800
                ),
                2
            ),

        "torque":
            round(
                random.uniform(
                    20,
                    60
                ),
                2
            ),

        "tool_wear":
            round(
                random.uniform(
                    0,
                    250
                ),
                2
            )
    }


if __name__ == "__main__":

    while True:

        data = generate_sensor_data()

        print(data)

        time.sleep(1)