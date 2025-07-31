import json
from datetime import datetime
from pathlib import Path


def read_JSON(folder_path):
    """
    Reads all JSON files in the given folder and processes employee data.
    - Iterates through each .json file in the folder.
    - Loads and parses the JSON content.
    - Checks for required keys 'jobMeta' and 'employeeData'.
    - Calls pay calculation on valid data.
    - Merges results from all files into combined_output.
    - Prints combined output and saves it to output.json.
    """
    combined_output = {}
    json_files = Path(folder_path).glob("*.json")  # Get all JSON files in folder

    for file_path in json_files:
        with open(file_path, "r") as file:
            employee_data = json.load(file)

            job_meta = employee_data.get("jobMeta")
            employee_punches = employee_data.get("employeeData")

            # Validate presence of required keys
            if not job_meta:
                print(f'Missing "jobMeta" in: {file_path} => Skipping file')
                continue
            if not employee_punches:
                print(f'Missing "employeeData" in: {file_path}=> Skipping file')
                continue

        # Calculate pay for current file's data
        output = calculate_pay(job_meta, employee_punches)

        # Merge output into combined_output
        for emp_name, emp_data in output.items():
            if emp_name not in combined_output:
                combined_output[emp_name] = emp_data
            else:
                # Sum numeric fields for the same employee across files
                for key in [
                    "regular",
                    "overtime",
                    "doubletime",
                    "wageTotal",
                    "benefitTotal",
                ]:
                    combined_output[emp_name][
                        key
                    ] = f"{float(combined_output[emp_name][key]) + float(emp_data[key]):.4f}"

    # Print combined result to terminal
    print(json.dumps(combined_output, indent=2))

    # Save combined result to output.json file
    with open("output.json", "w") as file:
        json.dump(combined_output, file, indent=2)


def calculate_pay(job_meta, employee_punches):
    """
     Calculates pay details per employee based on their punches and job metadata.
    - Converts job_meta list into a dictionary for quick lookups.
    - Iterates over each employee's punches.
    - Calculates regular, overtime, and doubletime hours and wages.
    - Returns a dict mapping employee names to their summarized pay data.
    """
    output = {}

    # Create dictionary for fast job info lookup by job name
    job_dict = {j["job"]: j for j in job_meta}

    for emp in employee_punches:
        employee_name = emp["employee"]
        total_hours = 0.0
        regular_hours = 0.0
        ot_hours = 0.0
        dt_hours = 0.0
        wage_total = 0.0
        benefit_total = 0.0

        for tp in emp["timePunch"]:
            # Parse punch start and end times
            s = datetime.strptime(tp["start"], "%Y-%m-%d %H:%M:%S")
            e = datetime.strptime(tp["end"], "%Y-%m-%d %H:%M:%S")

            # Calculate hours worked for this punch
            hrs_worked = round((e - s).total_seconds() / 3600.0, 4)

            job = tp["job"]
            job_info = job_info = job_dict[job]

            rate = job_info["rate"]
            ben_rate = job_info["benefitsRate"]

            unprocessed_hours = hrs_worked

            # Calculate and accumulate regular hours (up to 40 hours)
            if total_hours < 40:
                regular_hours_to_add = min(40 - total_hours, unprocessed_hours)
                regular_hours += regular_hours_to_add
                wage_total += regular_hours_to_add * rate
                benefit_total += regular_hours_to_add * ben_rate
                total_hours += regular_hours_to_add
                unprocessed_hours -= regular_hours_to_add

            # Calculate and accumulate overtime hours (40 to 48 hours)
            ot_hours_available = 48 - total_hours
            if unprocessed_hours > 0 and ot_hours_available > 0:
                ot_hours_to_add = min(ot_hours_available, unprocessed_hours)
                ot_hours += ot_hours_to_add
                wage_total += ot_hours_to_add * rate * 1.5
                benefit_total += ot_hours_to_add * ben_rate
                total_hours += ot_hours_to_add
                unprocessed_hours -= ot_hours_to_add

            # Calculate and accumulate doubletime hours (above 48 hours)
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

    return output


if __name__ == "__main__":
    read_JSON(".")
