from rest_framework import serializers
from .models import Job
from datetime import datetime


class JobSerializer(serializers.ModelSerializer):
    """
    Main serializer for Job model with validation
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Job
        fields = [
            'id',
            'job_title',
            'description',
            'status',
            'status_display',
            'category',
            'category_display',
            'address',
            'city',
            'state',
            'start_date',
            'end_date',
            'job_profile_picture',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_end_date(self, value):
        """
        Validate that end_date is not before start_date.
        start_date comes as a string from initial_data, so we parse it.
        """
        start_date_raw = self.initial_data.get('start_date')

        if value and start_date_raw:
            if isinstance(start_date_raw, str):
                try:
                    start_date = datetime.strptime(start_date_raw, "%Y-%m-%d").date()
                except ValueError:
                    raise serializers.ValidationError("Invalid start_date format. Use YYYY-MM-DD.")
            else:
                start_date = start_date_raw 

            if value < start_date:
                raise serializers.ValidationError("End date cannot be before start date.")

        return value

    def validate_job_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Job title cannot be empty.")
        return value

    def validate_description(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Description cannot be empty.")
        return value

    def validate(self, data):
        if 'end_date' in data and 'start_date' in data:
            if data['end_date'] and data['end_date'] < data['start_date']:
                raise serializers.ValidationError({
                    'end_date': 'End date cannot be before start date.'
                })
        return data


class JobListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for list view
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Job
        fields = [
            'id',
            'job_title',
            'description',
            'status',
            'status_display',
            'category',
            'category_display',
            'address',
            'city',
            'state',
            'start_date',
            'end_date',
            'job_profile_picture',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class JobAnalyticsSerializer(serializers.Serializer):
    """
    Serializer for analytics data
    """
    status_distribution = serializers.DictField()
    city_distribution = serializers.DictField()
    state_distribution = serializers.DictField()
    total_jobs = serializers.IntegerField()
    jobs_by_category = serializers.DictField()