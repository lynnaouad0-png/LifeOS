import os
import sys
from datetime import datetime, timezone

# Ensure the root LifeOS directory is on the system path for clean cross-module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.memory_service import MemoryService

class ReflectionAgent:
    def __init__(self):
        """Initializes the dedicated nightly closure and memory sync engine."""
        print("📝 Initializing Reflection Agent Core...")
        self.memory_service = MemoryService()

    def process_nightly_reflection(
        self, 
        user_id: str, 
        accomplishments: str, 
        distractions: str, 
        improvements: str
    ) -> dict:
        """
        Gathers nightly check-in logs, structures them into a comprehensive daily narrative, 
        and updates the Qdrant long-term vector brain index.
        """
        # Fixed the deprecation warning using a modern, timezone-aware UTC datetime object
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        print(f"\n🌙 Processing Evening Review Log for timestamp: {timestamp}")
        
        # 1. Compile the narrative baseline
        consolidated_narrative = (
            f"Daily Reflection Summary ({timestamp}):\n"
            f"• Accomplished: {accomplishments}\n"
            f"• Distractions/Friction: {distractions}\n"
            f"• Action Plan for Tomorrow: {improvements}"
        )
        
        # 2. Update the long-term semantic memory database cluster
        print("🧠 Injecting daily narrative insights into Qdrant Vector Space...")
        memory_uuid = self.memory_service.save_memory(
            user_id=user_id,
            content=consolidated_narrative,
            source_category="nightly_reflection",
            metadata={"date_logged": timestamp}
        )
        
        print(f"✅ Memory index successfully updated. Vector ID: {memory_uuid}")
        
        return {
            "status": "success",
            "memory_id": memory_uuid,
            "logged_entry": consolidated_narrative
        }


# --- LOCAL REFLECTION SANITY CHECK RUNNER ---
if __name__ == "__main__":
    reflection_engine = ReflectionAgent()
    mock_user = "b2156f03-4753-484e-abad-ced4371ebfb5"
    
    # Simulating authentic lifestyle tracking inputs
    user_accomplishments = "Idled microeconomics curriculum review phase and pushed AI Orchestrator backend to GitHub."
    user_distractions = "Spent too much time adjusting styling options in PyCharm before starting deep-work modules."
    user_improvements = "Will block all notification profiles and initialize the Python code deep-dive by 9:00 AM sharp."
    
    # Execute the processing pipeline
    reflection_result = reflection_engine.process_nightly_reflection(
        user_id=mock_user,
        accomplishments=user_accomplishments,
        distractions=user_distractions,
        improvements=user_improvements
    )
    
    print("\n==================== RECORDED NARRATIVE LOG ====================")
    print(reflection_result["logged_entry"])
    print("================================================================\n")