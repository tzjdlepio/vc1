import time
import psutil
import statistics
import json
import os
import sys

# 將專案路徑加入 PYTHONPATH 以利匯入 asgards
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def measure_performance(func, iterations=5):
    cpu_usages = []
    memory_usages = []
    response_times = []

    process = psutil.Process(os.getpid())

    for i in range(iterations):
        # 紀錄開始前狀態
        start_time = time.time()
        
        # 執行目標函式
        func()
        
        # 紀錄結束後狀態
        duration = time.time() - start_time
        cpu_pct = psutil.cpu_percent(interval=None)
        mem_info = process.memory_info().rss / (1024 * 1024) # MB

        response_times.append(duration)
        cpu_usages.append(cpu_pct)
        memory_usages.append(mem_info)

    results = {
        "cpu_performance": {
            "avg_percent": round(statistics.mean(cpu_usages), 2),
            "max_percent": max(cpu_usages)
        },
        "memory_performance": {
            "avg_mb": round(statistics.mean(memory_usages), 2),
            "max_mb": max(memory_usages)
        },
        "response_time": {
            "avg_seconds": round(statistics.mean(response_times), 4),
            "total_seconds": round(sum(response_times), 4)
        }
    }
    return results

def dummy_workload():
    # 這裡可以替換成 asgards 中的真實邏輯
    # 例如：from asgards.snake_game.engine import GameEngine
    temp_list = [x**2 for x in range(100000)]
    time.sleep(0.05)

if __name__ == "__main__":
    print("Running benchmarks...")
    perf_results = measure_performance(dummy_workload, iterations=5)
    
    with open("performance_report.json", "w") as f:
        json.dump(perf_results, f, indent=4)
    
    print(f"Benchmark finished. Avg Response Time: {perf_results['response_time']['avg_seconds']}s")
