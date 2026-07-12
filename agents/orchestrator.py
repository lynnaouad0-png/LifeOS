import os
import sys
from datetime import datetime

# Ensure the root LifeOS directory is on the system path for clean cross-module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.memory_service import MemoryService

class AIOrchestrator:
    def __init__(self):
        """Initializes the main routing hub and wires up the unified Phase 5 Memory Engine."""
        print("🤖 Initializing AI Orchestrator Core...")
        self.memory_service = MemoryService()
        # FUTURE EXPANSION: Initialize your LLM connection interface here (OpenAI, Ollama, etc.)

    def route_request(self, user_id: str, prompt: str) -> dict:
        """
        Receives every incoming string request, handles contextual memory injection, 
        and dispatches the cargo payload to the correct specialized target agent.
        """
        print(f"\n📩 Incoming request caught: '{prompt}'")
        
        # 1. Retrieve related long-term semantic context embeddings from Qdrant
        print("🔍 Scanning vector space for contextual memory matches...")
        memories = self.memory_service.retrieve_relevant_memories(user_id, prompt, limit=2)
        
        # 2. Determine target module destination 
        intent = self._determine_intent(prompt)
        print(f"🎯 Orchestrator Routing Determination: [{intent.upper()}_AGENT]")
        
        # 3. Read context data matrices (Placeholders for database relations)
        context_payload = {
            "memories": memories,
            "calendar": [],
            "tasks": [],
            "habits": [],
            "goals": []
        }
        
        # 4. Populate intent-specific contextual blocks and delegate execution
        if intent == "planner":
            # Mock datasets mimicking reads from PostgreSQL/iCal services
            context_payload["calendar"] = ["10:00 AM - Microeconomics Revision Session", "4:00 PM - Violin Bowing Technique Practice"]
            context_payload["tasks"] = ["Debug PyCharm application backend loops", "Verify LinkedIn certification entries"]
            context_payload["habits"] = ["Track hydration tracking metrics", "Log evening reflection check"]
            context_payload["goals"] = ["Maintain high academic trajectory", "Build comprehensive algorithmic pipelines"]
            
            return self._call_planner_agent(prompt, context_payload)
            
        elif intent == "analytics":
            return self._call_analytics_agent(prompt, context_payload)
            
        else:
            return self._call_general_agent(prompt, context_payload)

    def _determine_intent(self, prompt: str) -> str:
        """Analyzes incoming strings to map intent directly to processing pipelines."""
        lowered_prompt = prompt.lower()
        if any(keyword in lowered_prompt for keyword in ["plan", "schedule", "day", "calendar", "task", "habit", "todo"]):
            return "planner"
        if any(keyword in lowered_prompt for keyword in ["analyze", "stats", "metrics", "progress", "charts", "graphs"]):
            return "analytics"
        return "general"

    def _call_planner_agent(self, prompt: str, context: dict) -> dict:
        """Compiles active context tables and triggers the specialized daily scheduling planner."""
        print("🗂️ Passing context matrices down to [Planner Agent] pipeline...")
        
        # Extract matches found by your semantic FastEmbed matching loop
        memory_strings = [m['content'] for m in context['memories']]
        memory_context = " | ".join(memory_strings) if memory_strings else "No closely related contextual memory anchors detected."
        
        response_data = (
            f"✨ LifeOS Consolidated Daily Plan ✨\n"
            f"--------------------------------------------------\n"
            f"🎯 Core Active Goals:\n" + "".join([f"  • {g}\n" for g in context['goals']]) + "\n"
            f"📅 Calendar Blocks:\n" + "".join([f"  • {c}\n" for c in context['calendar']]) + "\n"
            f"📝 Essential Backlog Tasks:\n" + "".join([f"  • {t}\n" for t in context['tasks']]) + "\n"
            f"🧠 Injected Semantic Memories:\n"
            f"  \"{memory_context}\"\n\n"
            f"💡 Orchestrator Suggestion:\n"
            f"  Prioritize your Python software debugging and academic review modules during peak morning slots. "
            f"  Transition smoothly into your classical repertoire sessions (Bach/Sibelius) during your evening wind-down window."
        )
        return {"agent": "PlannerAgent", "status": "success", "output": response_data}

    def _call_analytics_agent(self, prompt: str, context: dict) -> dict:
        return {"agent": "AnalyticsAgent", "status": "success", "output": "Analytics processing dashboard active."}

    def _call_general_agent(self, prompt: str, context: dict) -> dict:
        return {"agent": "GeneralAgent", "status": "success", "output": "General request answered cleanly via basic fallback context."}


# --- LOCAL ORCHESTRATION SANITY CHECK RUNNER ---
if __name__ == "__main__":
    print("🚀 Initializing standalone AI Orchestrator test run...")
    mock_user = "b2156f03-4753-484e-abad-ced4371ebfb5"
    
    # Initialize the hub
    orchestrator_hub = AIOrchestrator()
    
    # Test Request Execution
    test_query = "Plan my day."
    execution_result = orchestrator_hub.route_request(user_id=mock_user, prompt=test_query)
    
    print("\n==================== CONSOLIDATED AGENT RESPONSE ====================")
    print(execution_result["output"])
    print("======================================================================\n")