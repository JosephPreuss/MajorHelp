import random
from django.core.exceptions import ObjectDoesNotExist
from MajorHelp.models import University, Major, Course 

# exec(open("populate_majors.py").read())
# Run above method in py shell to add random majors 
# you can change names of majors to create more random entries
# doesn't add courses 

# List of universities
UNIVERSITIES = [
    "UofSC", "Clemson", "Princeton", "MIT", "Harvard", "Stanford", "Furman",
    "The Citadel", "Yale", "Duke", "University of Pennsylvania", "Notre Dame",
    "Vanderbilt", "University of North Carolina", "New York University",
    "Coastal Carolina", "Ohio State", "Auburn", "University of Florida",
    "University of Georgia", "Virginia Tech", "College of Charleston",
    "University of Southern California", "University of Texas - Austin",
    "Gonzaga University" 
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
    "Humanities and Social Sciences",
    "Engineering and Technology"
]

# Major names (for only 5)
MAJOR_NAMES = [
    # Natural Sciences and Mathematics
    "Climate Science & Atmospheric Studies", "Computational Biology & Bioinformatics",
    "Mathematical Physics",

    # Business and Economics
    "Accounting Analytics & Audit Systems", "Nonprofit Management & Philanthropy", 
    "Global Markets & Investment Strategy",

    # Education
    "Adult & Continuing Education", "Instructional Design & Learning Sciences", 
    "Education Policy & Leadership",

    # Health Sciences
    "Occupational Therapy & Rehabilitation", "Clinical Laboratory Science", 
    "Health Communication & Promotion",

    # Arts and Design
    "Animation & Visual Effects", "Digital Art & Experimental Media", 

    # Agriculture and Environmental Studies
    "Wildlife & Fisheries Management", "Agricultural Business & Economics", 
    "Climate-Resilient Agriculture",

    # Communication and Media
    "Media Production & Editing", "Advertising & Integrated Marketing", 
    "Political Communication & Campaign Strategy",

    # Law and Criminal Justice
    "Cybercrime & Digital Forensics", "Corrections Administration & Policy", 
    "International Criminal Law",

    # Humanities and Social Sciences
    "Religious Studies & Theology", "Cultural Anthropology & Global Studies", 
    "Ethics & Moral Philosophy",

    # Engineering and Technology
    "Embedded Systems & IoT Engineering", "Civil Infrastructure & Construction Management", 
    "Aerospace Propulsion Systems"
]

# Standard college course naming format
COURSE_CODES = [
    "CS101", "CS201", "MATH150", "ENG101", "BIO110", "PHY210",
    "ECON101", "BUS200", "CHEM130", "PSY250", "HIST220", "ART105",
    "STAT300", "PHIL200", "SOC101", "POLS150", "MKTG230", "FIN310"
    "CS102", "CS301", "MATH250", "MATH320", "ENG201", "ENG260",
    "BIO210", "BIO315", "PHY120", "PHY340", "CHEM220", "CHEM310",
    "ECON201", "ECON305", "BUS210", "BUS330", "PSY101", "PSY310",
    "HIST101", "HIST330", "ART210", "ART330", "STAT200", "STAT420",
    "PHIL101", "PHIL310", "SOC201", "SOC330", "POLS220", "POLS310",
    "MKTG120", "MKTG350", "FIN101", "FIN420", "COMM101", "COMM250",
    "LING101", "LING215", "EDUC101", "EDUC310", "ENV110", "ENV305",
    "ASTR101", "ASTR220", "MUSC101"
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
