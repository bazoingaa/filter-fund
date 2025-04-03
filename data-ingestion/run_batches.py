import subprocess
import time

TOTAL = 20000
BATCH_SIZE = 500
DELAY_BETWEEN_BATCHES = 10  # seconds

for offset in range(0, TOTAL, BATCH_SIZE):
    print(f"🚀 Running batch starting at offset {offset}")
    subprocess.run(["python3", "fetch_data.py", str(offset)])
    print(f"✅ Batch {offset} complete. Sleeping for {DELAY_BETWEEN_BATCHES}s\n")
    time.sleep(DELAY_BETWEEN_BATCHES)

print("🎉 All batches complete!")