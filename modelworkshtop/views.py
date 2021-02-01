from rest_framework import viewsets

from . import serializers
from . import models
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.exceptions import APIException


class ModelViewSet(viewsets.ModelViewSet):
    queryset = models.Model.objects.all()
    serializer_class = serializers.Model


class JobViewSet(viewsets.ModelViewSet):
    queryset = models.Job.objects.all()
    serializer_class = serializers.Job


def fly():
    machine, _ = models.Machine.objects.get_or_create(pk=0)
    machine.timefly()
    return machine


class Machine(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.StateCmd

    def list(self, request):
        machine = fly()

        out = serializers.StateMachine(machine)

        return Response(out.data)

    def create(self, request):

        serializer = serializers.StateCmd(data=request.data)
        if not serializer.is_valid():
            raise APIException("Bad cmd")

        cmd = serializer.validated_data["cmd"]

        machine = fly()
        machine.execute(cmd)

        serializer = serializers.StateMachine(machine)

        return Response(serializer.data)
