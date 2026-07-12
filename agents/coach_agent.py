import os
import sys

class CoachAgent:
    def __init__(self):
        """Initializes the dedicated lifestyle assessment and high-performance coaching engine."""
        print("🧠 Initializing AI Coach Agent Core...")

    def generate_coaching_feedback(
        self, 
        habits: dict, 
        productivity_score: int, 
        missed_goals: list, 
        consistency_metrics: dict
    ) -> str:
        """
        Analyzes personal habit completion, productivity outputs, missed targets, 
        and routine consistency to generate customized coaching feedback.
        """
        feedback = []
        feedback.append("=== LIFEOS SYSTEMIC COACHING INSIGHTS ===")
        
        # 1. Evaluate Overall Productivity Metric
        feedback.append(f"📊 Macro Productivity Index: {productivity_score}/100")
        if productivity_score >= 80:
            feedback.append("  • Performance Status: High-velocity execution phase. Momentum is stable.")
        elif productivity_score >= 60:
            feedback.append("  • Performance Status: Standard operational output. Room for calendar optimization.")
        else:
            feedback.append("  • Performance Status: Velocity slip detected. Intervention recommended.")
        feedback.append("")

        # 2. Analyze Routine Habit Tracks
        feedback.append("🌱 Habit Loop Analytics:")
        low_habits = []
        for habit, completion in habits.items():
            feedback.append(f"  • {habit}: {completion}% completion rate")
            if completion < 75:
                low_habits.append(habit)
        if low_habits:
            feedback.append(f"  ⚠️ Actionable Coaching Notice: Friction detected in habit loops: {', '.join(low_habits)}.")
        feedback.append("")

        # 3. Post-Mortem on Missed Goals
        feedback.append("🎯 Missed Milestones & Friction Review:")
        if missed_goals:
            for goal in missed_goals:
                feedback.append(f"  • [Missed] {goal}")
            feedback.append("  💡 Tactical Correction: Break these items down into smaller sub-tasks for tomorrow's planner agent.")
        else:
            feedback.append("  • Clean sweep! All core goals hit successfully.")
        feedback.append("")

        # 4. Consistency Architecture Synthesis
        feedback.append("⚡ Routine Consistency Audit:")
        for block, metric in consistency_metrics.items():
            feedback.append(f"  • {block}: {metric}")
            
        # 5. Strategic Conclusion Blueprint
        feedback.append("\n💡 Strategic Coaching Directives:")
        if missed_goals or low_habits:
            feedback.append(
                "  1. Protect your deep-work focus windows early in the day to minimize task slippage.\n"
                "  2. Anchor lower-compliance habits right next to pre-established high-compliance calendar events."
            )
        else:
            feedback.append("  1. Velocity is optimal. Focus on maintaining baseline energy states to avoid burnout cascades.")
            
        feedback.append("\n=========================================")
        return "\n".join(feedback)


# --- LOCAL COACHING SANITY CHECK RUNNER ---
if __name__ == "__main__":
    coach = CoachAgent()
    
    # Mock data matrices tracking active personal habits and project tracks
    mock_habits = {
        "Hydration Tracking Metrics": 92,
        "Evening Reflection Log": 60
    }
    
    mock_productivity = 84
    
    mock_missed_goals = [
        "Deploy automated local testing infrastructure for AI trading bot codebase"
    ]
    
    mock_consistency = {
        "Python Application Development Blocks": "4 out of 5 days targeted",
        "Violin Repertoire Rehearsal Windows": "3 out of 5 days targeted"
    }
    
    # Run performance analytics engine
    coaching_report = coach.generate_coaching_feedback(
        habits=mock_habits,
        productivity_score=mock_productivity,
        missed_goals=mock_missed_goals,
        consistency_metrics=mock_consistency
    )
    
    print("\n" + coaching_report)