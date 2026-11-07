"""
Central AI Brain for MARK 12
Orchestrates context, intents, models, memory retrieval, and agent delegation.
"""
from typing import Dict, Any, Optional, List
from core.command_parser import global_command_parser
from core.intent_classifier import global_intent_classifier
from core.context_manager import global_context
from ai_engine.memory.memory_retriever import global_memory_retriever
from ai_engine.memory.long_term import global_long_term_memory
from ai_engine.llm.model_manager import global_model_manager
from agents.agent_manager import global_agent_manager
from automation.app_controller import global_app_controller
from automation.browser_controller import global_browser_controller
from automation.system_monitor import global_system_monitor
from automation.keyboard_mouse import global_input_controller
from task_manager.task_service import global_task_service
from database.repository import Repository

class AIBrain:
    def process_input(self, user_text: str, conv_id: str = "default", enable_voice: bool = False) -> Dict[str, Any]:
        # 1. Check for duplicate command within time window (Set data structure)
        if global_context.is_duplicate_command(user_text):
            return {
                "response": "Duplicate command ignored to prevent redundant execution.",
                "intent": "duplicate_suppressed",
                "agent_used": "safety"
            }

        # 2. Add to sequential List history
        global_context.add_message("user", user_text)
        Repository.add_message(conv_id, "user", user_text)

        # 3. Fast Dictionary Command Dispatch
        cmd_intent, cmd_target = global_command_parser.parse(user_text)

        if cmd_intent == "automation_launch" and cmd_target:
            res = global_app_controller.launch_app(cmd_target)
            reply = res["message"]
            return self._finalize(conv_id, reply, "automation", "Automation", enable_voice)

        elif cmd_intent == "browser_search" and cmd_target:
            res = global_browser_controller.search_web(cmd_target)
            reply = res["message"]
            return self._finalize(conv_id, reply, "browser", "Automation", enable_voice)

        elif cmd_intent == "automation_screenshot":
            res = global_input_controller.take_screenshot()
            reply = "Screenshot captured and saved to visual telemetry store." if res.get("success") else "Failed to capture screenshot."
            return self._finalize(conv_id, reply, "screenshot", "Automation", enable_voice, extra={"screenshot": res.get("relative_url")})

        elif cmd_intent == "system_telemetry":
            stats = global_system_monitor.get_system_telemetry()
            reply = (
                f"MARK 12 Telemetry: OS: {stats['os']} | CPU: {stats['cpu_percent']}% | "
                f"Memory: {stats['memory_percent']}% | Status: {stats['status']}"
            )
            return self._finalize(conv_id, reply, "system_telemetry", "Automation", enable_voice, extra={"telemetry": stats})

        elif cmd_intent == "memory_save" and cmd_target:
            mem_id = global_long_term_memory.remember(cmd_target, category="user_fact", importance=4)
            reply = f"Noted, sir. I have committed this to long-term memory: '{cmd_target}'."
            return self._finalize(conv_id, reply, "memory_save", "Memory", enable_voice)

        elif cmd_intent == "task_create" and cmd_target:
            task = global_task_service.create_task(title=cmd_target, priority=2)
            reply = f"Task registered in priority queue: '{cmd_target}' (Priority: 2 - High)."
            return self._finalize(conv_id, reply, "task_create", "TaskManager", enable_voice)

        elif cmd_intent == "system_undo":
            undo_res = global_context.execute_undo()
            return self._finalize(conv_id, undo_res["message"], "undo", "Safety", enable_voice)

        # 4. Multi-Agent Classification & Execution
        intent = global_intent_classifier.classify(user_text)

        if intent == "multi_agent_workflow":
            workflow_res = global_agent_manager.execute_multi_agent_workflow(user_text)
            reply = f"{workflow_res['final_summary']}\n\nKey execution outputs have been aggregated across the agent graph."
            return self._finalize(
                conv_id,
                reply,
                "multi_agent_workflow",
                "Planner",
                enable_voice,
                extra={"plan_steps": workflow_res["plan_steps"], "execution_log": workflow_res["execution_log"]}
            )

        # 5. Hybrid Memory Retrieval & LLM Generation
        memory_context = global_memory_retriever.retrieve_relevant_context(user_text)
        augmented_prompt = f"{memory_context}\n\nUser Request: {user_text}"
        llm_reply = global_model_manager.generate_response(augmented_prompt)

        return self._finalize(conv_id, llm_reply, intent, "Brain", enable_voice)

    def _finalize(self, conv_id: str, reply: str, intent: str, agent: str, enable_voice: bool, extra: Dict[str, Any] = None) -> Dict[str, Any]:
        global_context.add_message("assistant", reply, intent=intent, agent=agent)
        Repository.add_message(conv_id, "assistant", reply, intent=intent, agent=agent)

        audio_url = None
        if enable_voice:
            from ai_engine.speech.text_to_speech import global_tts
            from core.personality import global_personality
            spoken_text = global_personality.format_speech(reply)
            audio_url = global_tts.synthesize(spoken_text)

        result = {
            "response": reply,
            "conversation_id": conv_id,
            "intent": intent,
            "agent_used": agent,
            "audio_url": audio_url
        }
        if extra:
            result.update(extra)
        return result

global_brain = AIBrain()
