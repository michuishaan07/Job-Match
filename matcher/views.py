# matcher/views.py
from django.shortcuts import render, redirect
from .models import JobListing, Resume
from collections import Counter
from django.db.models import Count
from django.core.files.storage import FileSystemStorage
import PyPDF2



def home(request):
    return render(request, 'matcher/home.html', {'title': 'Job Match Analyzer'})

def job_summary(request):
    if not request.user.is_authenticated:
        return redirect('account_login')

    # Top 5 job roles
    jobs_by_role = JobListing.objects.values('title').annotate(count=Count('title')).order_by('-count')[:5]
    role_labels = [job['title'] for job in jobs_by_role]
    role_counts = [job['count'] for job in jobs_by_role]

    # Top 5 cities with most job postings
    jobs_by_city = JobListing.objects.values('location').annotate(count=Count('title')).order_by('-count')[:5]
    city_labels = [city['location'] for city in jobs_by_city]
    city_counts = [city['count'] for city in jobs_by_city]

    # Top 5 in-demand skills
    all_skills_raw = JobListing.objects.values_list('skills', flat=True)
    all_skills = []
    for skill_line in all_skills_raw:
        if skill_line:
            skills = [s.strip().lower() for s in skill_line.split(',')]
            all_skills.extend(skills)
    skill_counts = Counter(all_skills)
    top_skills = skill_counts.most_common(5)
    skill_labels = [skill for skill, count in top_skills]
    skill_values = [count for skill, count in top_skills]
    skill_colors = ['#0074D9', '#2ECC40', '#FF851B', '#B10DC9', '#FF4136']

    # Top 5 companies hiring
    top_companies = JobListing.objects.values('company').annotate(count=Count('id')).order_by('-count')[:5]
    company_labels = [c['company'] for c in top_companies]
    company_counts = [c['count'] for c in top_companies]
    company_colors = ['#E91E63', '#3F51B5', '#4CAF50', '#FFC107', '#9C27B0']

    print("Company labels:", company_labels)
    print("Company counts:", company_counts)

    return render(request, 'matcher/dashboard.html', {
        'role_labels': role_labels,
        'role_counts': role_counts,
        'city_labels': city_labels,
        'city_counts': city_counts,
        'colors': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],  # Consistent colors
        'skill_labels': skill_labels,
        'skill_values': skill_values,
        'skill_colors': skill_colors,
        'company_labels': company_labels,
        'company_counts': company_counts,
        'company_colors': company_colors,
    })

from django.shortcuts import render
from .models import JobListing
from .resume_parser import extract_skills_from_resume
from django.db.models import Q

def resume_upload(request):
    matched_jobs = []
    ats_score = None
    resume_skills = []
    top_skills = []
    skill_weights = {}

    if request.method == 'POST' and request.FILES.get('resume_file'):
        resume_file = request.FILES['resume_file']

        # Extract skills from resume
        resume_skills_raw = extract_skills_from_resume(resume_file)
        resume_skills = set([s.strip().lower() for s in resume_skills_raw if s.strip()])

        # Build a skill frequency dictionary from JobListing objects
        skill_counter = {}
        for job in JobListing.objects.exclude(skills__isnull=True).exclude(skills=''):
            job_skills = [s.strip().lower() for s in job.skills.split(',')]
            for skill in job_skills:
                if skill:
                    skill_counter[skill] = skill_counter.get(skill, 0) + 1

        # Extract top 20 skills dynamically
        sorted_skills = sorted(skill_counter.items(), key=lambda x: x[1], reverse=True)
        top_skills = [skill for skill, _ in sorted_skills[:20]]

        # Calculate ATS Score
        match_count = len(set(top_skills) & resume_skills)
        ats_score = (match_count / len(top_skills)) * 100 if top_skills else 0

        # Skill weights (optional)
        for skill in top_skills:
            skill_weights[skill] = 100.0 if skill in resume_skills else 0.0

        # Find matched jobs with at least 2 overlapping skills
        for job in JobListing.objects.all():
            job_skill_set = set([s.strip().lower() for s in job.skills.split(',') if s.strip()])
            if len(resume_skills & job_skill_set) >= 2:
                matched_jobs.append(job)

    return render(request, 'matcher/resume_upload.html', {
        'title': 'Upload Your Resume',
        'ats_score': ats_score,
        'resume_skills': list(resume_skills),
        'top_skills': top_skills,
        'skill_weights': skill_weights,
        'matched_jobs': matched_jobs,
    })
