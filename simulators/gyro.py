import time
import random

def run_gyro_simulator(delay, callback, stop_event, publish_event, settings):
    print(f"Starting {settings['name']} simulator")
    while not stop_event.is_set():
        # Simuliramo vrednosti akcelerometra i ziroskopa
        accel = [random.uniform(-1, 1) for _ in range(3)]
        gyro = [random.uniform(-10, 10) for _ in range(3)]

        # ne okida
        # accel = [random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), random.uniform(9.7, 9.9)]
        # gyro = [random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0)]

        callback(accel, gyro, publish_event, settings)
        time.sleep(delay)