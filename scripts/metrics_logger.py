import json
import time
from datetime import datetime
import os

class MetricsLogger:
    def __init__(self, step_name):
        self.data = {
            "step_name": step_name,
            "start_time": datetime.now().isoformat(),
            "start_ts": time.time()
        }

    def save(self, filename="execution_metrics.json"):
        end_ts = time.time()
        self.data["end_time"] = datetime.now().isoformat()
        self.data["duration_seconds"] = round(end_ts - self.data["start_ts"], 2)
        
        # 移除暫存的 timestamp
        if "start_ts" in self.data:
            del self.data["start_ts"]

        # 讀取並更新 JSON
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    current_data = json.load(f)
                    if not isinstance(current_data, list):
                        current_data = []
            else:
                current_data = []
        except (FileNotFoundError, json.JSONDecodeError):
            current_data = []

        current_data.append(self.data)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, indent=4, ensure_ascii=False)
        
        # 同時產生 Markdown 摘要給 ADO
        self.generate_markdown_summary(current_data)

    def generate_markdown_summary(self, all_data, summary_file="execution_summary.md"):
        """產生供 ADO 顯示的 Markdown 表格"""
        lines = [
            "# 🚀 Pipeline 執行數據摘要 (Execution Metrics)",
            "",
            "| 步驟名稱 (Step) | 開始時間 (Start) | 持續時間 (Duration s) |",
            "| :--- | :--- | :--- |"
        ]
        for item in all_data:
            lines.append(f"| {item['step_name']} | {item['start_time']} | {item['duration_seconds']}s |")
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        
        # 輸出 ADO 指令，讓摘要顯示在 Build Summary 頁面
        # 注意：這行也可以在 Pipeline YAML 中執行，效果相同
        print(f"##vso[task.uploadsummary]{os.path.abspath(summary_file)}")

if __name__ == "__main__":
    # 範例初始化
    logger = MetricsLogger("pipeline_start")
    logger.save()
