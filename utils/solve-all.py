import os
import subprocess
import sys
import time

paths = []
for path, dirs, files in os.walk('puzzles'):
    for file in files:
        paths.append(os.path.join(path, file))

for path in paths:
    for method in ['human', 'hybrid']:
        start = time.time()
        try:
            output = subprocess.check_output(['python3', 'takuzu.py', '--method', method, path], stderr = subprocess.STDOUT, timeout = 60)
        except subprocess.TimeoutExpired:
            output = False
        end = time.time()

        print('{file}\t{method}\t{time}'.format(
            file = '\t'.join(path.rsplit('.', 1)[0].split('/')[1:]),
            method = method,
            time = '{:.02f}'.format(end - start) if output else 'false',
        ))
        sys.stdout.flush()
