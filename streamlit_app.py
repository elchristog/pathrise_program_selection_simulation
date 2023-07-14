import pandas as pd
import streamlit as st

# Create Streamlit inputs
min_reach, max_reach = st.sidebar.slider("Enter the range for Reach salaries:", 0, 200000, (140000, 180000))
min_target, max_target = st.sidebar.slider("Enter the range for Target salaries:", 0, 200000, (80000, 140000))
min_safety, max_safety = st.sidebar.slider("Enter the range for Safety salaries:", 0, 200000, (60000, 100000))

cost_basic = st.sidebar.number_input("Enter the cost for Basic program:", min_value=0, value=12000)
cost_essentials = st.sidebar.number_input("Enter the cost for Essentials program:", min_value=0, value=18000)
cost_professional = st.sidebar.number_input("Enter the cost for Professional program:", min_value=0, value=24000)

percentage_basic = st.sidebar.number_input("Enter the percentage for Basic program:", min_value=0, max_value=100, value=7)
percentage_essentials = st.sidebar.number_input("Enter the percentage for Essentials program:", min_value=0, max_value=100, value=11)
percentage_professional = st.sidebar.number_input("Enter the percentage for Professional program:", min_value=0, max_value=100, value=14)

# Define the job scenarios
job_scenarios = {
    "Reach": {
        "Job Role": "Reach: Senior Data Analyst, Data Scientist, Machine Learning Engineer",
        "Probability of Job Level": 0.1,
        "Expected Annual Salary": (min_reach + max_reach) / 2,
    },
    "Target": {
        "Job Role": "Target: Data Analyst, Associate Data Scientist, Assistant/Junior Machine Learning Engineer",
        "Probability of Job Level": 0.25,
        "Expected Annual Salary": (min_target + max_target) / 2,
    },
    "Safety": {
        "Job Role": "Safety: Data Specialist, Data Associate, Junior Data Analyst/Scientist",
        "Probability of Job Level": 0.65,
        "Expected Annual Salary": (min_safety + max_safety) / 2,
    },
}

# Define the program scenarios
program_scenarios = {
    "Basic": {
        "Cost of Program": cost_basic,
        "Program Percentage of Payment": percentage_basic,
        "Job Search Speed": 0.2,
    },
    "Essentials": {
        "Cost of Program": cost_essentials,
        "Program Percentage of Payment": percentage_essentials,
        "Job Search Speed": 0.3,
    },
    "Professional": {
        "Cost of Program": cost_professional,
        "Program Percentage of Payment": percentage_professional,
        "Job Search Speed": 0.5,
    },
}

# Create a DataFrame for each job scenario
dataframes = []
for job_scenario, job_values in job_scenarios.items():
    for program_scenario, program_values in program_scenarios.items():
        row = {
            "Program": program_scenario,
            "Job Role": job_values["Job Role"],
            "Probability of Job Level": job_values["Probability of Job Level"],
            "Expected Annual Salary": job_values["Expected Annual Salary"],
            "Expected Monthly Salary": job_values["Expected Annual Salary"] / 12,
            "Cost of Program": program_values["Cost of Program"],
            "Program Percentage of Payment": program_values["Program Percentage of Payment"],
            "Job Search Speed": program_values["Job Search Speed"],
        }
        row["Program Cost CAP"] = row["Expected Annual Salary"] * row["Program Percentage of Payment"] / 100
        row["Program Cost CAP"] = min(row["Program Cost CAP"], row["Cost of Program"])  # Cap at maximum cost
        row["Free Monthly Money"] = row["Expected Monthly Salary"] - row["Program Cost CAP"] / 12
        row["Free Annually Money"] = row["Expected Annual Salary"] - row["Program Cost CAP"]
        row["Free Monthly Money percentage"] = (row["Free Monthly Money"] / row["Expected Monthly Salary"])
        row["Final Score"] = ((row["Probability of Job Level"] * row["Free Monthly Money percentage"]) * 0.6) + (row["Job Search Speed"] * 0.4)
        dataframes.append(row)

# Combine into a single DataFrame
df = pd.DataFrame(dataframes)

# Reorder columns
df = df[["Job Role", "Program", "Probability of Job Level", "Cost of Program", "Expected Annual Salary", "Expected Monthly Salary",
         "Program Percentage of Payment", "Program Cost CAP", "Job Search Speed", "Free Monthly Money", "Free Annually Money",
         "Free Monthly Money percentage", "Final Score"]]

# Display the DataFrame
st.write(df)
