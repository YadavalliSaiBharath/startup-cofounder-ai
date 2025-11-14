"""
Strategy Agent - Acts as a CEO/Business Strategist
This agent analyzes startup ideas and provides strategic business advice
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv


load_dotenv()

class StrategyAgent:
    """
    The Strategy Agent acts like a CEO with years of business experience.
    It analyzes startup ideas and provides comprehensive business strategy.
    """
    
    def __init__(self):
        """
        Initialize the Strategy Agent with:
        - API key from .env file
        - Groq LLM model
        - System prompt (agent's personality)
        """
        
    
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "llama-3.1-70b-versatile")
        
        
        self.llm = ChatGroq(
            api_key=self.api_key,
            model_name=self.model_name,
            temperature=0.7  
        )
        
        
        self.system_prompt = """You are an experienced CEO and business strategist with 20+ years of experience in startup advisory. 

Your expertise includes:
- Business model design and validation
- Market analysis and competitive positioning
- Revenue strategy and growth planning
- Risk assessment and mitigation
- Strategic planning and execution

When analyzing a startup idea, you provide:
1. **Business Model Analysis**: How the business will work
2. **Market Opportunity**: Target market size and potential
3. **Competitive Landscape**: Key competitors and differentiation
4. **Revenue Streams**: How the business will make money
5. **Strategic Recommendations**: Key actions and priorities
6. **Risk Assessment**: Potential challenges and mitigation strategies

Be thorough, analytical, and provide actionable insights. Use clear structure and bullet points for readability."""

    def analyze_startup_idea(self, startup_idea: str) -> str:
        """
        Main method: Analyzes a startup idea
        
        Args:
            startup_idea (str): The business idea to analyze
            
        Returns:
            str: Comprehensive strategic analysis
        """
        
        # Creatng the conversation messages
        messages = [
            SystemMessage(content=self.system_prompt),
            
            HumanMessage(content=f"""Analyze this startup idea comprehensively:

**Startup Idea:** {startup_idea}

Provide a detailed strategic analysis covering:
1. Business Model & Value Proposition
2. Target Market & Customer Segments
3. Competitive Analysis
4. Revenue Model & Pricing Strategy
5. Key Success Factors
6. Potential Risks & Mitigation
7. Strategic Recommendations & Next Steps

Be specific and actionable in your recommendations.""")
        ]
        
        # Sends messages to the LLM and get response
        # This is where the AI "thinks" and generates the analysis
        response = self.llm.invoke(messages)
        
        # Returns the agent's analysis
        return response.content

    def get_quick_feedback(self, startup_idea: str) -> str:
        """
        Provides quick, high-level feedback on a startup idea
        Useful for rapid iteration and brainstorming
        
        Args:
            startup_idea (str): The business idea
            
        Returns:
            str: Brief strategic feedback
        """
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""Provide quick strategic feedback on this idea in 3-4 sentences:

{startup_idea}

Focus on: viability, key opportunity, and one major risk.""")
        ]
        
        response = self.llm.invoke(messages)
        return response.content


# Test function
if __name__ == "__main__":
    """
    This code runs only when you execute this file directly
    Useful for testing the agent before integrating it
    """
    
    print("🤖 Strategy Agent Test\n")
    print("=" * 50)
    
    # Creates an instance of the Strategy Agent
    agent = StrategyAgent()
    
    # Tests with a sample startup idea
    test_idea = "An AI-powered meal planning app that creates personalized weekly meal plans based on dietary preferences, budget, and available cooking time. It also generates shopping lists and provides step-by-step cooking instructions."
    
    print(f"\n📝 Testing with idea:\n{test_idea}\n")
    print("=" * 50)
    print("\n🔍 Analysis:\n")
    
    # Gets the agent's analysis
    analysis = agent.analyze_startup_idea(test_idea)
    
    print(analysis)
    print("\n" + "=" * 50)
    print("✅ Test complete!")