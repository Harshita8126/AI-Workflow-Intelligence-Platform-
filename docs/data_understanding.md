# Data Understanding Report: Enterprise HR AI Platform

**Project:** Enterprise HR AI — Workforce Intelligence & Upskilling Platform  
**Document Version:** 1.0.0  
**Generated Date:** 2026-09-02  
**Author:** Lead AI Engineer & Full-Stack Architect  

---

## 1. Executive Summary

A comprehensive, ground-truth audit of the workspace and all raw data files was performed. No assumptions or synthetic data were injected. Every metric, shape, data type, missingness statistic, and relationship documented herein reflects the actual disk contents of the workspace.

### Key Highlights
1. **Workspace Files Found:** 6 CSV datasets across root and `data/raw/`, 1 architecture presentation (`Agentic_HRMS_Platform (1).pptx`), and 1 project build notebook document (`HR_AI_Project_Build_Notes.docx`).
2. **Attrition Ground Truth:** Standard IBM HR Analytics dataset (`WA_Fn-UseC_-HR-Employee-Attrition.csv`, 1,470 records, 35 features) provides high-quality tabular data for attrition modeling with 16.12% positive attrition rate.
3. **Performance & Engagement:** Two separate performance datasets exist (`Employee_Performance_Dataset.csv` with 5,000 records; `data/raw/employee_performance_pro.csv` with 500 records).
4. **Skills & Taxonomy:** Standard O*NET occupational taxonomies are present in `data/raw/` (`occupation_data.csv`: 1,016 occupations; `essential_skills.csv`: 18,200 records; `software_skills.csv`: 31,821 tools & technologies).
5. **Critical Missing Requirements Identified:**
   - **No Employee Skills Dataset:** No raw file contains current individual employee skill profiles (`employee_id` -> `skills`).
   - **No HR Policy Documents:** No policy documents, benefits handbooks, or leave guidelines exist for the Phase 4 RAG engine.
   - **ID Disconnect:** Employee IDs across the attrition and performance datasets do **NOT** refer to the same entities.

---

## 2. Workspace File Inventory

| Location | File Name | Size (Bytes) | File Type | Purpose / Domain |
| :--- | :--- | :--- | :--- | :--- |
| **Root** | `WA_Fn-UseC_-HR-Employee-Attrition.csv` | 227,977 | CSV | IBM HR Employee Attrition & Demographics (1,470 rows) |
| **Root** | `Employee_Performance_Dataset.csv` | 403,396 | CSV | Employee Performance & Productivity Scores (5,000 rows) |
| **Root** | `HR_AI_Project_Build_Notes.docx` | 20,705 | DOCX | Project build notes and phased engineering guidelines |
| **Root** | `Agentic_HRMS_Platform (1).pptx` | 614,529 | PPTX | Technical architecture and design presentation |
| `data/raw/` | `employee_performance_pro.csv` | 67,596 | CSV | Performance, engagement, leaves, and salary (500 rows) |
| `data/raw/` | `occupation_data.csv` | 268,030 | CSV | O*NET-SOC Master Occupation Taxonomy (1,016 roles) |
| `data/raw/` | `essential_skills.csv` | 2,328,135 | CSV | O*NET Foundation Skills Importance & Level (18,200 rows) |
| `data/raw/` | `software_skills.csv` | 3,557,545 | CSV | O*NET Software, Tools & Tech Competencies (31,821 rows) |

---

## 3. Detailed Dataset Profiling

### 3.1 `WA_Fn-UseC_-HR-Employee-Attrition.csv` (Primary Attrition Dataset)
* **Location:** Workspace Root
* **Shape:** 1,470 rows x 35 columns
* **Duplicate Rows:** 0 (0.0%)
* **Domain Entity:** Employee demographic, compensation, tenure, satisfaction, and turnover status.
* **Target Variable:** `Attrition` (`Yes`: 237 [16.12%], `No`: 1,233 [83.88%])
* **Primary Key Candidate:** `EmployeeNumber` (int64, values range from 1 to 2,068, 1,470 unique).

#### Column Breakdown & Schema

