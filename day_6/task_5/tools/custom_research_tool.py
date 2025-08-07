class ResearchTool:
    def run(self, query):
        knowledge = {
            "prompt engineering": "Prompt engineering is crafting input to get optimal LLM output.",
            "langchain": "LangChain is a Python framework for building LLM-powered applications."
        }
        for k, v in knowledge.items():
            if k in query.lower():
                return v
        return "No relevant info in custom research DB."
