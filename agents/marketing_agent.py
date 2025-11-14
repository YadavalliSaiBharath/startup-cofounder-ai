"""
Marketing Agent - Acts as a CMO/Marketing Strategist
This agent creates marketing strategy based on business strategy AND technical decisions
Designed for maximum collaboration with other agents
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()

class MarketingAgent:
    """
    The Marketing Agent acts like a CMO with expertise in brand strategy,
    customer acquisition, and growth marketing.
    
    MOST COLLABORATIVE AGENT:
    - Reads BOTH Strategy and Technical Agent outputs
    - Aligns marketing with business goals AND technical capabilities
    - Creates cohesive go-to-market plan
    """
    
    def __init__(self):
        """
        Initialize the Marketing Agent
        """
        
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
        
        self.llm = ChatGroq(
            api_key=self.api_key,
            model_name=self.model_name,
            temperature=0.8  
        )
        
        # Defines CMO personality -  collaboration
        self.system_prompt = """You are an experienced CMO and marketing strategist with 15+ years in brand building, customer acquisition, and growth marketing.

Your expertise includes:
- Brand positioning and messaging
- Customer acquisition strategy (paid and organic)
- Content marketing and storytelling
- Channel strategy and optimization
- Growth hacking and viral marketing
- Marketing budget allocation and ROI

**CRITICAL - Collaborative Mindset:**
You work closely with the Strategy Agent (CEO) and Technical Agent (CTO). Your marketing plans must:

1. **Align with Business Strategy**: 
   - Target the exact customer segments identified
   - Support the revenue model and pricing
   - Match the timeline and growth goals
   
2. **Work with Technical Constraints**:
   - Market what can actually be built
   - Time campaigns with product launch dates
   - Consider platform limitations (web vs mobile vs both)
   
3. **Create Cohesion**:
   - Reference specific points from strategy and tech analyses
   - Show how marketing supports both business and technical plans
   - Build bridges between different aspects of the business

When creating marketing strategy, provide:
1. **Brand Positioning**: How we'll position in the market (based on competitive analysis)
2. **Target Audience Strategy**: Specific segments with acquisition tactics
3. **Marketing Channels**: Prioritized based on budget, timeline, and platform
4. **Content Strategy**: What we'll create and why
5. **Go-to-Market Plan**: Phased approach aligned with product development
6. **Budget Allocation**: How to spend limited resources effectively
7. **Success Metrics**: KPIs that matter for this specific business

Always reference the strategy and technical context in your recommendations!
"""

    def create_marketing_strategy(
        self, 
        startup_idea: str,
        strategy_context: str = None,
        technical_context: str = None
    ) -> str:
        """
        Create comprehensive marketing strategy
        
        Args:
            startup_idea (str): The business idea
            strategy_context (str): Output from Strategy Agent
            technical_context (str): Output from Technical Agent
            
        Returns:
            str: Complete marketing strategy and go-to-market plan
        """
        
        # Buildng collaborative prompt
        if strategy_context and technical_context:
            
            prompt = f"""You are the CMO. Read the analyses from your CEO (Strategy) and CTO (Technical) below, then create a marketing strategy that aligns with both.

**CEO'S BUSINESS STRATEGY:**
{strategy_context}

**CTO'S TECHNICAL PLAN:**
{technical_context}

**ORIGINAL STARTUP IDEA:**
{startup_idea}

Now, create a comprehensive marketing strategy that:
- Targets the customers identified by the CEO
- Works within the budget and timeline from business strategy
- Aligns with the technical platform and launch plan from CTO
- Creates a cohesive go-to-market approach

Structure your response as:

## 1. Brand Positioning & Messaging
(Based on competitive analysis and target market from strategy)

## 2. Target Audience Strategy
(Specific segments with acquisition tactics for each)
- Primary Segment:
- Secondary Segment:
- Acquisition Channels for Each:

## 3. Marketing Channel Strategy
(Prioritized channels based on budget, platform, and timeline)
- Phase 1 (Pre-Launch):
- Phase 2 (Launch):
- Phase 3 (Growth):

