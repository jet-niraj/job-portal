from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job
from .serializers import JobSerializer, JobListSerializer, JobAnalyticsSerializer


class JobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Job objects with full CRUD operations.
    Includes custom actions for analytics, statistics, filters, and duplicate.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'city', 'state']
    search_fields = ['job_title', 'description', 'city', 'state']
    ordering_fields = ['created_at', 'job_title', 'status']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return JobListSerializer
        return JobSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Job deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """
        Duplicate an existing job.
        Note: job_profile_picture is NOT copied — image files can't be
        duplicated reliably from a URL reference. The duplicate will have no image.
        """
        try:
            job = self.get_object()

            new_job = Job(
                job_title=job.job_title,
                description=job.description,
                status=job.status,
                category=job.category,
                address=job.address,
                city=job.city,
                state=job.state,
                start_date=job.start_date,
                end_date=job.end_date,
            )
            new_job.save()

            serializer = self.get_serializer(new_job)
            return Response(
                {'message': 'Job duplicated successfully', 'job': serializer.data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """
        Analytics dashboard data: distribution by status, city, state, category.
        """
        try:
            jobs = self.get_queryset()

            # Status distribution
            status_data = jobs.values('status').annotate(count=Count('id'))
            status_display = {
                dict(Job.STATUS_CHOICES).get(item['status'], item['status']): item['count']
                for item in status_data
            }

            # City distribution
            city_distribution = {
                item['city']: item['count']
                for item in jobs.values('city').annotate(count=Count('id'))
                if item['city']
            }

            # State distribution
            state_distribution = {
                item['state']: item['count']
                for item in jobs.values('state').annotate(count=Count('id'))
                if item['state']
            }

            # Category distribution
            jobs_by_category = {
                dict(Job.CATEGORY_CHOICES).get(item['category'], item['category']): item['count']
                for item in jobs.values('category').annotate(count=Count('id'))
            }

            analytics_data = {
                'status_distribution': status_display,
                'city_distribution': city_distribution,
                'state_distribution': state_distribution,
                'jobs_by_category': jobs_by_category,
                'total_jobs': jobs.count(),
            }

            serializer = JobAnalyticsSerializer(analytics_data)
            return Response(serializer.data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Quick job counts by status and location."""
        jobs = self.get_queryset()
        return Response({
            'total_jobs': jobs.count(),
            'draft_jobs': jobs.filter(status='draft').count(),
            'posted_jobs': jobs.filter(status='posted').count(),
            'filled_jobs': jobs.filter(status='filled').count(),
            'unique_cities': jobs.values('city').distinct().count(),
            'unique_states': jobs.values('state').distinct().count(),
        })

    @action(detail=False, methods=['get'])
    def filters(self, request):
        """Available filter options for frontend dropdowns."""
        return Response({
            'statuses': [{'value': k, 'label': v} for k, v in Job.STATUS_CHOICES],
            'categories': [{'value': k, 'label': v} for k, v in Job.CATEGORY_CHOICES],
            'cities': list(Job.objects.values_list('city', flat=True).distinct()),
            'states': list(Job.objects.values_list('state', flat=True).distinct()),
        })