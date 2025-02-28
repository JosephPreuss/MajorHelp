import random
from django.core.exceptions import ObjectDoesNotExist
from MajorHelp.models import University, Major, Course 

# exec(open("populate_majors.py").read())
# Run above method in py shell to add random majors 
# you can change names of majors to create more random entries
# doesn't add courses 

# List of universities
UNIVERSITIES = [
    "UofSC", "Clemson", "Princeton", "MIT", "Harvard",
    "Stanford", "Furman", "The Citadel"
]

# Departments
DEPARTMENTS = [
    "Natural Sciences and Mathematics",
    "Business and Economics",
    "Education",
    "Health Sciences",
    "Arts and Design",
    "Agriculture and Environmental Studies",
    "Communication and Media",
    "Law and Criminal Justice",
    "Humanities and Social Sciences"
]

# Major names (for only 5)
MAJOR_NAMES = [
    "Physics", "Environmental Science", "Kinesiology & Sports Science", "Hospitality & Tourism Management", 
    "Urban Planning & Development", "Game Design & Interactive Media", "Forensic Science", "Marine Biology", 
    "Astronomy & Astrophysics", "Public Administration & Policy", "Music Business & Industry",
    "Fashion Merchandising & Design", "Supply Chain Management", "Rehabilitation Sciences",
    "Agriculture", "Cognitive Science", "Biomedical Informatics", "Acting & Performance Studies", 
    "Nutritional Science & Dietetics"
]

# Standard college course naming format
COURSE_CODES = [
    "CS101", "CS201", "MATH150", "ENG101", "BIO110", "PHY210",
    "ECON101", "BUS200", "CHEM130", "PSY250", "HIST220", "ART105",
    "STAT300", "PHIL200", "SOC101", "POLS150", "MKTG230", "FIN310"
]

# Retrieve existing universities
universities = {}
for name in UNIVERSITIES:
    try:
        university = University.objects.get(name=name)
        universities[name] = university
    except ObjectDoesNotExist:
        print(f"University '{name}' not found in the database. Skipping.")

# Retrieve available courses
courses = list(Course.objects.all())

# If no universities exist, exit
if not universities:
    print("No universities found. Add universities before running this script.")
    exit()

# Check the number of majors before adding new ones
existing_majors = Major.objects.count()
print(f"\nExisting majors in database: {existing_majors}")

# Add 5 majors
print("\nAdding 5 new majors with courses...\n")

added_count = 0
for i in range(3):
    university_name = random.choice(list(universities.keys()))
    university = universities[university_name]

    major_name = random.choice(MAJOR_NAMES)
    department = random.choice(DEPARTMENTS)

    print(f"Adding: {major_name} in {department} at {university.name}")

    major = Major(
        university=university,
        major_name=major_name,
        major_description=f"A study in {major_name}.",
        department=department,
        in_state_min_tuition=random.randint(15000, 20000),
        in_state_max_tuition=random.randint(21000, 40000),
        out_of_state_min_tuition=random.randint(25000, 50000),
        out_of_state_max_tuition=random.randint(51000, 90000),
        fees=random.randint(500, 5000),
        grad_in_state_min_tuition=random.randint(0, 50000),
        grad_in_state_max_tuition=random.randint(0, 70000),
        grad_out_of_state_min_tuition=random.randint(0, 80000),
        grad_out_of_state_max_tuition=random.randint(0, 100000),
    )

    try:
        major.save()
        added_count += 1

        # Assign 3 random courses to each major
        assigned_courses = random.sample(courses, min(3, len(courses)))  # Select up to 3
        major.courses.set(assigned_courses)  # Assign courses to major

        print(f" -> Assigned Courses: {[course.course_code for course in assigned_courses]}")

    except Exception as e:
        print(f"Error saving major {major_name}: {e}")

# Check the number of majors after inserting
new_major_count = Major.objects.count()
print(f"\nMajors before: {existing_majors}, Majors after: {new_major_count}")
print(f"Successfully added {added_count} new majors with courses.\n")
