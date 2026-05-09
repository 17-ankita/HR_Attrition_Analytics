import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="HR Attrition Analytics Dashboard",
    page_icon="👥",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617, #111827, #1e293b);
    color: #f8fafc;
}

section[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid rgba(255,255,255,0.08);
}

h1 {
    color: #38bdf8 !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #f8fafc !important;
}

[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0f172a, #1e3a8a);
    border: 1px solid rgba(56,189,248,0.25);
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
}

[data-testid="metric-container"] label {
    color: #cbd5e1 !important;
}

[data-testid="metric-container"] div {
    color: white !important;
}

button[data-baseweb="tab"] {
    background: #1e293b !important;
    color: white !important;
    border-radius: 12px !important;
    margin-right: 8px !important;
    padding: 10px 18px !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #0284c7, #38bdf8) !important;
    color: white !important;
}

[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}

.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HELPER FUNCTION ----------------
def apply_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_font=dict(size=20, color="white"),
        legend=dict(font=dict(color="white"))
    )
    return fig


# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("hr_attrition.csv")
    return df


df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.title("HR Analytics Filters")
st.sidebar.write("Filter employee data")

department_filter = st.sidebar.multiselect(
    "Select Department",
    sorted(df["Department"].unique()),
    default=sorted(df["Department"].unique())
)

jobrole_filter = st.sidebar.multiselect(
    "Select Job Role",
    sorted(df["JobRole"].unique()),
    default=sorted(df["JobRole"].unique())
)

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

overtime_filter = st.sidebar.multiselect(
    "Select Overtime",
    sorted(df["OverTime"].unique()),
    default=sorted(df["OverTime"].unique())
)

filtered_df = df[
    (df["Department"].isin(department_filter)) &
    (df["JobRole"].isin(jobrole_filter)) &
    (df["Gender"].isin(gender_filter)) &
    (df["OverTime"].isin(overtime_filter))
].copy()

# ---------------- HEADER ----------------
st.title("HR Attrition Analytics Dashboard")

st.markdown("""
This dashboard analyzes employee attrition patterns using **Python, SQL, Streamlit, Pandas, and Plotly**.
It helps identify high-risk employee segments, department-level attrition, overtime impact,
income patterns, satisfaction levels, and workforce retention insights.
""")

# ---------------- KPIs ----------------
total_employees = len(filtered_df)
attrition_count = filtered_df[filtered_df["Attrition"] == "Yes"].shape[0]
active_count = total_employees - attrition_count
attrition_rate = (attrition_count / total_employees * 100) if total_employees > 0 else 0
avg_age = filtered_df["Age"].mean() if total_employees > 0 else 0
avg_income = filtered_df["MonthlyIncome"].mean() if total_employees > 0 else 0
avg_years = filtered_df["YearsAtCompany"].mean() if total_employees > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Employees", total_employees)
col2.metric("Employees Left", attrition_count)
col3.metric("Active Employees", active_count)
col4.metric("Attrition Rate", f"{attrition_rate:.2f}%")

col5, col6, col7 = st.columns(3)
col5.metric("Average Age", f"{avg_age:.1f}")
col6.metric("Avg Monthly Income", f"₹{avg_income:,.0f}")
col7.metric("Avg Years at Company", f"{avg_years:.1f}")

st.divider()

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Department Analysis",
    "Employee Segments",
    "Satisfaction & Workload",
    "SQL Insights"
])

# ---------------- TAB 1 ----------------
with tab1:
    st.subheader("Overall Attrition Overview")

    col1, col2 = st.columns(2)

    with col1:
        attrition_data = filtered_df["Attrition"].value_counts().reset_index()
        attrition_data.columns = ["Attrition", "Count"]

        fig = px.pie(
            attrition_data,
            names="Attrition",
            values="Count",
            title="Attrition Distribution",
            hole=0.45
        )
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col2:
        dept_count = filtered_df["Department"].value_counts().reset_index()
        dept_count.columns = ["Department", "Employees"]

        fig = px.bar(
            dept_count,
            x="Department",
            y="Employees",
            title="Employees by Department",
            text="Employees",
            color="Department"
        )
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        role_count = filtered_df["JobRole"].value_counts().reset_index()
        role_count.columns = ["Job Role", "Employees"]

        fig = px.bar(
            role_count,
            x="Job Role",
            y="Employees",
            title="Employees by Job Role",
            text="Employees",
            color="Job Role"
        )
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col4:
        income_fig = px.histogram(
            filtered_df,
            x="MonthlyIncome",
            color="Attrition",
            title="Monthly Income Distribution by Attrition",
            nbins=25
        )
        st.plotly_chart(apply_theme(income_fig), use_container_width=True)