| # | Column Name | Dtype | Missing (Count / %) | Unique Count | Sample Values | Notes / Characteristics |
|---|---|---|---|---|---|---|
| 1 | `Age` | int64 | 0 (0.0%) | 43 | 41, 49, 37 | Range: 18 - 60, Mean: 36.92 |
| 2 | `Attrition` | object | 0 (0.0%) | 2 | 'Yes', 'No' | **Target Column** (Imbalanced: 16.1% Yes) |
| 3 | `BusinessTravel` | object | 0 (0.0%) | 3 | 'Travel_Rarely', 'Travel_Frequently', 'Non-Travel' | Categorical feature |
| 4 | `DailyRate` | int64 | 0 (0.0%) | 886 | 1102, 279, 1373 | Range: 102 - 1,499 |
| 5 | `Department` | object | 0 (0.0%) | 3 | 'Sales', 'Research & Development', 'Human Resources' | Categorical feature |
| 6 | `DistanceFromHome` | int64 | 0 (0.0%) | 29 | 1, 8, 2 | Range: 1 - 29 miles |
| 7 | `Education` | int64 | 0 (0.0%) | 5 | 2, 1, 4 | Ordinal (1: Below College, 5: Doctor) |
| 8 | `EducationField` | object | 0 (0.0%) | 6 | 'Life Sciences', 'Other', 'Medical' | Categorical feature |
| 9 | `EmployeeCount` | int64 | 0 (0.0%) | 1 | 1 | **Constant (Zero Variance)** - Drop |
| 10 | `EmployeeNumber` | int64 | 0 (0.0%) | 1470 | 1, 2, 4 | Primary Key identifier |
| 11 | `EnvironmentSatisfaction`| int64 | 0 (0.0%) | 4 | 2, 3, 4 | Likert scale (1: Low, 4: Very High) |
| 12 | `Gender` | object | 0 (0.0%) | 2 | 'Female', 'Male' | Sensitive demographic feature |
| 13 | `HourlyRate` | int64 | 0 (0.0%) | 71 | 94, 61, 92 | Range: 30 - 100 |
| 14 | `JobInvolvement` | int64 | 0 (0.0%) | 4 | 3, 2, 4 | Likert scale (1: Low, 4: Very High) |
| 15 | `JobLevel` | int64 | 0 (0.0%) | 5 | 2, 1, 3 | Ordinal hierarchy level (1 to 5) |
| 16 | `JobRole` | object | 0 (0.0%) | 9 | 'Sales Executive', 'Research Scientist', 'Laboratory Technician' | 9 distinct job roles |
| 17 | `JobSatisfaction` | int64 | 0 (0.0%) | 4 | 4, 2, 3 | Likert scale (1: Low, 4: Very High) |
| 18 | `MaritalStatus` | object | 0 (0.0%) | 3 | 'Single', 'Married', 'Divorced' | Sensitive demographic feature |
| 19 | `MonthlyIncome` | int64 | 0 (0.0%) | 1349 | 5993, 5130, 2090 | Range: 1,009 - 19,999 (Mean: 6,502.9) |
| 20 | `MonthlyRate` | int64 | 0 (0.0%) | 1427 | 19479, 24907, 2396 | Range: 2,094 - 26,999 |
| 21 | `NumCompaniesWorked` | int64 | 0 (0.0%) | 10 | 8, 1, 6 | Range: 0 - 9 |
| 22 | `Over18` | object | 0 (0.0%) | 1 | 'Y' | **Constant (Zero Variance)** - Drop |
| 23 | `OverTime` | object | 0 (0.0%) | 2 | 'Yes', 'No' | Binary feature ('Yes': 416, 'No': 1054) |
| 24 | `PercentSalaryHike` | int64 | 0 (0.0%) | 15 | 11, 23, 15 | Range: 11 - 25% |
| 25 | `PerformanceRating` | int64 | 0 (0.0%) | 2 | 3, 4 | Only values 3 (Excellent) & 4 (Outstanding) |
| 26 | `RelationshipSatisfaction`| int64 | 0 (0.0%) | 4 | 1, 4, 2 | Likert scale (1: Low, 4: Very High) |
| 27 | `StandardHours` | int64 | 0 (0.0%) | 1 | 80 | **Constant (Zero Variance)** - Drop |
| 28 | `StockOptionLevel` | int64 | 0 (0.0%) | 4 | 0, 1, 3 | Ordinal (0 to 3) |
| 29 | `TotalWorkingYears` | int64 | 0 (0.0%) | 40 | 8, 10, 7 | Range: 0 - 40 years |
| 30 | `TrainingTimesLastYear` | int64 | 0 (0.0%) | 7 | 0, 3, 2 | Range: 0 - 6 times |
| 31 | `WorkLifeBalance` | int64 | 0 (0.0%) | 4 | 1, 3, 2 | Likert scale (1: Bad, 4: Best) |
| 32 | `YearsAtCompany` | int64 | 0 (0.0%) | 37 | 6, 10, 0 | Range: 0 - 40 years |
| 33 | `YearsInCurrentRole` | int64 | 0 (0.0%) | 19 | 4, 7, 0 | Range: 0 - 18 years |
| 34 | `YearsSinceLastPromotion`| int64 | 0 (0.0%) | 16 | 0, 1, 3 | Range: 0 - 15 years |
| 35 | `YearsWithCurrManager` | int64 | 0 (0.0%) | 18 | 5, 7, 0 | Range: 0 - 17 years |

