import os
import sys

class AnalyticsDashboard:
    def __init__(self):
        """Initializes the performance monitoring and visualization engine."""
        print("📊 Initializing LifeOS Analytics Dashboard...")

    def generate_weekly_report(self, data: dict) -> str:
        """
        Processes raw metric dictionaries and generates a visual performance dashboard.
        Expected keys: study, coding, sleep, habits, goal_rate, focus_score, focus_time.
        """
        # Calculate summary statistics
        total_study = sum(data.get("study", []))
        total_coding = sum(data.get("coding", []))
        
        # Avoid division by zero by providing defaults if lists are empty
        sleep_data = data.get("sleep", [0])
        avg_sleep = sum(sleep_data) / len(sleep_data) if sleep_data else 0
        
        habit_data = data.get("habits", [0])
        avg_habit = round(sum(habit_data) / len(habit_data), 1) if habit_data else 0
        
        focus_scores = data.get("focus_score", [0])
        avg_focus = round(sum(focus_scores) / len(focus_scores), 1) if focus_scores else 0

        report = []
        report.append("=== LIFEOS WEEKLY ANALYTICS DASHBOARD ===")
        report.append(f"📅 Reporting Period: Last 7 Days\n")
        
        report.append("📈 Productivity Metrics:")
        report.append(f"  • Study Hours: {total_study} hrs")
        report.append(f"  • Coding Hours: {total_coding} hrs")
        report.append(f"  • Average Focus Score: {avg_focus}/10")
        report.append("")
        
        report.append("🔋 Wellness & Habits:")
        report.append(f"  • Average Sleep: {round(avg_sleep, 1)} hrs/night")
        report.append(f"  • Habit Completion Rate: {avg_habit}%")
        report.append("")
        
        report.append("🎯 Objective Alignment:")
        report.append(f"  • Goal Completion Rate: {data.get('goal_rate', 0)}%")
        report.append("")
        
        report.append("💡 Insights:")
        if avg_sleep < 7:
            report.append("  ⚠️ Sleep deficit detected. Impacting recovery metrics.")
        if total_coding > total_study:
            report.append("  🚀 Coding velocity is currently outpacing theoretical study.")
            
        report.append("==========================================")
        return "\n".join(report)

# --- LOCAL ANALYTICS SANITY CHECK RUNNER ---
if __name__ == "__main__":
    dashboard = AnalyticsDashboard()
    
    # Mock data snapshot for the current week
    mock_data = {
        "study": [3, 4, 2, 5, 3, 4, 2],
        "coding": [5, 4, 6, 4, 5, 5, 6],
        "sleep": [6.5, 7, 7.5, 6, 7, 7.5, 8],
        "habits": [85, 90, 80, 95, 88, 92, 90],
        "focus_score": [7, 8, 9, 7, 8, 9, 8],
        "goal_rate": 75,
        "focus_time": [240, 300, 210, 330, 240, 300, 270]
    }
    
    print("\n" + dashboard.generate_weekly_report(mock_data))