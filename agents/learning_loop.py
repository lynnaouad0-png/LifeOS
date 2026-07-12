import os
import sys
from datetime import datetime, timezone

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.memory_service import MemoryService
from analytics.dashboard import AnalyticsDashboard

class LearningLoop:
    def __init__(self):
        """Initializes the evolutionary optimization engine."""
        print("🧠 Initializing LifeOS Learning Loop (Phase 14)...")
        self.memory = MemoryService()
        self.dashboard = AnalyticsDashboard()

    def run_daily_optimization(self, daily_metrics: dict) -> str:
        """
        Synthesizes performance data into a Policy Update to personalize 
        future system behavior.
        """
        print("🔄 Synthesizing performance trends...")
        
        # 1. Analyze trends
        goal_rate = daily_metrics.get("goal_rate", 0)
        habit_rate = daily_metrics.get("habits", [0])
        avg_habit = sum(habit_rate) / len(habit_rate)
        
        # 2. Determine System Policy
        policy = "STABLE"
        if goal_rate < 70 or avg_habit < 70:
            policy = "CONSERVATIVE_PLANNING"
        elif goal_rate > 90 and avg_habit > 90:
            policy = "AGGRESSIVE_EXPANSION"
            
        # 3. Create Narrative Insight
        insight = (
            f"Optimization Insight ({datetime.now(timezone.utc).strftime('%Y-%m-%d')}):\n"
            f"• Performance Profile: {policy}\n"
            f"• Logic: Goal Rate at {goal_rate}%, Avg Habit Compliance at {avg_habit}%.\n"
            f"• Action: Planner Agent configured to {'tighten' if policy == 'CONSERVATIVE_PLANNING' else 'scale'} task volume."
        )
        
        # 4. Save to Memory (so other agents read this 'Policy' tomorrow)
        self.memory.save_memory(
            user_id="SYSTEM_CORE",
            content=insight,
            source_category="system_optimization",
            metadata={"policy": policy}
        )
        
        print(f"✅ System optimized. Current Policy: {policy}")
        return insight

# --- LOCAL OPTIMIZATION SANITY CHECK RUNNER ---
if __name__ == "__main__":
    optimizer = LearningLoop()
    
    # Mock data snapshot
    mock_metrics = {
        "study": [4, 5],
        "coding": [6, 6],
        "habits": [95, 98],
        "goal_rate": 92
    }
    
    insight = optimizer.run_daily_optimization(mock_metrics)
    print("\n" + insight)