#pip install fastapi uvicorn paho-mqtt requests

# python run_stack.py
import os, sys, subprocess, signal

CMD_TOPIC  = os.getenv("CMD_TOPIC", "huber/robot/plan/cmd")
GOAL_TOPIC = os.getenv("GOAL_TOPIC", "huber/robot/goal")
MQTT_HOST = os.getenv("MQTT_HOST", "test.mosquitto.org")
MQTT_PORT = os.getenv("MQTT_PORT", "8081")          # 8081 = WSS en test.mosquitto
MQTT_TRANSPORT = os.getenv("MQTT_TRANSPORT", "websockets")
MQTT_TLS = os.getenv("MQTT_TLS", "1")               # 1 = usar TLS (wss)
MQTT_WS_PATH = os.getenv("MQTT_WS_PATH", "/mqtt")
MQTT_KEEPALIVE= os.getenv("MQTT_KEEPALIVE","60")  # prueba 60; si sigue, "120" o "0"



def main():
    py = sys.executable

    env = os.environ.copy()
    env.update({
        "MQTT_HOST": MQTT_HOST,
        "MQTT_PORT": str(MQTT_PORT),
        "MQTT_TRANSPORT": MQTT_TRANSPORT,
        "MQTT_TLS": MQTT_TLS,
        "MQTT_WS_PATH": MQTT_WS_PATH,
        "CMD_TOPIC": CMD_TOPIC,
        "GOAL_TOPIC": GOAL_TOPIC,
        "MQTT_KEEPALIVE": MQTT_KEEPALIVE,   # prueba 60; si sigue, "120" o "0"
    })

    env["PYTHONUNBUFFERED"] = "1"

    planner = subprocess.Popen([
        py, "planner_mqtt.py",
        "--host", MQTT_HOST,
        "--port", str(MQTT_PORT),
        "--cmd_topic", CMD_TOPIC,
        "--goal_topic", GOAL_TOPIC,
        "--dt", "0.1"
    ], env=env)

    web = subprocess.Popen([
        py, "-m", "uvicorn",
        "api_server:app",
        "--host", "0.0.0.0",
        "--port", "8000"
    ], env=env)

    try:
        web.wait()
    except KeyboardInterrupt:
        pass
    finally:
        for p in (web, planner):
            try:
                p.send_signal(signal.SIGINT)
            except Exception:
                pass

if __name__ == "__main__":
    main()
