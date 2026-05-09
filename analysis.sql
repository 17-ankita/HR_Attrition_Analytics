-- =============================================================
-- HR ATTRITION ANALYTICS SQL FILE
-- Dataset table name: hr_attrition
-- =============================================================

-- Q1. Total employees
SELECT 
    COUNT(*) AS total_employees
FROM hr_attrition;

-- Q2. Total attrition count
SELECT 
    COUNT(*) AS attrition_count
FROM hr_attrition
WHERE Attrition = 'Yes';

-- Q3. Overall attrition rate
SELECT 
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage
FROM hr_attrition;

-- Q4. Department-wise attrition
SELECT 
    Department,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage,
    ROUND(AVG(MonthlyIncome), 2) AS avg_monthly_income
FROM hr_attrition
GROUP BY Department
ORDER BY attrition_rate_percentage DESC;

-- Q5. Job role-wise attrition
SELECT 
    JobRole,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage,
    ROUND(AVG(MonthlyIncome), 2) AS avg_monthly_income
FROM hr_attrition
GROUP BY JobRole
ORDER BY attrition_rate_percentage DESC;

-- Q6. Attrition by gender
SELECT 
    Gender,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage
FROM hr_attrition
GROUP BY Gender;

-- Q7. Attrition by marital status
SELECT 
    MaritalStatus,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage
FROM hr_attrition
GROUP BY MaritalStatus
ORDER BY attrition_rate_percentage DESC;

-- Q8. Overtime impact on attrition
SELECT 
    OverTime,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage,
    ROUND(AVG(WorkLifeBalance), 2) AS avg_work_life_balance
FROM hr_attrition
GROUP BY OverTime;

-- Q9. Business travel impact on attrition
SELECT 
    BusinessTravel,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage,
    ROUND(AVG(DistanceFromHome), 2) AS avg_distance_from_home
FROM hr_attrition
GROUP BY BusinessTravel
ORDER BY attrition_rate_percentage DESC;

-- Q10. Age group attrition
SELECT 
    CASE
        WHEN Age BETWEEN 18 AND 25 THEN '18-25'
        WHEN Age BETWEEN 26 AND 35 THEN '26-35'
        WHEN Age BETWEEN 36 AND 45 THEN '36-45'
        WHEN Age BETWEEN 46 AND 55 THEN '46-55'
        ELSE '56+'
    END AS age_group,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage
FROM hr_attrition
GROUP BY age_group
ORDER BY age_group;

-- Q11. Income band attrition
SELECT 
    CASE
        WHEN MonthlyIncome <= 3000 THEN '0-3K'
        WHEN MonthlyIncome <= 6000 THEN '3K-6K'
        WHEN MonthlyIncome <= 9000 THEN '6K-9K'
        WHEN MonthlyIncome <= 12000 THEN '9K-12K'
        ELSE '12K+'
    END AS income_band,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage,
    ROUND(AVG(JobSatisfaction), 2) AS avg_job_satisfaction
FROM hr_attrition
GROUP BY income_band
ORDER BY income_band;

-- Q12. Job satisfaction and attrition
SELECT 
    JobSatisfaction,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage
FROM hr_attrition
GROUP BY JobSatisfaction
ORDER BY JobSatisfaction;

-- Q13. Environment satisfaction and attrition
SELECT 
    EnvironmentSatisfaction,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage
FROM hr_attrition
GROUP BY EnvironmentSatisfaction
ORDER BY EnvironmentSatisfaction;

-- Q14. Work-life balance and attrition
SELECT 
    WorkLifeBalance,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage
FROM hr_attrition
GROUP BY WorkLifeBalance
ORDER BY WorkLifeBalance;

-- Q15. Years at company and attrition
SELECT 
    YearsAtCompany,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage
FROM hr_attrition
GROUP BY YearsAtCompany
ORDER BY YearsAtCompany;

-- Q16. Distance from home and attrition
SELECT 
    CASE
        WHEN DistanceFromHome <= 5 THEN '0-5 km'
        WHEN DistanceFromHome <= 10 THEN '6-10 km'
        WHEN DistanceFromHome <= 20 THEN '11-20 km'
        ELSE '20+ km'
    END AS distance_band,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage
FROM hr_attrition
GROUP BY distance_band
ORDER BY distance_band;

-- Q17. Training frequency and attrition
SELECT 
    TrainingTimesLastYear,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage
FROM hr_attrition
GROUP BY TrainingTimesLastYear
ORDER BY TrainingTimesLastYear;

-- Q18. Education field-wise attrition
SELECT 
    EducationField,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage
FROM hr_attrition
GROUP BY EducationField
ORDER BY attrition_rate_percentage DESC;

-- Q19. Performance rating and attrition
SELECT 
    PerformanceRating,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage
FROM hr_attrition
GROUP BY PerformanceRating
ORDER BY PerformanceRating;

-- Q20. Full department scorecard
SELECT 
    Department,
    COUNT(*) AS total_employees,
    SUM(AttritionFlag) AS attrition_count,
    ROUND(SUM(AttritionFlag) * 100.0 / COUNT(*), 2) AS attrition_rate_percentage,
    ROUND(AVG(Age), 2) AS avg_age,
    ROUND(AVG(MonthlyIncome), 2) AS avg_income,
    ROUND(AVG(YearsAtCompany), 2) AS avg_years_at_company,
    ROUND(AVG(JobSatisfaction), 2) AS avg_job_satisfaction,
    ROUND(AVG(WorkLifeBalance), 2) AS avg_work_life_balance
FROM hr_attrition
GROUP BY Department
ORDER BY attrition_rate_percentage DESC;