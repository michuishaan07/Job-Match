from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import django
import os

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "job_matcher.settings")
django.setup()

from matcher.models import JobListing

# Selenium driver setup
service = Service('/usr/local/bin/chromedriver')  # Adjust path if needed
driver = webdriver.Chrome(service=service)

base_url = "https://www.naukri.com/data-science-jobs"
params = "?k=data%20science&nignbevent_src=jobsearchDeskGNB"

for page in range(1, 3):  # Pages 1 to 5
    print(f"\n--- Scraping Page {page} ---")
    
    url = f"{base_url}-{page}{params}" if page > 1 else f"{base_url}{params}"
    driver.get(url)
    time.sleep(5)

    jobs = driver.find_elements(By.CLASS_NAME, 'srp-jobtuple-wrapper')
    print("Jobs found:", len(jobs))

    for job in jobs:
        try:
            title = job.find_element(By.CLASS_NAME, 'title').text
            company = job.find_element(By.CLASS_NAME, 'comp-name').text
            location = job.find_element(By.CLASS_NAME, 'locWdth').text

            try:
                job_url = job.find_element(By.CSS_SELECTOR, 'a.title').get_attribute('href')
            except:
                job_url = 'N/A'

            try:
                skills_list = job.find_elements(By.CSS_SELECTOR, "ul.tags-gt > li")
                skills = ", ".join([skill.text.strip() for skill in skills_list if skill.text.strip()])
            except:
                skills = 'N/A'

            try:
                salary = job.find_element(By.CSS_SELECTOR, '.sal-wrap span[title]').text
            except:
                salary = 'N/A'

            JobListing.objects.create(
                title=title,
                company=company,
                location=location,
                skills=skills,
                salary=salary,
                url=job_url
            )
            print(f"Saved: {title}")
        
        except Exception as e:
            print("Error:", e)

driver.quit()
