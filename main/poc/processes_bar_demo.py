"""
測試於 powerbarcoder.sh

python3 "${workingDirectory}poc/processes_bar_demo.py" "$1"
"""

import time
from tqdm import tqdm

list = range(10)
initial_desc = "Processing 0"
with tqdm(total=len(list),
          position=1,  # 用於製造換行
          leave=False,  # 避免最後一行多一個重複的 100% 進度條
          desc=initial_desc  # 避免第一行多出且刪不掉的 0% 進度條長太醜
          ) as pbar:
    for i in list:
        time.sleep(0.1)
        pbar.set_description(f"Processing {i}")
        pbar.update(1)
