import time


class Timer:

    def __init__(self):
        self.start_time = 0

    def start(self):

        self.start_time = time.perf_counter()

    def stop(self):

        return round(
            time.perf_counter() - self.start_time,
            6
        )


metrics = {}


def add_metric(name, value):

    metrics[name] = value


def get_metrics():

    return metrics


def clear_metrics():

    metrics.clear()