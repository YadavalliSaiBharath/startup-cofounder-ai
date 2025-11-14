"""
Multi-Agent Collaboration Workflow using LangGraph
This orchestrates the Strategy, Technical, and Marketing agents to work together
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import operator

# Importing all my agents
from agents.strategy_agent import StrategyAgent
from agents.technical_agent import TechnicalAgent
from agents.marketing_agent import MarketingAgent


# Defineng the shared state that all agents can access
class AgentState(TypedDict):
    """
    Shared state that flows through all agents
    Think of this as a shared document that each agent reads and updates
    """
    # Input from user
    startup_idea: str
    
    # Agent outputs
    strategy_analysis: str
    technical_analysis: str
    marketing_strategy: str
    
    # Final combined output
    final_report: str
    
    # Metadata
    current_step: str


class StartupCoFounderWorkflow:
    """
    Orchestrates the three agents to work together as a startup team
    
    WORKFLOW:
    1. User provides startup idea
    2. Strategy Agent analyzes business viability
    3. Technical Agent reads strategy, creates tech plan
    4. Marketing Agent reads both, creates marketing strategy
    5. All combined into unified report
    """
    
    def __init__(self):
        """
        Initialize all agents and build the workflow graph
        """
        print("🚀 Initializing Multi-Agent Workflow...")
        
        # Createing instances of all agents
        self.strategy_agent = StrategyAgent()
        self.technical_agent = TechnicalAgent()
        self.marketing_agent = MarketingAgent()
        
        # the workflow graph
        self.workflow = self._build_workflow()
        
        print("✅ Workflow initialized successfully!")
    
    def _build_workflow(self) -> StateGraph:
        """
        Build the LangGraph workflow
        
        This defines:
        - What agents exist (nodes)
        - What order they run in (edges)
        - How they share information (state)
        """
        
        # Createing the graph with our state structure
        workflow = StateGraph(AgentState)
        
        # Addng nodes (each agent is a node)
        workflow.add_node("strategy_agent", self._run_strategy_agent)
        workflow.add_node("technical_agent", self._run_technical_agent)
        workflow.add_node("marketing_agent", self._run_marketing_agent)
        workflow.add_node("compile_report", self._compile_final_report)
        
        # the flow (edges between nodes)
        workflow.set_entry_point("strategy_agent")  # Start here
        workflow.add_edge("strategy_agent", "technical_agent")  # Strategy → Technical
        workflow.add_edge("technical_agent", "marketing_agent")  # Technical → Marketing
        workflow.add_edge("marketing_agent", "compile_report")  # Marketing → Compile
        workflow.add_edge("compile_report", END)  # Compile → End
        
        return workflow.compile()
    
    def _run_strategy_agent(self, state: AgentState) -> AgentState:
        """
        Run the Strategy Agent (CEO)
        This is the FIRST agent to run
        """
        print("\n🎯 Strategy Agent (CEO) is analyzing the business idea...")
        
        startup_idea = state["startup_idea"]
        
        strategy_analysis = self.strategy_agent.analyze_startup_idea(startup_idea)
        
        # Updateing state with results
        state["strategy_analysis"] = strategy_analysis
        state["current_step"] = "Strategy Complete"
        
        print("✅ Strategy analysis complete!")
        
        return state
    
    def _run_technical_agent(self, state: AgentState) -> AgentState:
        """
        Run the Technical Agent (CTO)
        This agent READS the strategy analysis
        """
        print("\n💻 Technical Agent (CTO) is creating the technical plan...")
        print("   (Reading strategy analysis...)")
        
        startup_idea = state["startup_idea"]
        strategy_context = state["strategy_analysis"]
        
        # collaboration!
        technical_analysis = self.technical_agent.analyze_technical_requirements(
            startup_idea,
            strategy_context  # ← This is the key! Passing strategy to tech agent
        )
        
        # Updateing state
        state["technical_analysis"] = technical_analysis
        state["current_step"] = "Technical Complete"
        
        print("✅ Technical plan complete!")
        
        return state
    
    def _run_marketing_agent(self, state: AgentState) -> AgentState:
        """
        Run the Marketing Agent (CMO)
        This agent READS both strategy and technical analyses
        """
        print("\n📢 Marketing Agent (CMO) is developing the marketing strategy...")
        print("   (Reading strategy and technical analyses...)")
        
        startup_idea = state["startup_idea"]
        strategy_context = state["strategy_analysis"]
        technical_context = state["technical_analysis"]
        
        # full collaboration
        marketing_strategy = self.marketing_agent.create_marketing_strategy(
            startup_idea,
            strategy_context,   # ← From CEO
            technical_context   # ← From CTO
        )
        
        # Updateing state
        state["marketing_strategy"] = marketing_strategy
        state["current_step"] = "Marketing Complete"
        
        print("✅ Marketing strategy complete!")
        
        return state
    
    def _compile_final_report(self, state: AgentState) -> AgentState:
        """
        Compile all agent outputs into one unified report
        """
        print("\n📊 Compiling final comprehensive report...")
        
        final_report = f"""
