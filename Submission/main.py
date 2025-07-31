import json
from datetime import datetime


def read_JSON():
    """
    Reads and parses the JSON file named 'InputData.json'.
    Extracts job metadata and employee punch data.
    Calls calculate_pay to process the data.
    """
    with open("InputData.json", "r") as file:
        employee_data = json.load(file)
        job_meta = employee_data["jobMeta"]
        employee_punches = employee_data["employeeData"]
        calculate_pay(job_meta, employee_punches)


def calculate_pay(job_meta, employee_punches):
    """
    Processes employee punches and job metadata to calculate pay.
    Outputs the results in a dictionary for each employee.
    """
    output = {}

    print(json.dumps(job_meta, indent=2))
    for emp in employee_punches:
        employee_name = emp["employee"]
        print(employee_name)

        for tp in emp["timePunch"]:
            s = datetime.strptime(tp["start"], "%Y-%m-%d %H:%M:%S")
            e = datetime.strptime(tp["end"], "%Y-%m-%d %H:%M:%S")
            shift_duration = round((e - s).total_seconds() / 3600.0, 4)
            print(shift_duration)
        print()


if __name__ == "__main__":
    read_JSON()
