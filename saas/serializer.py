from rest_framework import serializers
from rest_framework.serializers import  ModelSerializer
from saas.models import *

class ProjectModelSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'






class ModuleModelSerializer(ModelSerializer):
    # project= ProjectModelSerializer()
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    # project = serializers.StringRelatedField()
    class Meta:
        model = Module
        fields = '__all__'

    # def create(self, validated_data):

class RelationshipModelSerializer(ModelSerializer):
    basecase = serializers.PrimaryKeyRelatedField(queryset=casenew.objects.all())
    relatedcase = serializers.PrimaryKeyRelatedField(queryset=casenew.objects.all(),allow_null=True,required=False)

    class Meta:
        model = relationship
        fields = '__all__'
        # exclude=['basecase']
        # depth=1


class CaseModelSerializer(ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(),allow_null=True)
    module = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all(),allow_null=True)
    result_log=serializers.CharField(label='请求结果',max_length=2000,required=False,read_only=True)
    related=RelationshipModelSerializer(source='basec',many=True,required=False)

    # method_response = serializers.SerializerMethodField()


    class Meta:
        model = casenew
        fields = '__all__'

    # def get_method_response(self, obj):
    #     return obj.get_method_display()


class fileModelSerializer(ModelSerializer):
    filepath = serializers.SerializerMethodField()
    class Meta:
        model = filetest
        fields = '__all__'

    def get_filepath(self, obj):
        return  str(obj.file)