---

### 3.2 `Employee_Performance_Dataset.csv` (Large Performance Dataset)
* **Location:** Workspace Root
* **Shape:** 5,000 rows x 13 columns
* **Duplicate Rows:** 0 (0.0%)
* **Domain Entity:** Employee operational performance, KPI fulfillment, attendance, peer review, and manager feedback.
* **Primary Key Candidate:** `Employee ID` (int64, values range from 100,021 to 999,957, all 5,000 unique).

#### Column Breakdown & Schema

| # | Column Name | Dtype | Missing (Count / %) | Unique Count | Min / Mean / Max | Notes |
|---|---|---|---|---|---|---|
| 1 | `Employee ID` | int64 | 0 (0.0%) | 5000 | 100021 / 554223 / 999957 | Unique 6-digit Identifier |
| 2 | `Name` | object | 0 (0.0%) | 4863 | - | Employee Name |
| 3 | `Department` | object | 0 (0.0%) | 5 | - | Sales (1035), Finance (1016), HR (1010), IT (974), Marketing (965) |
| 4 | `Job Role` | object | 0 (0.0%) | 15 | - | 15 distinct job roles |
| 5 | `Performance Score` | int64 | 0 (0.0%) | 51 | 50 / 74.78 / 100 | Continuous score 50–100 |
| 6 | `KPI Score` | float64 | 0 (0.0%) | 2651 | 60.01 / 77.38 / 94.99 | KPI fulfillment % |
| 7 | `Attendance (%)` | float64 | 0 (0.0%) | 2172 | 75.01 / 87.47 / 100.0 | Attendance % |
| 8 | `Peer Rating` | float64 | 0 (0.0%) | 21 | 3.0 / 4.00 / 5.0 | Peer evaluation score |
| 9 | `Task Completion (%)` | float64 | 0 (0.0%) | 2448 | 70.01 / 84.98 / 100.0 | Task completion rate |
| 10 | `Work Hours Logged` | int64 | 0 (0.0%) | 21 | 35 / 44.93 / 55 | Weekly work hours |
| 11 | `Manager Feedback` | float64 | 0 (0.0%) | 21 | 3.0 / 4.00 / 5.0 | Manager rating |
| 12 | `Training Hours` | int64 | 0 (0.0%) | 31 | 0 / 14.88 / 30 | Hours in training |
| 13 | `Promotion Eligibility`| object | 0 (0.0%) | 2 | - | 'No': 4305 (86.1%), 'Yes': 695 (13.9%) |

---

### 3.3 `data/raw/employee_performance_pro.csv` (Granular Performance Dataset)
* **Location:** `data/raw/`
* **Shape:** 500 rows x 24 columns
* **Duplicate Rows:** 0 (0.0%)
* **Domain Entity:** Multi-country employee records with leave history, projects handled, satisfaction ratings, salary, and pre-labeled attrition risk.
* **Primary Key Candidate:** `EmployeeID` (int64, values range from 1 to 500, all 500 unique).

#### Column Breakdown & Schema

