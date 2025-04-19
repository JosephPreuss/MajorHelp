import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pestopanini.settings')
django.setup()

from MajorHelp.models import University, Major
from django.utils.text import slugify
import csv

# Path to your CSV file
CSV_PATH = "Top_50_Majors_per_Department.csv"

print("Deleting all existing majors...")
Major.objects.all().delete()

def run():
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        universities = University.objects.all()

        major_objects = []

        for row in reader:
            major_name = row['major_name'].strip()
            major_description = row['major_description'].strip()
            department = row['department'].strip()

            # Raw CSV values
            in_state_min = int(float(row.get('in_state_min_tuition', 0) or 0))
            in_state_max = int(float(row.get('in_state_max_tuition', 0) or 0))
            out_state_min = int(float(row.get('out_of_state_min_tuition', 0) or 0))
            out_state_max = int(float(row.get('out_of_state_max_tuition', 0) or 0))
            fees = int(float(row.get('fees', 0) or 0))

            grad_in_min = int(float(row.get('grad_in_state_min_tuition', 0) or 0))
            grad_in_max = int(float(row.get('grad_in_state_max_tuition', 0) or 0))
            grad_out_min = int(float(row.get('grad_out_of_state_min_tuition', 0) or 0))
            grad_out_max = int(float(row.get('grad_out_of_state_max_tuition', 0) or 0))

            for university in universities:
                major_slug = f"{slugify(university.name).replace('-', '')}-{slugify(major_name).replace('-', '')}"

                # ✅ Add base tuition to totals
                total_in_min = in_state_min + (university.in_state_base_min_tuition or 0)
                total_in_max = in_state_max + (university.in_state_base_max_tuition or 0)
                total_out_min = out_state_min + (university.out_of_state_base_min_tuition or 0)
                total_out_max = out_state_max + (university.out_of_state_base_max_tuition or 0)

                major_objects.append(Major(
                    university=university,
                    major_name=major_name,
                    major_description=major_description,
                    department=department,
                    in_state_min_tuition=total_in_min,
                    in_state_max_tuition=total_in_max,
                    out_of_state_min_tuition=total_out_min,
                    out_of_state_max_tuition=total_out_max,
                    fees=fees,
                    grad_in_state_min_tuition=grad_in_min,
                    grad_in_state_max_tuition=grad_in_max,
                    grad_out_of_state_min_tuition=grad_out_min,
                    grad_out_of_state_max_tuition=grad_out_max,
                    slug=major_slug
                ))

        print(f"Attempting bulk insert of {len(major_objects)} majors...")
        Major.objects.bulk_create(major_objects, ignore_conflicts=True)
        print("Finished importing majors.")


if __name__ == "__main__":
    run()
