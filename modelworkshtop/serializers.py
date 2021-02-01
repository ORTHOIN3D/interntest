from rest_framework import serializers
from . import models


class Model(serializers.ModelSerializer):
    class Meta:
        model = models.Model
        fields = ("id", "name", "status", "raw", "output")


class Job(serializers.ModelSerializer):
    class Meta:
        model = models.Job
        fields = ("id", "model", "start_date", "terminated", "active", "state")
        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):
        machine, _ = models.Machine.objects.get_or_create(pk=0)
        if machine.state == "Idle":
            machine.state = "Ready"
            machine.save()

        return models.Job.objects.create(machine=machine, **validated_data)


class StateMachine(serializers.ModelSerializer):
    class Meta:
        model = models.Machine
        fields = ("state", "error_code", "progress")


class StateCmd(serializers.Serializer):
    cmd = serializers.ChoiceField(
        [
            ("start", "start"),
            ("stop", "stop"),
            ("ack", "ack"),
            ("fail", "fail"),
        ]
    )