| # | Column Name | Dtype | Missing (Count / %) | Unique Count | Min / Mean / Max | Notes |
|---|---|---|---|---|---|---|
| 1 | `EmployeeID` | int64 | 0 (0.0%) | 500 | 1 / 250.5 / 500 | Primary Key |
| 2 | `Name` | object | 0 (0.0%) | 500 | - | Employee Name |
| 3 | `Gender` | object | 0 (0.0%) | 3 | - | 'Female' (186), 'Male' (165), 'Other' (149) |
| 4 | `Age` | int64 | 0 (0.0%) | 40 | 21 / 40.86 / 60 | Age in years |
| 5 | `Department` | object | 0 (0.0%) | 6 | - | Sales (99), IT (93), Support (82), Finance (77), HR (77), Marketing (72) |
| 6 | `JobRole` | object | 0 (0.0%) | 13 | - | 13 distinct roles |
| 7 | `EducationLevel` | int64 | 0 (0.0%) | 5 | 1 / 3.02 / 5 | Education level 1–5 |
| 8 | `JoiningDate` | object | 0 (0.0%) | 473 | - | Date string (e.g. '2016-05-05') |
| 9 | `CountryCode` | int64 | 0 (0.0%) | 5 | 1 / 37.02 / 91 | International dialing code |
| 10 | `Country` | object | 0 (0.0%) | 6 | - | Canada (92), India (90), UK (85), France (80), Germany (77), USA (76) |
| 11 | `PhoneNumber` | int64 | 0 (0.0%) | 500 | - | Employee Phone number |
| 12 | `MonthlySalary` | int64 | 0 (0.0%) | 498 | 30120 / 103678 / 179876 | Monthly salary |
| 13 | `OvertimeHoursPerMonth`| int64 | 0 (0.0%) | 41 | 0 / 20.04 / 40 | Overtime hours |
| 14 | `LeavesTaken` | int64 | 0 (0.0%) | 31 | 0 / 13.72 / 30 | Annual leaves taken |
| 15 | `LastLeaveDate` | object | 0 (0.0%) | 268 | - | Date string |
| 16 | `LeaveDayName` | object | 0 (0.0%) | 7 | - | Day of week |
| 17 | `ProjectsHandled` | int64 | 0 (0.0%) | 15 | 1 / 8.07 / 15 | Count of projects |
| 18 | `TrainingHours` | int64 | 0 (0.0%) | 76 | 5 / 43.04 / 80 | Training hours |
| 19 | `CustomerSatisfaction` | float64 | **319 (63.8%)** | 10 | 1.0 / 5.21 / 10.0 | Missing for non-customer roles |
| 20 | `LastPromotionYear` | int64 | 0 (0.0%) | 15 | 2010 / 2020.4 / 2024 | Year of last promotion |
| 21 | `YearsAtCompany` | int64 | 0 (0.0%) | 14 | 2 / 8.09 / 15 | Tenure |
| 22 | `WorkLifeBalanceScore`| float64 | 0 (0.0%) | 273 | -2.83 / 3.71 / 9.83 | Continuous score (includes negative values) |
| 23 | `PerformanceRating` | int64 | 0 (0.0%) | 5 | 1 / 3.26 / 5 | Rating 1–5 |
| 24 | `AttritionRisk` | object | 0 (0.0%) | 2 | - | Pre-assigned label ('No': 445 [89%], 'Yes': 55 [11%]) |

---

### 3.4 `data/raw/occupation_data.csv` (Role Master Taxonomy)
* **Location:** `data/raw/`
* **Shape:** 1,016 rows x 3 columns
* **Duplicate Rows:** 0 (0.0%)
* **Missing Values:** 0 in all columns (0.0%)
* **Domain Entity:** Standard O*NET Standard Occupational Classification (SOC) system defining occupation titles, formal SOC codes, and job descriptions.
* **Primary Key:** `O*NET-SOC Code` (1,016 unique string codes, e.g., '11-1011.00', '15-1252.00').
* **Columns:**
  1. `O*NET-SOC Code` (object, unique identifier)
  2. `Title` (object, 1,016 unique occupation names, e.g., 'Chief Executives', 'Software Developers', 'Data Scientists')
  3. `Description` (object, detailed job description)

---