# ---------------- TAB 2 ----------------
with tab2:
    st.subheader("Department and Job Role Attrition Analysis")

    dept = (
        filtered_df.groupby("Department")
        .agg(
            Total_Employees=("EmployeeNumber", "count"),
            Attrition_Count=("AttritionFlag", "sum"),
            Avg_Income=("MonthlyIncome", "mean"),
            Avg_Age=("Age", "mean"),
            Avg_Years=("YearsAtCompany", "mean")
        )
        .reset_index()
    )

    dept["Attrition_Rate_%"] = (
        dept["Attrition_Count"] / dept["Total_Employees"] * 100
    ).round(2)

    dept["Avg_Income"] = dept["Avg_Income"].round(0)
    dept["Avg_Age"] = dept["Avg_Age"].round(1)
    dept["Avg_Years"] = dept["Avg_Years"].round(1)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            dept.sort_values("Attrition_Rate_%", ascending=False),
            x="Department",
            y="Attrition_Rate_%",
            title="Department-wise Attrition Rate",
            text_auto=".1f",
            color="Attrition_Rate_%"
        )
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col2:
        fig = px.bar(
            dept.sort_values("Avg_Income", ascending=False),
            x="Department",
            y="Avg_Income",
            title="Average Monthly Income by Department",
            text_auto=".0f",
            color="Avg_Income"
        )
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    st.markdown("### Department Scorecard")
    st.dataframe(dept, use_container_width=True)

    role = (
        filtered_df.groupby("JobRole")
        .agg(
            Total_Employees=("EmployeeNumber", "count"),
            Attrition_Count=("AttritionFlag", "sum"),
            Avg_Income=("MonthlyIncome", "mean"),
            Avg_Years=("YearsAtCompany", "mean")
        )
        .reset_index()
    )

    role["Attrition_Rate_%"] = (
        role["Attrition_Count"] / role["Total_Employees"] * 100
    ).round(2)

    role["Avg_Income"] = role["Avg_Income"].round(0)
    role["Avg_Years"] = role["Avg_Years"].round(1)

    fig = px.bar(
        role.sort_values("Attrition_Rate_%", ascending=False),
        x="JobRole",
        y="Attrition_Rate_%",
        title="Job Role-wise Attrition Rate",
        text_auto=".1f",
        color="Attrition_Rate_%"
    )
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(apply_theme(fig), use_container_width=True)

# ---------------- TAB 3 ----------------
with tab3:
    st.subheader("Employee Segment Analysis")

    bins = [18, 25, 35, 45, 55, 65]
    labels = ["18-25", "26-35", "36-45", "46-55", "56+"]
    filtered_df["Age_Group"] = pd.cut(filtered_df["Age"], bins=bins, labels=labels, include_lowest=True)

    income_bins = [0, 3000, 6000, 9000, 12000, 25000]
    income_labels = ["0-3K", "3K-6K", "6K-9K", "9K-12K", "12K+"]
    filtered_df["Income_Band"] = pd.cut(
        filtered_df["MonthlyIncome"],
        bins=income_bins,
        labels=income_labels,
        include_lowest=True
    )

    col1, col2 = st.columns(2)

    with col1:
        age_attrition = (
            filtered_df.groupby("Age_Group", observed=True)
            .agg(
                Employees=("EmployeeNumber", "count"),
                Attrition_Count=("AttritionFlag", "sum")
            )
            .reset_index()
        )
        age_attrition["Attrition_Rate_%"] = (
            age_attrition["Attrition_Count"] / age_attrition["Employees"] * 100
        ).round(2)

        fig = px.bar(
            age_attrition,
            x="Age_Group",
            y="Attrition_Rate_%",
            title="Attrition Rate by Age Group",
            text_auto=".1f",
            color="Attrition_Rate_%"
        )
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col2:
        income_attrition = (
            filtered_df.groupby("Income_Band", observed=True)
            .agg(
                Employees=("EmployeeNumber", "count"),
                Attrition_Count=("AttritionFlag", "sum")
            )
            .reset_index()
        )
        income_attrition["Attrition_Rate_%"] = (
            income_attrition["Attrition_Count"] / income_attrition["Employees"] * 100
        ).round(2)

        fig = px.bar(
            income_attrition,
            x="Income_Band",
            y="Attrition_Rate_%",
            title="Attrition Rate by Income Band",
            text_auto=".1f",
            color="Attrition_Rate_%"
        )
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        gender_data = (
            filtered_df.groupby("Gender")
            .agg(
                Employees=("EmployeeNumber", "count"),
                Attrition_Count=("AttritionFlag", "sum")
            )
            .reset_index()
        )
        gender_data["Attrition_Rate_%"] = (
            gender_data["Attrition_Count"] / gender_data["Employees"] * 100
        ).round(2)

        fig = px.bar(
            gender_data,
            x="Gender",
            y="Attrition_Rate_%",
            title="Attrition Rate by Gender",
            text_auto=".1f",
            color="Gender"
        )
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col4:
        marital_data = (
            filtered_df.groupby("MaritalStatus")
            .agg(
                Employees=("EmployeeNumber", "count"),
                Attrition_Count=("AttritionFlag", "sum")
            )
            .reset_index()
        )
        marital_data["Attrition_Rate_%"] = (
            marital_data["Attrition_Count"] / marital_data["Employees"] * 100
        ).round(2)

        fig = px.bar(
            marital_data,
            x="MaritalStatus",
            y="Attrition_Rate_%",
            title="Attrition Rate by Marital Status",
            text_auto=".1f",
            color="MaritalStatus"
        )
        st.plotly_chart(apply_theme(fig), use_container_width=True)

