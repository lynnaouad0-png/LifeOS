import os
import sys

class DecisionAgent:
    def __init__(self):
        """Initializes the strategic decision-making support engine."""
        print("⚖️ Initializing AI Decision Agent Core...")

    def get_recommendation(
        self, 
        current_goal: str, 
        goals: list, 
        calendar: list, 
        skills: list, 
        past_decisions: list
    ) -> str:
        """
        Analyzes constraints, capabilities, and historical outcomes to output
        a data-driven recommendation for a specific choice or direction.
        """
        print(f"\n🧠 Decision Agent analyzing recommendation for: '{current_goal}'")
        
        # 1. Logic Gate: Skill Gap Analysis
        # Check if the goal requires skills present in user's profile
        is_skilled = any(skill.lower() in current_goal.lower() for skill in skills)
        
        # 2. Logic Gate: Calendar Conflict
        # Simple heuristic check for time pressure
        has_conflicts = len(calendar) > 5
        
        # 3. Logic Gate: Historical Precedent
        # Check if similar past decisions were successful
        similar_past = [d for d in past_decisions if any(word in d['choice'] for word in current_goal.split())]
        past_success_rate = sum(d['outcome'] == 'success' for d in similar_past) / len(similar_past) if similar_past else 0.5
        
        # 4. Formulate Recommendation
        recommendation = []
        recommendation.append("=== DECISION AGENT REPORT ===")
        
        if is_skilled and past_success_rate >= 0.5:
            recommendation.append(f"✅ Recommendation: PROCEED with '{current_goal}'.")
            recommendation.append("  Reasoning: Skills are aligned and historical outcomes suggest positive trajectory.")
        elif not is_skilled:
            recommendation.append(f"⚠️ Recommendation: CAUTION/UPSKILLING REQUIRED.")
            recommendation.append(f"  Reasoning: The goal '{current_goal}' requires competencies outside your currently listed skill set.")
        else:
            recommendation.append(f"📉 Recommendation: RE-EVALUATE.")
            recommendation.append("  Reasoning: Low confidence in historical success rates for this category.")
            
        if has_conflicts:
            recommendation.append("\n  [Note]: Your calendar is currently high-density. Consider offloading non-critical tasks.")
            
        recommendation.append("\n=============================")
        return "\n".join(recommendation)


# --- LOCAL DECISION SANITY CHECK RUNNER ---
if __name__ == "__main__":
    decision_engine = DecisionAgent()
    
    # Mock parameters representing current state
    user_goals = ["Build AI Trading Bot", "Complete Microeconomics"]
    user_calendar = ["10:00 AM - Revision", "4:00 PM - Violin", "7:00 PM - Coding"]
    user_skills = ["Python", "Statistics", "Accounting"]
    user_past_decisions = [
        {"choice": "Build AI Trading Bot", "outcome": "success"},
        {"choice": "Learn violin", "outcome": "success"}
    ]
    
    # Analyze a hypothetical new decision
    decision = decision_engine.get_recommendation(
        current_goal="Build AI Trading Bot",
        goals=user_goals,
        calendar=user_calendar,
        skills=user_skills,
        past_decisions=user_past_decisions
    )
    
    print(decision)