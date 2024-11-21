from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from .models import SpyCat, Target, Mission
from .serializers import SpyCatSerializer, TargetSerializer, MissionSerializer


class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer

    @action(detail=True, methods=["put"])
    def update_salary(self, request, pk=None):
        cat = self.get_object()
        salary = request.data.get("salary")
        if not isinstance(salary, (int, float)):
            raise ValidationError("Salary must be a number.")
        cat.salary = salary
        cat.save()
        return Response({"status": "salary updated"})


class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def create(self, request, *args, **kwargs):
        mission_data = request.data
        cat_id = mission_data.get("cat")
        targets_data = mission_data.get("targets")

        # Handle creating targets
        targets = [Target.objects.create(**target) for target in targets_data]

        # Create mission
        mission = Mission.objects.create(
            cat_id=cat_id, complete=mission_data.get("complete", False)
        )
        mission.targets.set(targets)
        mission.save()
        return Response(self.get_serializer(mission).data)

    @action(detail=True, methods=["put"])
    def update_target(self, request, pk=None):
        mission = self.get_object()
        target_id = request.data.get("target_id")
        target = mission.targets.get(id=target_id)

        # Validate if mission or target is completed
        if mission.complete or target.complete:
            raise ValidationError(
                "Cannot update target because the mission or target is completed."
            )

        target.notes = request.data.get("notes", target.notes)
        target.complete = request.data.get("complete", target.complete)
        target.save()
        return Response({"status": "target updated"})

    @action(detail=True, methods=["post"])
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        cat_id = request.data.get("cat_id")

        # Validate if mission is already assigned to a cat
        if mission.cat:
            raise ValidationError("Mission already assigned to a cat.")

        mission.cat_id = cat_id
        mission.save()
        return Response({"status": "cat assigned to mission"})

    def perform_destroy(self, instance):
        # Ensure mission is not deleted if it has an assigned cat
        if instance.cat:
            raise ValidationError(
                "Cannot delete mission because it's assigned to a cat."
            )
        instance.delete()
