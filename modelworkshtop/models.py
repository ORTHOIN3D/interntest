import uuid
from django.db import models
import datetime
import pytz
from rest_framework.exceptions import APIException


class Model(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=256, default="New Model")

    status = models.CharField(max_length=256, default="new")
    raw = models.FileField()


STATES = [
    ("Idle", "Idle"),
    ("Ready", "Ready"),
    ("Working", "Working"),
    ("Finished", "Finished"),
    ("Failed", "Failed"),
]


class Forbidden(APIException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    status_code = 403


class Machine(models.Model):
    state = models.CharField(max_length=256, choices=STATES, default=0)
    progress = models.IntegerField(default=0)
    error_code = models.IntegerField(default=0)

    def timefly(self):
        now = datetime.datetime.now(pytz.utc)
        duration = datetime.timedelta(seconds=10)

        # Test if there a an active job
        job_queue = self.job_set.filter(terminated=False)
        actives = job_queue.filter(active=True)

        if self.state == "Working" and actives.count() > 0:
            job = actives.first()
            if job.start_date < now - duration:
                self.progress = 100
                job.active = False
                job.terminated = True
                job.state = "Finished"
                job.save()
                self.state = "Finished"
                self.save()
            else:
                self.progress = int((now - job.start_date) / duration * 100)
                self.save()

    def execute(self, opcode):
        state = self.state
        now = datetime.datetime.now(pytz.utc)

        if opcode == "start":
            if state == "Idle":
                raise Forbidden("No available job")
            elif state == "Ready":
                job_queue = self.job_set.filter(terminated=False)
                job = job_queue.first()
                job.active = True
                job.start_date = now
                job.save()

                self.state = "Working"
            elif state == "Working":
                raise Forbidden("Wait until the end of the job")
            elif state == "Finished":
                raise Forbidden("Acknowledge the end of the previous job")
            elif state == "Failed":
                raise Forbidden("Acknowledge the last failed")

        elif opcode == "stop":
            if state == "Idle":
                pass  # NOOP
            elif state == "Ready":
                self.state = "Finished"
            elif state == "Working":
                self.state = "Finished"
            elif state == "Finished":
                raise Forbidden(
                    "Job is already finished, please acknowledge the previous job"
                )
            elif state == "Failed":
                raise Forbidden("Acknowledge the last failed")

        elif opcode == "ack":
            if state == "Idle":
                pass  # NOOP
            elif state == "Ready":
                pass  # NOOP
            elif state == "Working":
                pass  # NOOP
            elif state == "Finished":
                self.state = "Idle"
                self.progress = 0
            elif state == "Failed":
                self.state = "Idle"
                self.progress = 0

        elif opcode == "fail":
            self.state = "Failed"
            self.error_code = 1

            jobs = self.job_set.filter(active=True)
            if jobs.count() > 0:
                job = jobs.first()
                job.active = False
                job.terminated = True
                job.sate = "Failed"
                job.save()

        self.save()


class Job(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )

    model = models.ForeignKey(Model, on_delete=models.CASCADE)

    start_date = models.DateTimeField(null=True, blank=True)
    terminated = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    state = models.CharField(max_length=256, default="Pending", blank=True)

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
