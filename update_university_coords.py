import os
import csv
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pestopanini.settings")
django.setup()

from MajorHelp.models import University

updated = 0
not_found = []
skipped = []

with open('Updated_University_Data.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['institution name'].strip()
        location = row['location'].strip()
        lat = row['latitude']
        lng = row['longitude']

        if not lat or not lng:
            continue  # skip if lat/lng missing

        # Get all universities with same name and location
        matches = University.objects.filter(name__iexact=name, location__iexact=location)

        if not matches.exists():
            not_found.append(f"{name} ({location})")
            print(f"❌ Not found: {name} ({location})")
            continue

        # Delete any with no majors
        with_majors = []
        for uni in matches:
            if uni.majors.exists():
                with_majors.append(uni)
            else:
                print(f"🗑️ Deleting duplicate with no majors: {uni.name} ({uni.location})")
                uni.delete()

        # If no university left after deletion, skip
        if not with_majors:
            skipped.append(f"{name} ({location})")
            print(f"⚠️ Skipped: No matching university with majors remains for {name} ({location})")
            continue

        # Use the first university that has majors
        uni = with_majors[0]
        uni.latitude = float(lat)
        uni.longitude = float(lng)
        uni.save()
        updated += 1
        print(f"✅ Updated {uni.name} ({uni.location})")

# Final summary
print(f"\n✅ {updated} universities updated.")
if not_found:
    print(f"❌ {len(not_found)} not found:")
    for item in not_found:
        print(f" - {item}")

if skipped:
    print(f"\n⚠️ {len(skipped)} skipped (no university with majors remained):")
    for item in skipped:
        print(f" - {item}")
