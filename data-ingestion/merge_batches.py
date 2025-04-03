import os
import json

input_folder = "../backend/data/fundamentals"
output_file = "../backend/data/stock_cache.json"

print(f"📂 Reading individual ticker files from: {input_folder}")

all_data = []
count = 0

for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(input_folder, filename)
        try:
            with open(file_path, "r") as f:
                stock_data = json.load(f)
                all_data.append(stock_data)
                count += 1
        except Exception as e:
            print(f"⚠️ Skipped {filename} due to error: {e}")

print(f"✅ Merged {count} ticker files, total {len(all_data)} stocks")

with open(output_file, "w") as f:
    json.dump(all_data, f, indent=2)

print(f"✅ Saved merged data to {output_file}")
