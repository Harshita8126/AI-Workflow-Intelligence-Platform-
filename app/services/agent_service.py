import os
import pandas as pd
from app.utils.config import DATA_PROCESSED
from app.services.skill_gap_service import get_employee_by_id
from app.services.rag_service import HRPolicyRAGEngine
from app.utils.logger import app_logger

# ---------------- Governed Tools ----------------
def tool_get_employee_profile(employee_id: int):
    return get_employee_by_id(employee_id)

def tool_get_role_requirements(target_role: str):
    profiles_path = os.path.join(DATA_PROCESSED, "role_competency_profiles.csv")
    df = pd.read_csv(profiles_path)
    match = df[df['job_role'].str.lower() == target_role.lower()]
    if match.empty:
        # Fallback closest match
        match = df[df['job_role'].str.contains(target_role, case=False, na=False)]
    if match.empty:
        return []
    return match.iloc[0]['required_skills_list'].split('|')

def tool_calculate_skill_gap(current_skills: list, target_role_skills: list):
    current_set = set(current_skills)
    target_set = set(target_role_skills)
    missing = target_set - current_set
    matched = target_set.intersection(current_set)
    readiness = (len(matched) / len(target_set) * 100) if target_set else 100.0
    return {
        "missing_skills": sorted(list(missing)),
        "matched_skills": sorted(list(matched)),
        "readiness_pct": round(readiness, 2)
    }

def tool_recommend_courses(missing_skills: list):
    catalog_path = os.path.join(DATA_PROCESSED, "course_catalog.csv")
    df = pd.read_csv(catalog_path)
    recommended = []
    for skill in missing_skills:
        for _, c in df.iterrows():
            if skill.lower() in c['target_skills'].lower():
                recommended.append(f"{c['course_title']} ({c['course_id']})")
                break
    return list(dict.fromkeys(recommended))[:3]

# ---------------- Governed Multi-Agent Orchestrator ----------------
def orchestrate_career_upskilling_agent(employee_id: int, target_role: str, user_goal: str):
    app_logger.info(f"Governed Agent Workflow triggered: EmpID={employee_id} -> TargetRole={target_role}")
    trace = []
    
    # Step 1: Governed Profile Access
    profile = tool_get_employee_profile(employee_id)
    if not profile:
        return {
            "employee_id": employee_id,
            "target_role": target_role,
            "current_readiness": 0.0,
            "skill_gap_count": 0,
            "missing_skills": [],
            "recommended_courses": [],
            "execution_trace": [{"step": 1, "tool": "get_employee_profile", "status": "FAILED: Employee Not Found"}],
            "governance_status": "DENIED / INVALID IDENTIFIER"
        }
    
    trace.append({
        "step": 1,
        "tool": "get_employee_profile()",
        "output": f"Retrieved profile for {profile['job_role']} (Dept: {profile['department']}, Risk: {profile['attrition_risk_level']})"
    })
    
    # Step 2: Resolve Target Role Competency Requirements
    actual_target = target_role if target_role else profile['job_role']
    required_skills = tool_get_role_requirements(actual_target)
    trace.append({
        "step": 2,
        "tool": "get_role_requirements()",
        "output": f"Resolved {len(required_skills)} O*NET competency benchmarks for '{actual_target}'"
    })
    
    # Step 3: Calculate Skill Gap & Readiness
    gap_result = tool_calculate_skill_gap(profile['current_skills'], required_skills)
    trace.append({
        "step": 3,
        "tool": "calculate_skill_gap()",
        "output": f"Computed {len(gap_result['missing_skills'])} missing competencies | Career Readiness: {gap_result['readiness_pct']}%"
    })
    
    # Step 4: Recommend Courses
    courses = tool_recommend_courses(gap_result['missing_skills'])
    trace.append({
        "step": 4,
        "tool": "recommend_courses()",
        "output": f"Ranked {len(courses)} high-priority learning paths from enterprise catalog"
    })
    
    return {
        "employee_id": employee_id,
        "target_role": actual_target,
        "current_readiness": gap_result['readiness_pct'],
        "skill_gap_count": len(gap_result['missing_skills']),
        "missing_skills": gap_result['missing_skills'],
        "recommended_courses": courses,
        "execution_trace": trace,
        "governance_status": "AUTHORIZED & COMPLETED"
    }
