import json


##Calculate Pay Function
# This function reads employee punch data from a JSON file and calculates their pay.
def calculate_pay():
    with open("InputData.json", "r") as file:
        employee_data = json.load(file)
        job_meta = employee_data["jobMeta"]
        employee_punches = employee_data["employeeData"]

        print(json.dumps(employee_punches, indent=2))
        print(print(json.dumps(job_meta, indent=2)))


if __name__ == "__main__":
    calculate_pay()