### 3.5 `data/raw/essential_skills.csv` (Foundational Skills Taxonomy)
* **Location:** `data/raw/`
* **Shape:** 18,200 rows x 15 columns
* **Duplicate Rows:** 0 (0.0%)
* **Missing Values:** `Not Relevant` has 9,100 nulls (50.0%), corresponding exactly to rows where `Scale ID == 'IM'` (Importance rating).
* **Domain Entity:** Standard O*NET basic skill ratings (Reading Comprehension, Active Listening, Writing, Speaking, Mathematics, Science, Critical Thinking, Active Learning, Learning Strategies, Monitoring) across 910 SOC occupations.
* **Join Key to Occupations:** `O*NET-SOC Code`
* **Columns:** `O*NET-SOC Code`, `Title`, `Element ID`, `Element Name`, `Scale ID` ('IM' for Importance, 'LV' for Level), `Scale Name`, `Data Value` (float 0.0–6.0), `N` (8), `Standard Error`, `Lower CI Bound`, `Upper CI Bound`, `Recommend Suppress`, `Not Relevant`, `Date`, `Domain Source`.

---

### 3.6 `data/raw/software_skills.csv` (Technical & Software Skills Taxonomy)
* **Location:** `data/raw/`
* **Shape:** 31,821 rows x 7 columns
* **Duplicate Rows:** 0 (0.0%)
* **Missing Values:** 0 in all columns (0.0%)
* **Domain Entity:** O*NET technology skills repository mapping specific software products, programming languages, platforms, and tools to SOC occupations.
* **Join Key to Occupations:** `O*NET-SOC Code`
* **Columns:**
  1. `O*NET-SOC Code` (object, 923 unique SOC codes)
  2. `Title` (object, 923 unique occupation titles)
  3. `Workplace Example` (object, 8,753 unique software/tool names, e.g., 'Python', 'Apache Spark', 'Docker', 'Microsoft Excel', 'Salesforce')
  4. `Element ID` (object, 134 unique taxonomy element codes)
  5. `Element Name` (object, 134 categories, e.g., 'Development environment software', 'Analytical or scientific software')
  6. `Hot Technology` (object, 'Y': 11,571, 'N': 20,250)
  7. `In Demand` (object, 'Y': 2,425, 'N': 29,396)

---

## 4. Cross-Dataset Join Keys & Entity Verification

### 4.1 Verification of Employee Identifiers
We strictly tested whether similarly named ID columns represent the same entities:

| Table A | Table A Key | Table B | Table B Key | Overlap Count | Entity Alignment Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `WA_Fn-UseC_-HR-Employee-Attrition.csv` | `EmployeeNumber` (1–2068) | `Employee_Performance_Dataset.csv` | `Employee ID` (100021–999957) | **0 records** | **NO OVERLAP.** Disjoint ID spaces. |
| `WA_Fn-UseC_-HR-Employee-Attrition.csv` | `EmployeeNumber` (1–2068) | `employee_performance_pro.csv` | `EmployeeID` (1–500) | **377 numeric matches** | **FALSE OVERLAP.** Records with identical integer IDs are completely different individuals (e.g. ID 1 in Attrition is a 41yo Sales Executive; ID 1 in Perf Pro is a 57yo Auditor). |
| `Employee_Performance_Dataset.csv` | `Employee ID` (100021–999957) | `employee_performance_pro.csv` | `EmployeeID` (1–500) | **0 records** | **NO OVERLAP.** Disjoint ID spaces. |

> [!CAUTION]
> **Do NOT merge datasets by employee ID.** The employee tables come from distinct synthetic/benchmark generators and represent different populations.

---

### 4.2 Job Role Alignment to O*NET Taxonomy
We mapped the distinct `JobRole` categories from the employee datasets against the 1,016 O*NET occupations:

