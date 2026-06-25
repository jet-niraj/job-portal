"""
Script to populate sample data for testing
Run with: python manage.py shell < sample_data.py
"""

from jobs.models import Job
from datetime import datetime, timedelta

# Clear existing jobs
Job.objects.all().delete()

# Sample job data
sample_jobs = [
    {
        'job_title': 'Senior Python Developer',
        'description': 'We are looking for an experienced Python developer with 5+ years of experience in Django and REST APIs.',
        'status': 'posted',
        'category': 'full_time',
        'address': '123 Tech Street, Bandra',
        'city': 'Mumbai',
        'state': 'Maharashtra',
        'start_date': datetime.now().date(),
        'end_date': (datetime.now() + timedelta(days=180)).date(),
    },
    {
        'job_title': 'Frontend Developer (Vue.js)',
        'description': 'Seeking a creative Frontend Developer with expertise in Vue.js, Tailwind CSS, and modern JavaScript.',
        'status': 'posted',
        'category': 'full_time',
        'address': '456 Innovation Park',
        'city': 'Bangalore',
        'state': 'Karnataka',
        'start_date': datetime.now().date(),
        'end_date': (datetime.now() + timedelta(days=180)).date(),
    },
    {
        'job_title': 'Data Scientist',
        'description': 'Looking for a Data Scientist with expertise in Machine Learning, Python, and data visualization.',
        'status': 'posted',
        'category': 'full_time',
        'address': '789 Business Hub',
        'city': 'Hyderabad',
        'state': 'Telangana',
        'start_date': datetime.now().date(),
        'end_date': (datetime.now() + timedelta(days=180)).date(),
    },
    {
        'job_title': 'UI/UX Designer',
        'description': 'We need a talented UI/UX Designer to create beautiful and user-friendly interfaces.',
        'status': 'draft',
        'category': 'full_time',
        'address': '321 Design Studio',
        'city': 'Delhi',
        'state': 'Delhi',
        'start_date': datetime.now().date(),
        'end_date': (datetime.now() + timedelta(days=120)).date(),
    },
    {
        'job_title': 'DevOps Engineer',
        'description': 'Seeking a DevOps Engineer with experience in Docker, Kubernetes, AWS, and CI/CD pipelines.',
        'status': 'posted',
        'category': 'full_time',
        'address': '654 Cloud Center',
        'city': 'Pune',
        'state': 'Maharashtra',
        'start_date': datetime.now().date(),
        'end_date': (datetime.now() + timedelta(days=200)).date(),
    },
    {
        'job_title': 'React Developer - Part Time',
        'description': 'Part-time position for React developer to work on exciting projects.',
        'status': 'posted',
        'category': 'part_time',
        'address': '987 Startup Hub',
        'city': 'Mumbai',
        'state': 'Maharashtra',
        'start_date': datetime.now().date(),
        'end_date': (datetime.now() + timedelta(days=90)).date(),
    },
    {
        'job_title': 'Intern - Web Development',
        'description': 'Great opportunity for a fresher to learn web development with full stack mentorship.',
        'status': 'posted',
        'category': 'intern',
        'address': '111 Tech Academy',
        'city': 'Bangalore',
        'state': 'Karnataka',
        'start_date': datetime.now().date(),
        'end_date': (datetime.now() + timedelta(days=180)).date(),
    },
    {
        'job_title': 'QA Automation Engineer',
        'description': 'Looking for a QA Automation Engineer with expertise in Selenium, Python, and test automation frameworks.',
        'status': 'filled',
        'category': 'full_time',
        'address': '222 Quality Center',
        'city': 'Pune',
        'state': 'Maharashtra',
        'start_date': datetime.now().date(),
        'end_date': (datetime.now() + timedelta(days=150)).date(),
    },
    {
        'job_title': 'Full Stack Developer',
        'description': 'Experienced Full Stack Developer needed for building scalable web applications.',
        'status': 'requested',
        'category': 'full_time',
        'address': '333 Development Hub',
        'city': 'Bangalore',
        'state': 'Karnataka',
        'start_date': datetime.now().date(),
        'end_date': (datetime.now() + timedelta(days=200)).date(),
    },
    {
        'job_title': 'Product Manager',
        'description': 'Seeking a strategic Product Manager with experience in SaaS and agile methodologies.',
        'status': 'draft',
        'category': 'full_time',
        'address': '444 Product Office',
        'city': 'Delhi',
        'state': 'Delhi',
        'start_date': datetime.now().date(),
        'end_date': (datetime.now() + timedelta(days=180)).date(),
    },
]

# Create jobs
created_jobs = []
for job_data in sample_jobs:
    job = Job.objects.create(**job_data)
    created_jobs.append(job)
    print(f"✓ Created: {job.job_title}")

print(f"\n✅ Successfully created {len(created_jobs)} sample jobs!")
print("\nJob Summary:")
print(f"- Total Jobs: {Job.objects.count()}")
print(f"- Posted Jobs: {Job.objects.filter(status='posted').count()}")
print(f"- Draft Jobs: {Job.objects.filter(status='draft').count()}")
print(f"- Filled Jobs: {Job.objects.filter(status='filled').count()}")
print(f"- Requested Jobs: {Job.objects.filter(status='requested').count()}")