## 4. Content & Creative Strategy
(What content we'll create and why)

## 5. Go-to-Market Timeline
(Aligned with product development milestones from CTO)

## 6. Budget Allocation
(How to allocate marketing budget effectively)

## 7. Key Messaging & Copy
(Sample taglines, value propositions, ad copy)

## 8. Success Metrics & KPIs
(Specific metrics for this business model)

## 9. Launch Campaign Plan
(Detailed plan for launch week/month)

**IMPORTANT:** Reference specific points from both the Strategy and Technical analyses throughout your recommendations. Show how marketing connects business goals with technical capabilities!"""
        
        elif strategy_context:
            # STRATEGY-ONLY COLLABORATION
            prompt = f"""Based on the business strategy below, create a marketing strategy:

**BUSINESS STRATEGY:**
{strategy_context}

**STARTUP IDEA:**
{startup_idea}

Create comprehensive marketing strategy that aligns with the business goals above."""
        
        else:
            prompt = f"""Create a comprehensive marketing strategy for:

**STARTUP IDEA:**
{startup_idea}

Include brand positioning, target audience, channels, content strategy, and go-to-market plan."""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        return response.content

    def create_launch_campaign(
        self,
        startup_idea: str,
        launch_date: str = "in 3 months"
    ) -> str:
        """
        Creates focused launch campaign plan
        """
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""Create a detailed launch campaign plan for:

{startup_idea}

Launch date: {launch_date}

Include:
1. Pre-launch activities (4-6 weeks before)
2. Launch week strategy
3. Post-launch momentum tactics
4. Budget allocation
5. Key messaging""")
        ]
        
        response = self.llm.invoke(messages)
        return response.content


# Test function
if __name__ == "__main__":
    """
    Test Marketing Agent with full collaboration
    """
    
    print("🤖 Marketing Agent Test - Full Collaboration Mode\n")
    print("=" * 70)
    
    agent = MarketingAgent()
    
    test_idea = "An AI-powered meal planning app that creates personalized weekly meal plans based on dietary preferences, budget, and available cooking time."
    
    #strategy context
    mock_strategy = """
**Business Model:**
- Target: Busy professionals, 25-40 years old, $50k+ income
- Revenue: Freemium + $9.99/month premium subscription
- Key Value: Save 5+ hours per week on meal planning
- Market Size: 45M potential users in US
- Timeline: MVP in 3 months for holiday season launch

**Competitive Edge:**
- Better AI personalization than competitors
- Focus on budget-conscious meal planning (unique angle)
- Integration with grocery delivery services

**Strategic Priorities:**
1. Fast market entry (3 months)
2. Cost-efficient customer acquisition (<$20 CAC)
3. High retention (target 70% monthly retention)
"""
    
    #technical context
    mock_technical = """
**Technology Stack:**
- Frontend: React Native (iOS and Android from single codebase)
- Backend: Python/FastAPI with OpenAI API integration
- Database: PostgreSQL
- Infrastructure: AWS (serverless architecture for cost efficiency)

**Launch Plan:**
- Month 1: MVP development (core meal planning features)
- Month 2: Beta testing with 100 users
- Month 3: Public launch on App Store and Google Play

**Platform:**
- Mobile-first (app only at launch)
- Web version in Phase 2 (Month 6)
- Push notifications for meal reminders

**Costs:**
- Development: $15k (3 months)
- Infrastructure: $500/month initially
- AI API costs: $0.02 per meal plan generated
"""
    
    print("\n📱 FULL COLLABORATION TEST:")
    print("(Marketing Agent reads BOTH Strategy and Technical outputs)\n")
    print("=" * 70)
    print("\n📢 Marketing Strategy:\n")
    
    #fully collaborative marketing strategy
    strategy = agent.create_marketing_strategy(
        test_idea, 
        mock_strategy, 
        mock_technical
    )
    
    print(strategy)
    
    print("\n" + "=" * 70)
    print("✅ Full collaboration test complete!")
    print("\nNOTICE: Marketing strategy references BOTH business goals AND technical decisions!")