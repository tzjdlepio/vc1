import json
import time
from datetime import datetime
import os

class MetricsLogger:
    def __init__(self, step_name):
        self.data = {
            "step_name": step_name,
            "start_time": datetime.now().isoformat(),
            "start_ts": time.time(),
            "token_input": 0,
            "token_output": 0,
            "token_total": 0
        }

    def log_tokens(self, input_tokens=0, output_tokens=0):
        self.data["token_input"] = input_tokens
        self.data["token_output"] = output_tokens
        self.data["token_total"] = input_tokens + output_tokens

    def save(self, filename="execution_metrics.json"):
        end_ts = time.time()
        self.data["end_time"] = datetime.now().isoformat()
        self.data["duration_seconds"] = round(end_ts - self.data["start_ts"], 4)
        del self.data["start_ts"]

        # 讀取舊資料並附加
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    current_data = json.load(f)
                    if not isinstance(current_data, list):
                        current_data = []
            else:
                current_data = []
        except (FileNotFoundError, json.JSONDecodeError):
            current_data = []

        current_data.append(self.data)
        with open(filename, 'w') as f:
            json.dump(current_data, f, indent=4)

if __name__ == "__main__":
    # 範例初始化
    logger = MetricsLogger("pipeline_start")
    logger.save()