# 🚀 COMPREHENSIVE STARTUP ANALYSIS
## Generated by AI Co-Founder Team

---

## 📋 STARTUP IDEA
{state["startup_idea"]}

---

## 🎯 BUSINESS STRATEGY ANALYSIS
### By Strategy Agent (CEO)

{state["strategy_analysis"]}

---

## 💻 TECHNICAL ARCHITECTURE & PLAN
### By Technical Agent (CTO)

{state["technical_analysis"]}

---

## 📢 MARKETING STRATEGY & GO-TO-MARKET
### By Marketing Agent (CMO)

{state["marketing_strategy"]}

---

## ✅ NEXT STEPS & ACTION ITEMS

Based on the collaborative analysis above, here are the immediate priorities:

1. **Week 1-2**: Validate assumptions with target customers (from Strategy)
2. **Week 3-4**: Set up technical infrastructure (from Technical)
3. **Week 4-6**: Begin pre-launch marketing activities (from Marketing)
4. **Month 2**: Start MVP development
5. **Month 3**: Beta testing and launch preparation

---

*This report was generated by a multi-agent AI system where each agent built upon the insights of previous agents to create a cohesive, unified strategy.*
"""
        
        # Updateing state with final report
        state["final_report"] = final_report
        state["current_step"] = "Complete"
        
        print("✅ Final report compiled!")
        
        return state
    
    def analyze_startup(self, startup_idea: str) -> dict:
        """
        Main method to run the complete multi-agent workflow
        
        Args:
            startup_idea (str): The startup idea to analyze
            
        Returns:
            dict: Complete analysis with all agent outputs
        """
        
        print("\n" + "="*70)
        print("🤖 MULTI-AGENT STARTUP CO-FOUNDER SYSTEM")
        print("="*70)
        print(f"\n💡 Analyzing: {startup_idea[:100]}...")
        print("\n" + "="*70)
        
        initial_state = {
            "startup_idea": startup_idea,
            "strategy_analysis": "",
            "technical_analysis": "",
            "marketing_strategy": "",
            "final_report": "",
            "current_step": "Starting"
        }
        
        # This executes: Strategy → Technical → Marketing → Compile
        final_state = self.workflow.invoke(initial_state)
        
        print("\n" + "="*70)
        print("✅ ANALYSIS COMPLETE!")
        print("="*70 + "\n")
        
        return final_state


# Test function
if __name__ == "__main__":
    """
    Test the complete multi-agent workflow
    """
    
    workflow = StartupCoFounderWorkflow()
    
    test_idea = """An AI-powered meal planning app for busy professionals that:
- Creates personalized weekly meal plans based on dietary preferences and budget
- Generates automated shopping lists
- Provides step-by-step cooking instructions
- Integrates with grocery delivery services
- Learns from user preferences over time"""
    
    result = workflow.analyze_startup(test_idea)
    
    print("\n" + "="*70)
    print("📄 FINAL COMPREHENSIVE REPORT")
    print("="*70 + "\n")
    print(result["final_report"])
    
    print("\n" + "="*70)
    print("🎉 Multi-Agent Collaboration Test Complete!")
    print("="*70)