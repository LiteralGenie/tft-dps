import multiprocessing as mp


def run_job_worker(job_queue: mp.Queue, result_queue: mp.Queue):
    while True:
        job = job_queue.get()
        resp = ...
        result_queue.put(
            dict(
                **job,
                resp=resp,
            )
        )
