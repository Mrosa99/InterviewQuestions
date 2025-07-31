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

    for emp in employee_punches:
        employee_name = emp["employee"]
        total_hours = 0.0
        regular_hours = 0.0
        ot_hours = 0.0
        dt_hours = 0.0
        wage_total = 0.0
        benefit_total = 0.0

        for tp in emp["timePunch"]:
            s = datetime.strptime(tp["start"], "%Y-%m-%d %H:%M:%S")
            e = datetime.strptime(tp["end"], "%Y-%m-%d %H:%M:%S")
            hrs_worked = round((e - s).total_seconds() / 3600.0, 4)

            job = tp["job"]
            job_info = [j for j in job_meta if j["job"] == job][0]

            rate = job_info["rate"]
            ben_rate = job_info["benefitsRate"]

            unprocessed_hours = hrs_worked

            # Process regular hours left before 48-hour cap
            if total_hours < 40:
                regular_hours_to_add = min(40 - total_hours, unprocessed_hours)
                regular_hours += regular_hours_to_add
                wage_total += regular_hours_to_add * rate
                benefit_total += regular_hours_to_add * ben_rate
                total_hours += regular_hours_to_add
                unprocessed_hours -= regular_hours_to_add

            # Process overtime hours left before 48-hour cap
            ot_hours_available = 48 - total_hours
            if unprocessed_hours > 0 and ot_hours_available > 0:
                ot_hours_to_add = min(ot_hours_available, unprocessed_hours)
                ot_hours += ot_hours_to_add
                wage_total += ot_hours_to_add * rate * 1.5
                benefit_total += ot_hours_to_add * ben_rate
                total_hours += ot_hours_to_add
                unprocessed_hours -= ot_hours_to_add

            # Process anything about 48 hours
            if unprocessed_hours > 0:
                dt_hours += unprocessed_hours
                wage_total += unprocessed_hours * rate * 2
                benefit_total += unprocessed_hours * ben_rate
                total_hours += unprocessed_hours
                unprocessed_hours = 0

        # Store results for this employee
        output[employee_name] = {
            "employee": employee_name,
            "regular": f"{regular_hours:.4f}",
            "overtime": f"{ot_hours:.4f}",
            "doubletime": f"{dt_hours:.4f}",
            "wageTotal": f"{wage_total:.4f}",
            "benefitTotal": f"{benefit_total:.4f}",
        }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    read_JSON(".")
