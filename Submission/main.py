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
    """
    output = {}

    # print(json.dumps(job_meta, indent=2))  # Remove After
    for emp in employee_punches:
        employee_name = emp["employee"]
        total_hours = 0.0
        regular_hours = 0.0
        wage_total = 0.0

        for tp in emp["timePunch"]:
            s = datetime.strptime(tp["start"], "%Y-%m-%d %H:%M:%S")
            e = datetime.strptime(tp["end"], "%Y-%m-%d %H:%M:%S")
            hrs_worked = round((e - s).total_seconds() / 3600.0, 4)

            job = tp["job"]
            job_info = [j for j in job_meta if j["job"] == job][0]

            rate = job_info["rate"]
            ben_rate = job_info["benefitsRate"]

            unprocessed_hours = hrs_worked

            if total_hours < 40:
                regular_hrs_available = min(40 - total_hours, unprocessed_hours)
                regular_hours += regular_hrs_available
                wage_total += regular_hrs_available * rate

        # Store results for this employee
        output[employee_name] = {
            "employee": employee_name,
            "regular": f"{regular_hours:.4f}",
            "wageTotal": f"{wage_total:.4f}",
        }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    read_JSON(".")
