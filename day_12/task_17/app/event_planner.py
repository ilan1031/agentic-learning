from app.agents import create_user_proxy_agent, create_event_processing_agent, create_progress_summarization_agent
import autogen
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventPlanner:
    def __init__(self):
        self.user_proxy = create_user_proxy_agent()
        self.event_processor = create_event_processing_agent()
        self.progress_summarizer = create_progress_summarization_agent()
        
        # Create group chat
        self.groupchat = autogen.GroupChat(
            agents=[self.user_proxy, self.event_processor, self.progress_summarizer],
            messages=[],
            max_round=10
        )
        
        # Create group chat manager
        self.manager = autogen.GroupChatManager(
            groupchat=self.groupchat,
            llm_config={"config_list": [{"model": "gemini-1.5-flash"}]}
        )
        
        # Initialize state
        self.event_details = {}
        self.task_list = []
        self.progress_report = ""
        self.timeline = []
    
    def plan_event(self, event_details: str):
        """Initiate event planning process"""
        try:
            self.event_details = self._parse_event_details(event_details)
            
            # Initiate conversation
            self.user_proxy.initiate_chat(
                self.manager,
                message=f"Plan this event: {event_details}"
            )
            
            # Extract results from conversation
            self._extract_results()
            
            return {
                "event_details": self.event_details,
                "task_list": self.task_list,
                "progress_report": self.progress_report,
                "timeline": self.timeline
            }
        except Exception as e:
            logger.error(f"Event planning failed: {str(e)}")
            return {
                "error": str(e),
                "event_details": {},
                "task_list": [],
                "progress_report": "",
                "timeline": []
            }
    
    def _parse_event_details(self, event_details: str) -> dict:
        """Parse event details into structured format"""
        # In a real implementation, this would use NLP to extract details
        return {
            "event_type": "Corporate Seminar" if "seminar" in event_details.lower() else "Wedding",
            "location": "Chennai" if "Chennai" in event_details else "Unknown",
            "attendees": 100 if "100" in event_details else 0,
            "date": "October 2025" if "October" in event_details else "TBD",
            "key_requirements": event_details
        }
    
    def _extract_results(self):
        """Extract results from group chat messages"""
        # Extract task list
        for msg in reversed(self.groupchat.messages):
            if "task_list" in msg.get("content", ""):
                try:
                    content = msg["content"]
                    start = content.find('[')
                    end = content.rfind(']') + 1
                    if start != -1 and end != -1:
                        self.task_list = json.loads(content[start:end])
                        break
                except:
                    pass
        
        # Extract progress report
        for msg in reversed(self.groupchat.messages):
            if "progress_report" in msg.get("content", ""):
                self.progress_report = msg["content"]
                break
        
        # Create timeline from task list
        self.timeline = [
            {"task": task["name"], "category": task["category"], "deadline": task["deadline"], "status": "pending"}
            for task in self.task_list
        ]

# Create singleton instance
event_planner = EventPlanner()