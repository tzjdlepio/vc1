import time
import psutil
import os
import json
import statistics

def run_benchmark(cmd, iterations=3):
    """執行多次並取平均值 (CPU, Memory, Response Time)"""
    cpu_usages = []
    mem_usages = []
    durations = []

    print(f"Starting benchmark for: {cmd} ({iterations} iterations)")

    for i in range(iterations):
        start_time = time.time()
        process = psutil.Popen(cmd, shell=True)
        
        cpu_percents = []
        mem_rss = []
        
        while process.poll() is None:
            try:
                p = psutil.Process(process.pid)
                cpu_percents.append(p.cpu_percent(interval=0.1))
                mem_rss.append(p.memory_info().rss / (1024 * 1024)) # MB
            except:
                break
        
        duration = time.time() - start_time
        durations.append(duration)
        if cpu_percents: cpu_usages.append(statistics.mean(cpu_percents))
        if mem_rss: mem_usages.append(statistics.mean(mem_rss))
        
        print(f"  Iteration {i+1}: {round(duration, 2)}s")

    report = {
        "command": cmd,
        "avg_response_time_sec": round(statistics.mean(durations), 4),
        "avg_cpu_percent": round(statistics.mean(cpu_usages), 2) if cpu_usages else 0,
        "avg_memory_mb": round(statistics.mean(mem_usages), 2) if mem_usages else 0,
        "iterations": iterations
    }
    
    with open("performance_report.json", "w") as f:
        json.dump(report, f, indent=4)
    
    return report

if __name__ == "__main__":
    # 範例：測試執行 hello.py 或其他主要進入點
    run_benchmark("python asgards/hello.py", iterations=3)
