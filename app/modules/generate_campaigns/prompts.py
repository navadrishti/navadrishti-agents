SCHEDULE_VII = """
Schedule VII Categories (Companies Act 2013):
i   - Hunger, poverty, malnutrition, health, sanitation
ii  - Education, vocational skills, livelihood
iii - Gender equality, women empowerment
iv  - Environment, ecology, conservation
v   - National heritage, art, culture
vi  - Armed forces veterans
vii - Rural/Olympic/Paralympic sports
viii- Technology incubators
ix  - Rural development
x   - Slum development
xi  - Disaster management
xii - Other (PM Relief Fund)
"""

def generate_campaigns_prompt(preferences: dict) -> str:
    budget = preferences.get('budget')
    category = preferences.get('category')
    location = preferences.get('location')
    timeline_start = preferences.get('timeline_start')
    timeline_end = preferences.get('timeline_end')
    milestone_count = preferences.get('milestones')
    milestone_info = preferences.get('milestone_info')

    return f"""
You are a CSR strategy expert helping Indian companies design practical, real-world CSR campaign drafts.

The goal is to generate **80% complete, realistic campaign drafts** that companies can refine further.

{SCHEDULE_VII}

-----------------------------------
COMPANY REQUIREMENTS
-----------------------------------
- Budget: ₹{budget}
- Category: {category}
- Location: {location}
- Start Date: {timeline_start}
- End Date: {timeline_end}
- Timeline: {timeline_start} to {timeline_end}
- Milestones: {milestone_count}
- user defined Milestone Details: {milestone_info}

-----------------------------------
REAL-WORLD RULES
-----------------------------------

1. **Budget Consistency**
- Total of milestone budgets should match total budget (or very close)
- budgetBreakdown should roughly align with milestone budgets

2. **Timeline Consistency**
- Distribute timeline logically across milestones
- Sum of milestone.duration_weeks ≈ total timeline

3. **Execution Realism**
Each campaign must explain:
- how beneficiaries are identified
- how delivery happens (NGO, camps, infrastructure, etc.)
- actual ground execution steps in {location}

4. **Milestone Enhancement**
For each milestone:
- add realistic description
- assign duration_weeks
- define clear deliverables

5. **Diversity**
All 3 campaigns MUST differ in approach:
- one infrastructure-based
- one training/service-based
- one distribution-based

-----------------------------------
STRICT RULES
-----------------------------------
- scheduleVII must align with category
- beneficiaries must be integer
- Output MUST be valid JSON
- NO markdown, NO extra text

-----------------------------------
OUTPUT FORMAT
-----------------------------------

{{
  "campaigns": [
    {{
      "title": "string",

      "description": "clear explanation of how the campaign will be executed in {location}",
      "category": "{category}",   
      "location": "{location}",
      "budget_inr": {budget},

      "budget_breakdown": {{
        "infrastructure": 0,
        "training": 0,
        "materials": 0,
        "monitoring": 0,
        "contingency": 0
      }},

      "schedule_vii": "one of the categories",

      "sdg_alignment": [1, 4],
      "start_date": "{timeline_start}",
      "end_date": "{timeline_end}",
      "impact_metrics": {{
        "beneficiaries": 0,
        "duration": "{timeline_start} to {timeline_end}"
      }},

      "milestones": [
        {{
          "title": "string",
          "description": "specific execution step",
          "duration_weeks": 0,
          "budget_allocated": 0,
          "deliverables": ["clear outputs"]
        }}
      ]
    }}
  ]
}}
"""


'''def generate_campaigns_prompt(preferences: dict) -> str:
    budget = preferences.get('budget')
    category = preferences.get('category')
    location = preferences.get('location')
    timeline_start = preferences.get('timeline_start')
    timeline_end = preferences.get('timeline_end')
    milestone = preferences.get('milestones')
    return f"""You are an expert CSR strategist helping Indian companies design impactful CSR campaigns aligned with Schedule VII of the Companies Act 2013.
    {SCHEDULE_VII}
    budget: ₹{budget} INR
    category: {category}
    location: {location}
    timeline: {timeline_start} to {timeline_end}
    milestones: {milestone}


    Generate exactly 3 distinct CSR campaign concepts based on these preferences.

    STRICT RULES:
    - Each campaign MUST be aligned with a Schedule VII category
    - estimated_budget MUST be ≤ ₹{budget}
    - budget_breakdown values MUST sum exactly to estimated_budget
    - All 3 campaigns MUST be meaningfully different from each other
    - expected_beneficiaries MUST be an integer only — no text, no units
    - Return ONLY valid JSON — no markdown, no extra text

    Return ONLY this JSON:
    {{
    "campaigns": [
        {{
        "title": "string",
        "description": "description about the offers, approach and goal of this campaign",
        "budgetBreakdown": {{
            "infrastructure": 50000,
            "training": 40000,
            "materials": 35000,
            "monitoring": 15000,
            "contingency": 10000
        }},
        "scheduleVII": "e.g. Education",
        "sdgAlignment": [4, 8],
        "impactMetrics": {{
            "beneficiaries": 100,
            "duration": "{timeline_start} to {timeline_end}"
        }},
        "milestones": [
            {{
            "title": "Setup & Onboarding",
            "description": "Identify beneficiaries, set up required infrastructure",
            "duration_weeks": 2,
            "budget_allocated": 20000,
            "deliverables": [
                "Beneficiary list finalized",
                "Infrastructure ready"
            ]
            }},
            {{
            "title": "Phase 1 - Implementation",
            "description": "Begin core program activities with first batch",
            "duration_weeks": 8,
            "budget_allocated": 80000,
            "deliverables": [
                "First batch completed",
                "Progress report submitted"
            ]
            }},
            {{
            "title": "Phase 2 - Completion",
            "description": "Complete remaining activities and document impact",
            "duration_weeks": 14,
            "budget_allocated": 50000,
            "deliverables": [
                "All beneficiaries covered",
                "Final impact report ready"
            ]
            }}
        ]
        }}
    ]
    }}"""
'''