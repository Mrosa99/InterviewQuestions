# Payroll Calculator

This Python script reads employee punch data and job metadata from JSON files in a specified folder, calculates pay (regular, overtime, doubletime hours and wages), and outputs a combined summary for all employees.

---

## Features

- Processes multiple JSON files in a folder.
- Calculates:
  - Regular hours (up to 40 hours at base rate).
  - Overtime hours (40 to 48 hours at 1.5x rate).
  - Doubletime hours (above 48 hours at 2x rate).
  - Total wage and benefit costs.

---

## How to Run

1. Clone the repository

2. Change directory to `Submission`

<pre>
cd Submission
</pre>

3. (Highly recommended) Create and activate a virtual environment:

<pre>
python -m venv venv
</pre>

- On Windows, activate with:

<pre>
venv\Scripts\activate
</pre>

- On macOS/Linux, activate with:

<pre>
source venv/bin/activate
</pre>

4. Run the script

- On Windows, activate with:

<pre>
python main.py
</pre>

- On macOS/Linux, activate with:

<pre>
python3 main.py
</pre>

5. View results

- Output prints to terminal
- Also saved as `output.json` in the `Submission` folder.
