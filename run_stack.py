#pip install fastapi uvicorn paho-mqtt requests

# run_stack.py
import os, sys, subprocess, signal

CMD_TOPIC  = os.getenv("CMD_TOPIC", "huber/robot/plan/cmd")
GOAL_TOPIC = os.getenv("GOAL_TOPIC", "huber/robot/goal")

def main():
    py = sys.executable

    planner = subprocess.Popen([
        py, "planner_mqtt.py",
        "--cmd_topic", CMD_TOPIC,
        "--goal_topic", GOAL_TOPIC,
        "--dt", "0.1"
    ])

    web = subprocess.Popen([
        py, "-m", "uvicorn",
        "api_server:app",
        "--host", "0.0.0.0",
        "--port", "8000"
    ])

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
