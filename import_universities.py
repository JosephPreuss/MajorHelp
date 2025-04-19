import os
import django
import csv
from django.utils.text import slugify

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pestopanini.settings")
django.setup()

from MajorHelp.models import University

CSV_PATH = "Updated_University_Data.csv"

def clean_slug(name):
    return slugify(name).replace('-', '')

def generate_unique_slug(base_name):
    base_slug = slugify(base_name).replace("-", "")
    slug = base_slug
    counter = 1
    while University.objects.filter(slug=slug).exists():
        slug = f"{base_slug}{counter}"
        counter += 1
    return slug

def run():
    print("Deleting all existing universities...")
    University.objects.all().delete()

    print("Importing new universities...")
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Read values
            in_state_min = int(float(row.get('In-state min tuition', 0) or 0))
            in_state_max = int(float(row.get('In-state max tuition', 0) or 0))
            out_state_min = int(float(row.get('Out-of-state min tuition', 0) or 0))
            out_state_max = int(float(row.get('Out-of-state max tuition', 0) or 0))

            #  Apply logic to fix 0 out-of-state min tuition
            if out_state_min == 0 and out_state_max > 0 and in_state_min <= out_state_max:
                out_state_min = in_state_min

            # Create university entry
            University.objects.create(
                name=row['institution name'].strip(),
                location=row['location'].strip(),
                is_public=row['is_public'].strip().lower() == 'true',
                aboutText=row['aboutText'].strip(),
                TotalUndergradStudents=int(float(row.get('Undergraduate enrollment', 0) or 0)),
                TotalGradStudents=int(float(row.get('Graduate enrollment', 0) or 0)),
                GraduationRate=float(row.get('Graduation rate', 0.0) or 0.0),
                latitude=float(row.get('Latitude', 0.0) or 0.0),
                longitude=float(row.get('Longitude', 0.0) or 0.0),
                in_state_base_min_tuition=in_state_min,
                in_state_base_max_tuition=in_state_max,
                out_of_state_base_min_tuition=out_state_min,
                out_of_state_base_max_tuition=out_state_max,
                fees=int(float(row.get('Fees', 0) or 0)),
                primary_color="#268f95",
                secondary_color="#FFFFFF",
                slug=generate_unique_slug(row['institution name']),
            )

    print("Import complete.")

if __name__ == "__main__":
    run()
