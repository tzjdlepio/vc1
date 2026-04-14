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
            "token_usage": {"input": 0, "output": 0, "total": 0},
            "duration_seconds": 0
        }

    def log_tokens(self, input_tokens, output_tokens):
        """記錄使用的 token 數"""
        self.data["token_usage"]["input"] = input_tokens
        self.data["token_usage"]["output"] = output_tokens
        self.data["token_usage"]["total"] = input_tokens + output_tokens

    def save(self, filename="execution_metrics.json"):
        end_ts = time.time()
        self.data["end_time"] = datetime.now().isoformat()
        self.data["duration_seconds"] = round(end_ts - self.data["start_ts"], 4)
        
        # 複製一份資料來存檔，移除暫存的 timestamp
        temp_data = self.data.copy()
        if "start_ts" in temp_data:
            del temp_data["start_ts"]

        # 讀取現有的 JSON 並附加新紀錄
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    current_data = json.load(f)
                    if not isinstance(current_data, list):
                        current_data = []
            else:
                current_data = []
        except:
            current_data = []

        current_data.append(temp_data)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, indent=4, ensure_ascii=False)
