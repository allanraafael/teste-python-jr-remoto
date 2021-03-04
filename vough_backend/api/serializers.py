from rest_framework import serializers

from . import models


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializador dos campos das organizações"""

    class Meta:
        model = models.Organization
        fields = "__all__"
