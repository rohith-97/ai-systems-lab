import time
import os
import concurrent.futures
from typing import List
from tqdm import tqdm

def task(task_id: int):
    time.sleep(0.1)
    if task_id == 500:
        raise ValueError(f"Task {task_id} encountered an error")
    return f"Task {task_id} completed"

def main():
    start = time.time()
    results = []
    errors = []
    max_workers=min(200, (os.cpu_count() or 1) * 2)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(task, i): i for i in range(1000)}
        for future in tqdm(concurrent.futures.as_completed(futures), total=1000, colour="blue"):
            task_id = futures[future]
            try:
                result = future.result()
                results.append(result)
            
            except Exception as e:
                errors.append(str(e))
                tqdm.write(f"Error in task {task_id}: {e}")
            

    end = time.time()
    print(f"\n✅ Completed: {len(results)}")
    print(f"❌ Failed: {len(errors)}")
    print(f"Total time: {end - start:.2f} seconds")
if __name__ == "__main__":
    main()
