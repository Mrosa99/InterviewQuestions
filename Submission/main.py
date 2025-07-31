import json


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
    Receives job metadata and employee punches.
    """
    print(json.dumps(job_meta, indent=2))
    print(json.dumps(employee_punches, indent=2))


if __name__ == "__main__":
    read_JSON()
