import re
import pandas as pd

# --- Configuration ---
LOG_FILE = "./logs/IS/test.log"   # path to your log file
CLEAN_LOG_FILE = "./logs/IS/cleaned_test.log"
OUTPUT_CSV = "objectives.csv"
TIME_POINTS = ['10', '100', '1000']  # seconds
MIN_OR_MAX = 'MAX'  # 'MIN' for minimization, 'MAX' for maximization

# Regex: extract best objective and time (e.g., "22331.2741 ... 100s")
pattern = re.compile(r".*?([\d\.]+)\s+[\d\.]+\s+[\d\.]+%\s+.*?(\d+)s")
# Store results
results = []
current_best = 0

with open(CLEAN_LOG_FILE, "w", encoding="utf-8", errors="ignore") as clean_f:
    with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if(line.startswith('[')):
                continue  # skip lines starting with '['
            clean_f.write(line)

with open(CLEAN_LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if(line.startswith("Read LP format model from file")):
            for key in TIME_POINTS:
                if len(results) > 0 and (key not in results[-1]):
                    results[-1][key] = current_best
            results.append({})
            current_best = float('inf') if MIN_OR_MAX == 'MIN' else float('-inf')
        
        match = pattern.search(line)
        if match:
            obj = float(match.group(1))
            t = match.group(2)            
            for key in TIME_POINTS: # 没有在这一秒记录，用上一次log的值
                if int(key)<int(t) and (key not in results[-1]):
                    results[-1][key] = current_best
            current_best = (min(current_best, obj) if MIN_OR_MAX == 'MIN' else max(current_best, obj))
            if t in TIME_POINTS:  # only keep the desired timestamps
                results[-1][t] = current_best
    for key in TIME_POINTS: # 任务时间小于时间点，用最后的值填充
        if len(results) > 0 and (key not in results[-1]):
            results[-1][key] = current_best

# Convert to DataFrame
df = pd.DataFrame(results)
df.to_csv(OUTPUT_CSV, index=False)
print("Saved ->", OUTPUT_CSV)

# Calculate means
mean_values = df.mean()
print("\nMean Objectives:")
for col, mean in mean_values.items():
    print(f"{col}: {mean}")
print(df.head())