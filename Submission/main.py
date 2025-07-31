import json
from datetime import datetime
from pathlib import Path


def read_JSON(folder_path):
    """
    Reads all JSON files in the given folder and processes employee data.
    - Iterates through each .json file.
    - Parses the file content.
    - Validates that required keys ('jobMeta' and 'employeeData') are present.
    - Passes valid data to the pay calculation function.
    """
    json_files = Path(folder_path).glob("*.json")

    for file_path in json_files:
        with open(file_path, "r") as file:
            employee_data = json.load(file)

            job_meta = employee_data.get("jobMeta")
            employee_punches = employee_data.get("employeeData")
            if not job_meta:
                print(f'Missing "jobMeta" in: {file_path} => Skipping file')
                continue
            if not employee_punches:
                print(f'Missing "employeeData" in: {file_path}=> Skipping file')
                continue
            calculate_pay(job_meta, employee_punches)


def calculate_pay(job_meta, employee_punches):
    """
    Processes employee punches and job metadata to calculate pay.
    output = {}
    """
    print(json.dumps(job_meta, indent=2))
    for emp in employee_punches:
        employee_name = emp["employee"]
        print(employee_name)

        for tp in emp["timePunch"]:
            s = datetime.strptime(tp["start"], "%Y-%m-%d %H:%M:%S")
            e = datetime.strptime(tp["end"], "%Y-%m-%d %H:%M:%S")
            hrs_worked = round((e - s).total_seconds() / 3600.0, 4)
            print(hrs_worked)
        print()


if __name__ == "__main__":
    read_JSON(".")
