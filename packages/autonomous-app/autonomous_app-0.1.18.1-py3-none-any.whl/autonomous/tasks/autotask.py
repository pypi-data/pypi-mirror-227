import redis
from rq import Queue
import os


class AutoTasks:
    _connection = None
    queue = None

    def __init__(self, connection_string="redis://redis:6379"):
        if not AutoTasks._connection:
            AutoTasks._connection = redis.from_url(os.environ.get("RQ_DEFAULT_CONNECTION", connection_string))
            AutoTasks.queue = Queue(connection=self._connection)

    def task(self, job, *args, **kwargs):
        task = self.queue.enqueue(job, *args, **kwargs)
        return task.id

    # get job given its id
    def get_task(self, job_id):
        try:
            return self.queue.fetch_job(job_id)
        except Exception as e:
            return f"invalid:\t{e}"

    # get job given its id
    def get_status(self, job_id):
        try:
            return self.queue.fetch_job(job_id).get_status()
        except Exception as e:
            return f"invalid:\t{e}"

    # get job given its id
    def get_result(self, job_id):
        try:
            return self.queue.fetch_job(job_id).result
        except Exception as e:
            return f"invalid:\t{e}"

    # get all jobs
    def get_all(self):
        # init all_jobs list
        all_jobs = list(
            set(
                [
                    self.queue.started_job_registry.get_job_ids(),
                    self.queue.job_ids.get_job_ids(),  # queued job ids
                    self.queue.failed_job_registry.get_job_ids(),
                    self.queue.deferred_job_registry.get_job_ids(),
                    self.queue.finished_job_registry.get_job_ids(),
                    self.queue.scheduled_job_registry.get_job_ids(),
                ]
            )
        )
        # iterate over job ids list and fetch jobs
        for job_id in all_jobs:
            all_jobs.append(self.get_task(job_id))
        return all_jobs
