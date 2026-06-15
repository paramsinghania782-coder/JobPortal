import os
import django
import random
from faker import Faker

# Yahan JOBPORTAL tumhare main project folder ka naam hai
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_portal.settings')
django.setup()

from jobs.models import Job
from django.contrib.auth.models import User

def populate(N=200):
    fake = Faker()

    print("Checking for recruiter user...")
    # Job create karne ke liye ek user chahiye, toh hum ek dummy user dhundhenge ya banayenge
    recruiter_user, created = User.objects.get_or_create(
        username='dummy_recruiter',
        defaults={
            'email': 'recruiter@jobhub.com',
            'first_name': 'Dummy',
            'last_name': 'Recruiter'
        }
    )
    
    # Agar naya user create hua hai, toh uska password set kar dete hain
    if created:
        recruiter_user.set_password('jobhub123')
        recruiter_user.save()
        print("Naya dummy recruiter ban gaya hai (Username: dummy_recruiter, Password: jobhub123)")
    else:
        print("Pehle se maujud 'dummy_recruiter' ka use kar rahe hain.")

    print("Fake Jobs add karna shuru kar rahe hain...")
    
    for _ in range(N):
        fake_title = fake.job()
        fake_company = fake.company()
        fake_location = fake.city()
        fake_description = fake.text(max_nb_chars=200)
        
        # Salary tumhara CharField hai, isliye isko string me daal rahe hain
        fake_salary = f"₹{random.randint(15000, 80000)}/month"

        # Database me Job save karna
        Job.objects.create(
            recruiter=recruiter_user,  # Ye foreign key field dena zaroori tha
            title=fake_title,
            company=fake_company,
            location=fake_location,
            description=fake_description,
            salary=fake_salary
        )
        
    print(f"Successfully {N} fake jobs add ho gayi hain!")

if __name__ == '__main__':
    # 20 jobs add karne ke liye. Tum chaho toh ise badha kar 50 ya 100 bhi kar sakte ho.
    populate(200)