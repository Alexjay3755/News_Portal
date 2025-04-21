from .models import *
from rest_framework import serializers


class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'url']


class SClassSerializer(serializers.HyperlinkedModelSerializer):
    school = SchoolSerializer(read_only=True)
    school_id = serializers.PrimaryKeyRelatedField(
        queryset=School.objects.all(),
        write_only=True
    )

    class Meta:
        model = SClass
        fields = ['id', 'grade', 'url', 'school', 'school_id',]

    def create(self, validated_data):
        school = validated_data.pop('school_id')
        sclass = SClass.objects.create(school=school,**validated_data)
        return sclass


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    sclass = SClassSerializer(read_only=True)
    class_id = serializers.PrimaryKeyRelatedField(
        queryset=SClass.objects.all(),
        write_only=True
    )

    class Meta:
        model = Student
        fields = ['id', 'name', 'url', 'sclass', 'class_id']

    def create(self, validated_data):
        sclass = validated_data.pop('class_id')
        sclass = Student.objects.create(sclass=sclass,**validated_data)
        return sclass