| Employee Dataset Job Role | Best O*NET SOC Match | O*NET Title |
| :--- | :--- | :--- |
| `Sales Executive` | `41-4012.00` | Sales Representatives, Wholesale and Manufacturing, Except Technical and Scientific Products |
| `Research Scientist` | `15-1221.00` | Computer and Information Research Scientists |
| `Laboratory Technician` | `29-2012.00` | Medical and Clinical Laboratory Technicians |
| `Manufacturing Director` | `11-1021.00` | General and Operations Managers |
| `Healthcare Representative`| `41-4011.00` | Sales Representatives, Wholesale and Manufacturing, Technical and Scientific Products |
| `Manager` | `11-1021.00` | General and Operations Managers |
| `Sales Representative` | `41-4012.00` | Sales Representatives, Wholesale and Manufacturing |
| `Research Director` | `11-9121.00` | Natural Sciences Managers |
| `Human Resources` | `13-1071.00` | Human Resources Specialists |
| `Software Engineer / Developer` | `15-1252.00` | Software Developers |
| `Data Analyst` | `15-2051.01` | Business Intelligence Analysts / Data Analysts |
| `Cybersecurity Specialist` | `15-1212.00` | Information Security Analysts |
| `Accountant` | `13-2011.00` | Accountants and Auditors |

---

## 5. Target Leakage & Predictive Governance Audit

### 5.1 Constant / Zero-Variance Columns
In `WA_Fn-UseC_-HR-Employee-Attrition.csv`, the following columns contain exactly one unique value across all 1,470 rows and must be dropped during preprocessing:
* `EmployeeCount` (constant = 1)
* `Over18` (constant = 'Y')
* `StandardHours` (constant = 80)

### 5.2 Target Leakage Verification
We computed Pearson correlation with `Attrition == Yes`:
* Strongest negative drivers: `TotalWorkingYears` (-0.171), `JobLevel` (-0.169), `YearsInCurrentRole` (-0.161), `MonthlyIncome` (-0.159), `Age` (-0.159), `YearsWithCurrManager` (-0.156).
* Strongest positive drivers: `OverTime == Yes` (+0.246), `DistanceFromHome` (+0.078).
* **Verdict:** There is **NO direct or indirect target leakage** (no "TerminationDate", "ExitInterviewScore", or post-hoc indicators). The dataset is clean for predictive ML modeling.

### 5.3 Sensitive Demographic Attributes (Governance Policy)
* `Gender` (Male / Female) and `MaritalStatus` (Single / Married / Divorced) are present.
* **Governance Rule:** In accordance with ethical HR AI standards, sensitive demographic attributes must be excluded from feature sets during production model training or used strictly for fairness/bias auditing.

---

## 6. Audit of Missing Information Required by Architecture

| Architecture Requirement | Current Workspace State | Impact on Project | Controlled Proposal for Approval |
| :--- | :--- | :--- | :--- |
| **1. Employee Current Skills** | **MISSING.** No CSV lists what skills individual employees possess. | Skill Gap Engine cannot compute Required - Current without a baseline. | Build a deterministic, controlled `data/processed/employee_skills_controlled.csv` derived strictly from O*NET taxonomy with fixed random seed (documented transparently as synthetic MVP). |
| **2. Learning Course Catalog** | **MISSING.** No course catalog table exists. | Recommendation engine cannot rank real courses for missing skills. | Construct a structured, high-quality course catalog `data/processed/course_catalog.csv` covering the major skill categories in O*NET. |
| **3. HR Policy Documents (RAG)** | **MISSING.** No policy PDFs/markdowns exist. | RAG retrieval pipeline has no document corpus to index and retrieve. | Create a grounded set of 6 authentic HR policy documents in `data/knowledge/` (Parental Leave, Remote Work, Performance Review, Tuition Assistance, Health Benefits, Code of Conduct). |
| **4. Raw Data Organization** | `WA_Fn-UseC_-HR-Employee-Attrition.csv` & `Employee_Performance_Dataset.csv` are in root. | Notebooks expect `data/raw/employee_attrition.csv` & `data/raw/hr_performance_engagement.csv`. | Copy/standardize raw files into `data/raw/` with standardized aliases without modifying originals. |

---

## 7. Recommended Next Steps

1. **Step 1:** Obtain User Approval on this Data Understanding Report and the proposed controlled solutions for missing components (Employee Skills, Course Catalog, HR Policy Corpus).
2. **Step 2:** Standardize `data/raw/` file paths.
3. **Step 3:** Execute **Phase 1 Data Foundation** (Notebooks `01_data_understanding.ipynb` through `04_data_relationships.ipynb`, outputting clean datasets in `data/processed/` and `docs/data_relationships.md`).
