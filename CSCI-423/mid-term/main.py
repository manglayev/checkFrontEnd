import os
from zipfile import ZipFile
import csv

# === PATHS (adjust as needed) ===
path = "/home/talgat/Desktop/mid-term-2"
file_result = "/home/talgat/Desktop/mid-term-2/results_mt2.csv"
file_participants = "/home/talgat/Desktop/mid-term-2/participants.csv"

# === CSV HEADER ===
with open(file_result, mode='w') as csv_file:
    fieldnames = ["first_name", "last_name", "id", "grade", "feedback"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

# === PROCESS SUBMISSIONS ===
directoryObject = os.scandir(path)

for entry in directoryObject:
    if not entry.is_dir():
        continue

    # Extract student names from folder name
    first_name = entry.name[0:entry.name.find(' ')]
    last_name = entry.name[entry.name.find(' ') + 1:entry.name.find('_')]
    student_info = {"first_name": first_name, "last_name": last_name, "id": ""}

    # Match ID from participants.csv
    with open(file_participants, newline='') as csvfile:
        path_participants = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in path_participants:
            if student_info["first_name"] in row[0] and student_info["last_name"] in row[0]:
                parts = row[0].split(',')
                if len(parts) >= 3:
                    student_info["id"] = parts[2]

    # === Unpack zip files ===
    entryDirectory = os.scandir(entry)
    for zip_file in entryDirectory:
        if zip_file.is_file():
            file_name, file_extension = os.path.splitext(zip_file)
            if file_extension == ".zip":
                new_name = file_name + "_archive.zip"
                os.rename(zip_file, new_name)
                with ZipFile(new_name, 'r') as zObject:
                    zObject.extractall(path=os.path.dirname(zip_file))
    # === Save results ===
    with open(file_result, mode='a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["first_name", "last_name", "id", "grade", "feedback"])
        writer.writerow({
            "first_name": student_info["first_name"],
            "last_name": student_info["last_name"],
            "id": student_info["id"],
            "grade": 0,
            "feedback": ""
        })