import pandas as pd
import numpy as np

df = pd.read_csv("hr_attrition.csv")

print("=" * 60)
print("HR ATTRITION ANALYTICS REPORT")
print("=" * 60)

print("\nDataset Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

# ---------------- BASIC KPIs ----------------
total_employees = len(df)
attrition_count = df[df["Attrition"] == "Yes"].shape[0]
attrition_rate = attrition_count / total_employees * 100
avg_age = df["Age"].mean()
avg_income = df["MonthlyIncome"].mean()
avg_years_company = df["YearsAtCompany"].mean()

print("\n" + "=" * 60)
print("KEY PERFORMANCE INDICATORS")
print("=" * 60)

print(f"Total Employees      : {total_employees}")
print(f"Employees Left       : {attrition_count}")
print(f"Attrition Rate       : {attrition_rate:.2f}%")
print(f"Average Age          : {avg_age:.1f}")
print(f"Average Monthly Income: ₹{avg_income:,.0f}")
print(f"Avg Years at Company : {avg_years_company:.1f}")

# ---------------- DEPARTMENT ANALYSIS ----------------
print("\n" + "=" * 60)
print("DEPARTMENT-WISE ATTRITION")
print("=" * 60)

dept = (
    df.groupby("Department")
    .agg(
        Total_Employees=("EmployeeNumber", "count"),
        Attrition_Count=("AttritionFlag", "sum"),
        Avg_Income=("MonthlyIncome", "mean"),
        Avg_Age=("Age", "mean")
    )
    .reset_index()
)

dept["Attrition_Rate_%"] = (
    dept["Attrition_Count"] / dept["Total_Employees"] * 100
).round(2)

print(dept.to_string(index=False))

# ---------------- JOB ROLE ANALYSIS ----------------
print("\n" + "=" * 60)
print("JOB ROLE-WISE ATTRITION")
print("=" * 60)

role = (
    df.groupby("JobRole")
    .agg(
        Total_Employees=("EmployeeNumber", "count"),
        Attrition_Count=("AttritionFlag", "sum"),
        Avg_Income=("MonthlyIncome", "mean"),
        Avg_Years_Company=("YearsAtCompany", "mean")
    )
    .reset_index()
)

role["Attrition_Rate_%"] = (
    role["Attrition_Count"] / role["Total_Employees"] * 100
).round(2)

role = role.sort_values("Attrition_Rate_%", ascending=False)

print(role.to_string(index=False))

# ---------------- OVERTIME ANALYSIS ----------------
print("\n" + "=" * 60)
print("OVERTIME VS ATTRITION")
print("=" * 60)

overtime = (
    df.groupby("OverTime")
    .agg(
        Total_Employees=("EmployeeNumber", "count"),
        Attrition_Count=("AttritionFlag", "sum"),
        Avg_Income=("MonthlyIncome", "mean"),
        Avg_WorkLifeBalance=("WorkLifeBalance", "mean")
    )
    .reset_index()
)

overtime["Attrition_Rate_%"] = (
    overtime["Attrition_Count"] / overtime["Total_Employees"] * 100
).round(2)

print(overtime.to_string(index=False))

# ---------------- AGE GROUP ANALYSIS ----------------
print("\n" + "=" * 60)
print("AGE GROUP ANALYSIS")
print("=" * 60)

bins = [18, 25, 35, 45, 55, 65]
labels = ["18-25", "26-35", "36-45", "46-55", "56+"]
df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels, include_lowest=True)

age_group = (
    df.groupby("AgeGroup", observed=True)
    .agg(
        Total_Employees=("EmployeeNumber", "count"),
        Attrition_Count=("AttritionFlag", "sum"),
        Avg_Income=("MonthlyIncome", "mean"),
        Avg_Years_Company=("YearsAtCompany", "mean")
    )
    .reset_index()
)

age_group["Attrition_Rate_%"] = (
    age_group["Attrition_Count"] / age_group["Total_Employees"] * 100
).round(2)

print(age_group.to_string(index=False))

# ---------------- INCOME ANALYSIS ----------------
print("\n" + "=" * 60)
print("INCOME BAND ANALYSIS")
print("=" * 60)

income_bins = [0, 3000, 6000, 9000, 12000, 20000]
income_labels = ["0-3K", "3K-6K", "6K-9K", "9K-12K", "12K+"]
df["IncomeBand"] = pd.cut(df["MonthlyIncome"], bins=income_bins, labels=income_labels)

income = (
    df.groupby("IncomeBand", observed=True)
    .agg(
        Total_Employees=("EmployeeNumber", "count"),
        Attrition_Count=("AttritionFlag", "sum"),
        Avg_JobSatisfaction=("JobSatisfaction", "mean"),
        Avg_WorkLifeBalance=("WorkLifeBalance", "mean")
    )
    .reset_index()
)

income["Attrition_Rate_%"] = (
    income["Attrition_Count"] / income["Total_Employees"] * 100
).round(2)

print(income.to_string(index=False))

# ---------------- SATISFACTION ANALYSIS ----------------
print("\n" + "=" * 60)
print("SATISFACTION ANALYSIS")
print("=" * 60)

satisfaction = (
    df.groupby("JobSatisfaction")
    .agg(
        Total_Employees=("EmployeeNumber", "count"),
        Attrition_Count=("AttritionFlag", "sum"),
        Avg_Income=("MonthlyIncome", "mean")
    )
    .reset_index()
)

satisfaction["Attrition_Rate_%"] = (
    satisfaction["Attrition_Count"] / satisfaction["Total_Employees"] * 100
).round(2)

print(satisfaction.to_string(index=False))

# ---------------- BUSINESS TRAVEL ANALYSIS ----------------
print("\n" + "=" * 60)
print("BUSINESS TRAVEL ANALYSIS")
print("=" * 60)

travel = (
    df.groupby("BusinessTravel")
    .agg(
        Total_Employees=("EmployeeNumber", "count"),
        Attrition_Count=("AttritionFlag", "sum"),
        Avg_Distance=("DistanceFromHome", "mean"),
        Avg_Income=("MonthlyIncome", "mean")
    )
    .reset_index()
)

travel["Attrition_Rate_%"] = (
    travel["Attrition_Count"] / travel["Total_Employees"] * 100
).round(2)

print(travel.to_string(index=False))

# ---------------- KEY INSIGHTS ----------------
print("\n" + "=" * 60)
print("KEY INSIGHTS SUMMARY")
print("=" * 60)

print(f"""
1. Overall attrition rate is {attrition_rate:.2f}%.
2. Overtime can be compared with attrition to identify workload-related employee exits.
3. Department-wise attrition helps identify high-risk business units.
4. Job role analysis shows which roles have higher employee turnover.
5. Income bands help understand whether lower compensation is linked with attrition.
6. Satisfaction and work-life balance scores help explain employee retention risk.
""")