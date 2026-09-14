<h1 align="center">
  Smart Home IoT System
</h1>

<p align="center">
  A distributed smart home system built on three Raspberry Pi units communicating over MQTT, with a Python/Flask server handling automation logic, InfluxDB + Grafana for monitoring, and a web dashboard for live control.
</p>

<div align="center">

![Python](https://img.shields.io/badge/Python-3-blue)
![Flask](https://img.shields.io/badge/Flask-server-black)
![MQTT](https://img.shields.io/badge/MQTT-Mosquitto-660066)
![InfluxDB](https://img.shields.io/badge/InfluxDB-2.7-22ADF6)
![Grafana](https://img.shields.io/badge/Grafana-visualization-F46800)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![status](https://img.shields.io/badge/Status-University%20Project-yellow)

</div>

## About the Project

This project implements a smart home automation and security system distributed across three Raspberry Pi devices, each responsible for a different set of sensors and actuators (door sensors, motion detectors, a keypad, temperature/humidity sensors, a gyroscope, RGB lighting, a buzzer, an LCD display, a 4-digit display, and more). All devices communicate asynchronously through an MQTT broker, publishing sensor readings and subscribing to actuator commands.

A central Flask server subscribes to all sensor/actuator topics, persists every reading to InfluxDB, and runs the automation and security logic as a state machine — for example, correlating an ultrasonic sensor with a PIR motion sensor to count people entering/leaving a room, automatically turning lights on/off based on motion, and arming/disarming an alarm system via a PIN entered on a keypad. Grafana is used to visualize the stored sensor data, and a lightweight web dashboard exposes live camera feed, security controls, lighting, and a kitchen stopwatch to the end user.

Each sensor/actuator also has a software simulator, so the full system can be run and tested without physical Raspberry Pi hardware.

## Features

- Three independently running Raspberry Pi nodes (`pi1.py`, `pi2.py`, `pi3.py`), each driving its own set of sensors/actuators over MQTT
- Door and motion sensing (ultrasonic + PIR) combined to detect and count people entering/exiting through two doors
- Automatic lighting control based on motion detection, with a self-resetting "keep on" timer
- PIN-based alarm arming/disarming via a keypad, with automatic arming delay and intrusion timer
- Buzzer-based alarm triggering on unauthorized entry
- Temperature/humidity monitoring (DHT sensors) with readings rotated on an LCD display
- Kitchen stopwatch/timer controlled from the dashboard and displayed on a 4-digit display
- RGB lighting control (red/green/blue/white/off) from the web dashboard
- Live camera feed integration on the dashboard
- All sensor/actuator events persisted to InfluxDB and visualized in Grafana
- MQTT message batching on each Pi to reduce network overhead
- Hardware simulators for every sensor/actuator, allowing the system to run without physical devices
- Dockerized infrastructure (MQTT broker, InfluxDB, Grafana) via `docker-compose`

## Architecture

- **Raspberry Pi nodes (`pi1`, `pi2`, `pi3`)** — each runs a set of sensor/actuator drivers (real or simulated) and communicates with the rest of the system exclusively through MQTT, publishing readings under `Sensors/#` and `Actuators/#`, and listening for commands under `Commands/<PI>/#`.
- **MQTT Broker (Eclipse Mosquitto)** — the central message bus connecting all Pi nodes and the server.
- **Server (`server/server.py`, Flask)** — subscribes to all sensor/actuator topics, writes every event to InfluxDB, and runs the core automation/security logic as an in-memory state machine (alarm state, people count, door timers, PIN buffer, stopwatch state). Exposes a REST API consumed by the web dashboard.
- **InfluxDB** — time-series storage for all sensor readings and system events (e.g. alarm state changes).
- **Grafana** — dashboards for visualizing historical sensor data from InfluxDB.
- **Web dashboard (`frontend/`)** — a simple HTML/CSS/JS interface for viewing the live camera feed, disarming the alarm, controlling RGB lighting, and setting the kitchen stopwatch.

## Technologies

**Language:** Python 3

**Messaging:** MQTT (Eclipse Mosquitto, `paho-mqtt`)

**Backend:** Flask, Flask-CORS

**Data & Visualization:** InfluxDB 2.7, Grafana

**Infrastructure:** Docker Compose

**Frontend:** HTML, CSS, JavaScript

**Hardware:** Raspberry Pi, GPIO-based sensors/actuators (DHT, PIR, ultrasonic, gyroscope/MPU6050, keypad, RGB LED, buzzer, LCD, 4-digit display)

## Project Structure

```
📦 root
 ┣ 📂 sensors       — real GPIO sensor drivers (DHT, PIR, ultrasonic, gyro/MPU6050, keypad, door sensor)
 ┣ 📂 actuators     — real GPIO actuator drivers (LCD, RGB LED, buzzer, light, 4-digit display)
 ┣ 📂 components    — wrappers that select real vs. simulated sensors/actuators based on config
 ┣ 📂 simulators    — software simulators for every sensor/actuator
 ┣ 📂 server        — Flask server: MQTT subscriber, InfluxDB writer, automation/security logic, REST API
 ┣ 📂 frontend      — web dashboard (camera feed, alarm control, RGB lighting, stopwatch)
 ┣ 📂 infrastructure
 ┃ ┣ docker-compose.yml   — Mosquitto, InfluxDB, Grafana services
 ┃ ┗ 📂 broker-config     — Mosquitto configuration
 ┣ pi1.py / pi2.py / pi3.py   — entry points for each Raspberry Pi node
 ┣ main.py           — local entry point
 ┣ settings.py / settings.json   — sensor/actuator configuration (real vs. simulated, MQTT topics)
 ┗ requirements.txt
```

## Running the Project

### Prerequisites

- Python 3
- Docker and Docker Compose
- (Optional) Raspberry Pi hardware with the corresponding sensors/actuators — the system runs fully in simulated mode without it

### Infrastructure

```bash
cd infrastructure
docker compose up -d
```

This starts the MQTT broker (Mosquitto), InfluxDB, and Grafana.

### Server

```bash
pip install -r requirements.txt
python server/server.py
```

### Raspberry Pi nodes

On each device (or locally, in simulated mode):

```bash
python pi1.py
python pi2.py
python pi3.py
```

### Frontend

Open `frontend/index.html` in a browser, or serve the `frontend/` folder with any static file server.
