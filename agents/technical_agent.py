"""
Technical Agent - Acts as a CTO/Technical Architect
This agent makes technology decisions based on business strategy
Designed to work collaboratively with Strategy Agent
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()

class TechnicalAgent:
    """
    The Technical Agent acts like a CTO with deep technical expertise.
    It reads the business strategy and makes informed technical decisions.
    
    KEY DIFFERENCE FROM INDEPENDENT AGENT:
    - Takes strategy_context as input
    - Makes decisions BASED ON business requirements
    - References specific business needs in recommendations
    """
    
    def __init__(self):
        """
        Initialize the Technical Agent
        """
        
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
        
        # Initializingg LLM
        self.llm = ChatGroq(
            api_key=self.api_key,
            model_name=self.model_name,
            temperature=0.7
        )
        
        # Defines CTO personality and expertise
        #This prompt is designed for COLLABORATION
        self.system_prompt = """You are an experienced CTO and technical architect with 15+ years in software development and system design.

Your expertise includes:
- Technology stack selection and architecture design
- Scalability and performance optimization
- Development timeline and resource estimation
- Technical risk assessment and mitigation
- DevOps, security, and infrastructure planning
- Cost-effective technical solutions

**IMPORTANT - Collaborative Approach:**
You will receive business strategy insights from the Strategy Agent. Your job is to:
1. **Read and understand** the business requirements carefully
2. **Reference specific business needs** in your recommendations
3. **Align technical decisions** with business goals, budget, and timeline
4. **Explain WHY** each technical choice supports the business strategy

When analyzing, provide:
1. **Recommended Tech Stack**: Specific technologies with justifications tied to business needs
2. **System Architecture**: High-level design that supports the business model
3. **Development Roadmap**: Phased approach aligned with business priorities
4. **Resource Requirements**: Team size, skills, and budget estimates
5. **Technical Risks**: Challenges and mitigation strategies
6. **Scalability Plan**: How the system will grow with the business

Always connect your technical recommendations back to the business strategy. 
For example: "Given the target of busy professionals mentioned in the strategy, 
we'll prioritize mobile-first design and quick load times under 2 seconds."
"""

    def analyze_technical_requirements(
        self, 
        startup_idea: str, 
        strategy_context: str = None
    ) -> str:
        """
        Analyze technical requirements for a startup
        
        Args:
            startup_idea (str): The business idea
            strategy_context (str): Output from Strategy Agent (for collaboration)
            
        Returns:
            str: Comprehensive technical analysis and recommendations
        """
        
        # Builds the prompt based on whether we have strategy context orr not
        if strategy_context:
            # COLLABORATIVE MODE: Usees strategy insights
            prompt = f"""Based on the business strategy analysis below, provide comprehensive technical recommendations.

**BUSINESS STRATEGY ANALYSIS:**
{strategy_context}

**ORIGINAL STARTUP IDEA:**
{startup_idea}

Now, as the CTO, provide technical analysis that ALIGNS with the business strategy above. 

Structure your response as:

## 1. Technical Strategy Overview
(How your technical approach supports the business goals)

## 2. Recommended Technology Stack
(Specific technologies with justifications linked to business needs)
- Frontend:
- Backend:
- Database:
- Infrastructure:
- AI/ML (if applicable):

## 3. System Architecture
(High-level design that supports the business model)

## 4. Development Roadmap
(Phased approach aligned with business priorities and timeline)
- Phase 1 (MVP):
- Phase 2 (Scale):
- Phase 3 (Advanced):

## 5. Team & Resource Requirements
(Based on the business strategy and timeline)

## 6. Technical Risks & Mitigation
(Specific to this business model and market)

## 7. Cost Estimates
(Infrastructure and development costs aligned with business budget)

## 8. Scalability & Performance Strategy
(How we'll handle growth based on business projections)

**Remember:** Reference specific points from the business strategy in your recommendations!"""
        
        else:
            # STANDALONE MODE: No strategy context
            prompt = f"""Analyze the technical requirements for this startup idea:

**STARTUP IDEA:**
{startup_idea}

Provide comprehensive technical recommendations covering:
1. Technology Stack
2. System Architecture
3. Development Roadmap
4. Resource Requirements
5. Technical Risks
6. Cost Estimates
7. Scalability Plan"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        # Gets response from LLM
        response = self.llm.invoke(messages)
        
        return response.content

    def quick_tech_assessment(self, startup_idea: str) -> str:
        """
        Provides quick technical assessment
        Useful for rapid validation
        """
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""Provide a quick technical assessment (3-4 sentences) for:

{startup_idea}

Focus on: recommended tech stack, biggest technical challenge, and estimated timeline.""")
        ]
        
        response = self.llm.invoke(messages)
        return response.content


# Test function
if __name__ == "__main__":
    """
    Test the Technical Agent with and without strategy context
    """
    
    print("🤖 Technical Agent Test\n")
    print("=" * 70)
    
    agent = TechnicalAgent()
    
    # Test idea
    test_idea = "An AI-powered meal planning app that creates personalized weekly meal plans based on dietary preferences, budget, and available cooking time."
    
    # Simulated strategy context (what Strategy Agent would provide)
    mock_strategy = """
**Business Model Analysis:**
- Target Market: Busy professionals aged 25-40, household income $50k+
- Revenue Model: Freemium with $9.99/month premium subscription
- Key Value Prop: Save 5+ hours per week on meal planning
- Competitive Edge: AI personalization better than competitors
- Timeline: Need MVP in 3 months to capture holiday season

**Market Opportunity:**
- Market size: 45M busy professionals in US
- Growing trend: 73% want healthier eating but lack time
- Price sensitivity: Target willing to pay $10-15/month for time savings

**Strategic Priority:**
- Launch fast with core features
- Mobile-first approach (users plan on-the-go)
- Keep costs under $5k/month initially
"""
    
    print("\n📱 COLLABORATIVE MODE TEST:")
    print("(Technical Agent reads Strategy Agent's output)\n")
    print("=" * 70)
    print("\n🔍 Technical Analysis:\n")
    
    # Get collaborative analysis
    analysis = agent.analyze_technical_requirements(test_idea, mock_strategy)
    print(analysis)
    
    print("\n" + "=" * 70)
    print("✅ Collaborative test complete!")
    print("\nNOTICE: The technical recommendations reference the business strategy!")