# ---------------- TAB 4 ----------------
with tab4:
    st.subheader("Satisfaction, Workload and Retention Factors")

    col1, col2 = st.columns(2)

    with col1:
        overtime = (
            filtered_df.groupby("OverTime")
            .agg(
                Employees=("EmployeeNumber", "count"),
                Attrition_Count=("AttritionFlag", "sum"),
                Avg_WorkLifeBalance=("WorkLifeBalance", "mean")
            )
            .reset_index()
        )
        overtime["Attrition_Rate_%"] = (
            overtime["Attrition_Count"] / overtime["Employees"] * 100
        ).round(2)
        overtime["Avg_WorkLifeBalance"] = overtime["Avg_WorkLifeBalance"].round(2)

        fig = px.bar(
            overtime,
            x="OverTime",
            y="Attrition_Rate_%",
            title="Overtime Impact on Attrition",
            text_auto=".1f",
            color="OverTime"
        )
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col2:
        travel = (
            filtered_df.groupby("BusinessTravel")
            .agg(
                Employees=("EmployeeNumber", "count"),
                Attrition_Count=("AttritionFlag", "sum")
            )
            .reset_index()
        )
        travel["Attrition_Rate_%"] = (
            travel["Attrition_Count"] / travel["Employees"] * 100
        ).round(2)

        fig = px.bar(
            travel.sort_values("Attrition_Rate_%", ascending=False),
            x="BusinessTravel",
            y="Attrition_Rate_%",
            title="Business Travel Impact on Attrition",
            text_auto=".1f",
            color="BusinessTravel"
        )
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        satisfaction = (
            filtered_df.groupby("JobSatisfaction")
            .agg(
                Employees=("EmployeeNumber", "count"),
                Attrition_Count=("AttritionFlag", "sum")
            )
            .reset_index()
        )
        satisfaction["Attrition_Rate_%"] = (
            satisfaction["Attrition_Count"] / satisfaction["Employees"] * 100
        ).round(2)

        fig = px.line(
            satisfaction,
            x="JobSatisfaction",
            y="Attrition_Rate_%",
            title="Job Satisfaction vs Attrition Rate",
            markers=True
        )
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col4:
        worklife = (
            filtered_df.groupby("WorkLifeBalance")
            .agg(
                Employees=("EmployeeNumber", "count"),
                Attrition_Count=("AttritionFlag", "sum")
            )
            .reset_index()
        )
        worklife["Attrition_Rate_%"] = (
            worklife["Attrition_Count"] / worklife["Employees"] * 100
        ).round(2)

        fig = px.line(
            worklife,
            x="WorkLifeBalance",
            y="Attrition_Rate_%",
            title="Work-Life Balance vs Attrition Rate",
            markers=True
        )
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    st.markdown("### Overtime Scorecard")
    st.dataframe(overtime, use_container_width=True)

# ---------------- TAB 5 ----------------
with tab5:
    st.subheader("SQL-Style Business Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Top Job Roles by Attrition Rate")
        top_roles = (
            filtered_df.groupby("JobRole")
            .agg(
                Total_Employees=("EmployeeNumber", "count"),
                Attrition_Count=("AttritionFlag", "sum"),
                Avg_Income=("MonthlyIncome", "mean")
            )
            .reset_index()
        )
        top_roles["Attrition_Rate_%"] = (
            top_roles["Attrition_Count"] / top_roles["Total_Employees"] * 100
        ).round(2)
        top_roles["Avg_Income"] = top_roles["Avg_Income"].round(0)

        top_roles = top_roles.sort_values("Attrition_Rate_%", ascending=False)
        st.dataframe(top_roles, use_container_width=True)

    with col2:
        st.markdown("### Department-Level Workforce Summary")
        dept_summary = (
            filtered_df.groupby("Department")
            .agg(
                Employees=("EmployeeNumber", "count"),
                Avg_Age=("Age", "mean"),
                Avg_Income=("MonthlyIncome", "mean"),
                Avg_Years=("YearsAtCompany", "mean"),
                Attrition_Count=("AttritionFlag", "sum")
            )
            .reset_index()
        )
        dept_summary["Attrition_Rate_%"] = (
            dept_summary["Attrition_Count"] / dept_summary["Employees"] * 100
        ).round(2)
        dept_summary = dept_summary.round(2)

        st.dataframe(dept_summary, use_container_width=True)

    st.markdown("### Department × Job Role Attrition Heatmap")

    heatmap = filtered_df.pivot_table(
        index="Department",
        columns="JobRole",
        values="AttritionFlag",
        aggfunc="mean",
        fill_value=0
    ) * 100

    fig = px.imshow(
        heatmap.round(1),
        text_auto=".1f",
        title="Attrition Rate Heatmap: Department vs Job Role",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(apply_theme(fig), use_container_width=True)

# ---------------- DATASET VIEW ----------------
st.divider()

with st.expander("View Filtered Dataset"):
    st.dataframe(filtered_df, use_container_width=True)