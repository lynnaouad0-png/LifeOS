import os
import sys

class PlannerAgent:
    def __init__(self):
        """Initializes the dedicated daily schedule optimization agent."""
        print("📅 Initializing Planner Agent Core...")

    def build_today_schedule(
        self, 
        goals: list, 
        calendar: list, 
        habits: list, 
        deadlines: list, 
        task_durations: dict, 
        energy_level: str
    ) -> str:
        """
        Generates a structured daily itinerary based strictly on the six required parameters:
        Goals, Calendar, Habits, Deadlines, Task Durations, and Energy Level.
        """
        schedule_output = []
        schedule_output.append(f"=== LIFEOS DAILY SCHEDULE ARCHITECTURE ===")
        schedule_output.append(f"State of Capacity: [{energy_level.upper()} ENERGY]\n")
        
        # 1. Align Focus Goals
        schedule_output.append("🎯 Active Alignment Goals:")
        for goal in goals:
            schedule_output.append(f"  • {goal}")
        schedule_output.append("")

        # 2. Map Fixed Commitments (Calendar)
        schedule_output.append("🔒 Fixed Time-Block Commitments (Calendar):")
        if calendar:
            for item in calendar:
                schedule_output.append(f"  • {item}")
        else:
            schedule_output.append("  • No fixed external calendar items.")
        schedule_output.append("")

        # 3. Process Backlog Tasks by Priority, Urgency, and Durations
        schedule_output.append("⚡ Dynamic Task Allocations:")
        
        # Sort tasks based on urgency/deadline metrics supplied
        sorted_deadlines = sorted(deadlines, key=lambda x: x.get('urgency_score', 1), reverse=True)
        
        for task_entry in sorted_deadlines:
            task_name = task_entry.get('name')
            due_date = task_entry.get('due')
            duration = task_durations.get(task_name, "Duration unmapped")
            
            # Simple energy-matching heuristic logic
            if energy_level.lower() == "high":
                allocation_window = "Deep-Work Core Focus Window"
            elif energy_level.lower() == "medium":
                allocation_window = "Standard Processing Block"
            else:
                allocation_window = "Low-Intensity / Fragmented Block"
                
            schedule_output.append(
                f"  • [Task] {task_name}\n"
                f"    Estimated Time: {duration} | Target Deadline: {due_date}\n"
                f"    Allocation Priority: {allocation_window}"
            )
        schedule_output.append("")

        # 4. Inject Routine Habits
        schedule_output.append("🌱 Habit Loop Integrations:")
        if habits:
            for habit in habits:
                schedule_output.append(f"  • [Habit] {habit}")
        else:
            schedule_output.append("  • No habit items queued.")
            
        schedule_output.append("\n==========================================")
        return "\n".join(schedule_output)


# --- LOCAL AGENT SANITY CHECK RUNNER ---
if __name__ == "__main__":
    planner = PlannerAgent()
    
    # Mock parameters matching active routine metrics for engineering validation
    mock_goals = ["Maintain high academic trajectory", "Build comprehensive algorithmic pipelines"]
    mock_calendar = ["10:00 AM - Microeconomics Revision Session", "4:00 PM - Violin Bowing Technique Practice"]
    mock_habits = ["Track hydration metrics", "Log evening reflection check"]
    
    mock_deadlines = [
        {"name": "Debug PyCharm application backend loops", "due": "Tonight", "urgency_score": 3},
        {"name": "Verify LinkedIn certification entries", "due": "End of week", "urgency_score": 1}
    ]
    
    mock_durations = {
        "Debug PyCharm application backend loops": "2 hours",
        "Verify LinkedIn certification entries": "30 mins"
    }
    
    mock_energy = "high"
    
    # Execute structural layout engine
    result_schedule = planner.build_today_schedule(
        goals=mock_goals,
        calendar=mock_calendar,
        habits=mock_habits,
        deadlines=mock_deadlines,
        task_durations=mock_durations,
        energy_level=mock_energy
    )
    
    print("\n" + result_schedule)