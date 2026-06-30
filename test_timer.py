import time

from evaluation.metrics import Timer

timer = Timer()

timer.start()

time.sleep(2)

print(timer.stop())