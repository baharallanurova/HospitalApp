from rest_framework import serializers

from hospital.models import Hospital_Information


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital_Information
        fields = '__all__'
