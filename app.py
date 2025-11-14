"""
Startup Co-Founder AI - Multi-Agent System Application
Complete workflow with Strategy, Technical, and Marketing agents
"""

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from workflows.collaboration import StartupCoFounderWorkflow
import time

# Page configuration
st.set_page_config(
    page_title="AI Startup Co-Founder Team",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextArea textarea {
        font-size: 16px;
    }
    .agent-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 14px;
        font-weight: bold;
        margin: 4px;
    }
    .strategy-badge {
        background-color: #e3f2fd;
        color: #1976d2;
    }
    .technical-badge {
        background-color: #f3e5f5;
        color: #7b1fa2;
    }
    .marketing-badge {
        background-color: #fff3e0;
        color: #f57c00;
    }
    </style>
""", unsafe_allow_html=True)

# Initializeiing workflow (cached)
@st.cache_resource
def load_workflow():
    """
    Load and cache the multi-agent workflow
    """
    return StartupCoFounderWorkflow()

# Main App
def main():
    """
    Main application
    """
    
    # Header
    st.title("🚀 AI Startup Co-Founder Team")
    st.markdown("**Your complete AI business team: CEO, CTO, and CMO working together**")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🤖 Your AI Team")
        
        st.markdown("""
        <div class="agent-badge strategy-badge">🎯 Strategy Agent (CEO)</div>
        <p style='font-size: 13px; margin-left: 10px;'>
        • Business model analysis<br>
        • Market opportunity<br>
        • Competitive strategy<br>
        • Risk assessment
        </p>
        
        <div class="agent-badge technical-badge">💻 Technical Agent (CTO)</div>
        <p style='font-size: 13px; margin-left: 10px;'>
        • Technology stack<br>
        • System architecture<br>
        • Development roadmap<br>
        • Resource planning
        </p>
        
        <div class="agent-badge marketing-badge">📢 Marketing Agent (CMO)</div>
        <p style='font-size: 13px; margin-left: 10px;'>
        • Brand positioning<br>
        • Marketing strategy<br>
        • Go-to-market plan<br>
        • Customer acquisition
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**💡 How It Works:**")
        st.markdown("""
        1. CEO analyzes business viability
        2. CTO reads strategy, plans tech
        3. CMO reads both, creates marketing
        4. All combined into master plan
        """)
        
        st.markdown("---")
        st.markdown("**Model:** Llama 3.3 70B via Groq")
        st.markdown("**Status:** ✅ Multi-Agent Active")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Enter Your Startup Idea")
        
        startup_idea = st.text_area(
            "Describe your startup idea in detail:",
            placeholder="Example: An AI-powered personal finance app that analyzes spending patterns, provides personalized savings recommendations, and automatically invests spare change. Target market is millennials aged 25-35 who want to build wealth but don't have time for complex financial planning.",
            height=180,
            help="The more detail you provide, the better the analysis. Include target market, key features, and value proposition."
        )
        
        analyze_button = st.button(
            "🚀 Analyze with Full AI Team", 
            type="primary", 
            use_container_width=True
        )
    
    with col2:
        st.header("ℹ️ What You'll Get")
        st.markdown("""
        **Complete Startup Analysis:**
        
        🎯 **Business Strategy**
        - Market analysis
        - Business model
        - Competitive positioning
        - Revenue strategy
        
        💻 **Technical Plan**
        - Tech stack recommendations
        - Architecture design
        - Development timeline
        - Cost estimates
        
        📢 **Marketing Strategy**
        - Brand positioning
        - Channel strategy
        - Launch campaign
        - Customer acquisition
        
        📊 **Unified Master Plan**
        All insights combined into one cohesive strategy!
        """)
    
    # Initializing session state
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
        st.session_state.startup_idea = None
        st.session_state.analysis_time = None
    
    # Process analysis
    if analyze_button:
        if not startup_idea.strip():
            st.error("⚠️ Please enter a startup idea to analyze!")
        else:
            # Loading mym workflow
            workflow = load_workflow()
            
            # Creating progress container
            progress_container = st.container()
            
            with progress_container:
                st.markdown("---")
                st.subheader("🤖 AI Team Working...")
                
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Agent status indicators
                col_s, col_t, col_m = st.columns(3)
                with col_s:
                    strategy_status = st.empty()
                    strategy_status.markdown("🎯 **Strategy Agent**: ⏳ Waiting...")
                with col_t:
                    technical_status = st.empty()
                    technical_status.markdown("💻 **Technical Agent**: ⏳ Waiting...")
                with col_m:
                    marketing_status = st.empty()
                    marketing_status.markdown("📢 **Marketing Agent**: ⏳ Waiting...")
            
            try:
                start_time = time.time()
                
                # Update status : Strategy Agent working
                status_text.text("Strategy Agent (CEO) analyzing business viability...")
                strategy_status.markdown("🎯 **Strategy Agent**: 🔄 Analyzing...")
                progress_bar.progress(25)
                
                # Running the complete workflow
                # We'll update status by checking the state as it progresses
                result = workflow.analyze_startup(startup_idea)
                
                # Technical Agent
                progress_bar.progress(50)
                strategy_status.markdown("🎯 **Strategy Agent**: ✅ Complete")
                technical_status.markdown("💻 **Technical Agent**: ✅ Complete")
                status_text.text("Technical Agent (CTO) completed tech plan...")
                
                # Marketing Agent
                progress_bar.progress(75)
                marketing_status.markdown("📢 **Marketing Agent**: ✅ Complete")
                status_text.text("Marketing Agent (CMO) completed strategy...")
                
                # Final compilation
                progress_bar.progress(100)
                status_text.text("Compiling comprehensive report...")
                
                end_time = time.time()
                analysis_time = round(end_time - start_time, 2)
                
                # Storing  in session state
                st.session_state.analysis_result = result
                st.session_state.startup_idea = startup_idea
                st.session_state.analysis_time = analysis_time
                
                # Clearng progress indicators
                time.sleep(0.5)
                progress_container.empty()
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.info("💡 Tips:\n- Check your API key in .env\n- Ensure internet connection\n- Try again")
    
    # Displaying results
    if st.session_state.analysis_result:
        result = st.session_state.analysis_result
        
        st.success(f"✅ Complete analysis by your AI team! (took {st.session_state.analysis_time} seconds)")
        
        st.markdown("---")
        
        # Creating tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Master Plan", 
            "🎯 Strategy (CEO)", 
            "💻 Technical (CTO)", 
            "📢 Marketing (CMO)",
            "💾 Export"
        ])
        
        with tab1:
            st.header("📊 Comprehensive Master Plan")
            st.markdown("*All three agents collaborated to create this unified strategy*")
            st.markdown(result["final_report"])
        
        with tab2:
            st.header("🎯 Business Strategy Analysis")
            st.markdown("*by Strategy Agent (CEO)*")
            st.markdown(result["strategy_analysis"])
        
        with tab3:
            st.header("💻 Technical Architecture & Plan")
            st.markdown("*by Technical Agent (CTO)*")
            st.markdown(result["technical_analysis"])
        
        with tab4:
            st.header("📢 Marketing Strategy & Go-to-Market")
            st.markdown("*by Marketing Agent (CMO)*")
            st.markdown(result["marketing_strategy"])
        
        with tab5:
            st.markdown("### 💾 Export Your Analysis")
            
            col_e1, col_e2 = st.columns(2)
            
            with col_e1:
                st.markdown("**📥 Download Complete Report**")
                st.download_button(
                    label="Download Master Plan (Markdown)",
                    data=result["final_report"],
                    file_name="startup_analysis_complete.md",
                    mime="text/markdown"
                )
            
            with col_e2:
                st.markdown("**📋 Copy to Clipboard**")
                st.code(result["final_report"], language=None)
                st.caption("Click the copy button ☝️")
            
            st.markdown("---")
            st.markdown("**Individual Agent Reports:**")
            
            col_d1, col_d2, col_d3 = st.columns(3)
            
            with col_d1:
                st.download_button(
                    label="📥 Strategy Report",
                    data=result["strategy_analysis"],
                    file_name="strategy_analysis.txt",
                    mime="text/plain"
                )
            
            with col_d2:
                st.download_button(
                    label="📥 Technical Report",
                    data=result["technical_analysis"],
                    file_name="technical_analysis.txt",
                    mime="text/plain"
                )
            
            with col_d3:
                st.download_button(
                    label="📥 Marketing Report",
                    data=result["marketing_strategy"],
                    file_name="marketing_strategy.txt",
                    mime="text/plain"
                )
        
        # Feedback section
        st.markdown("---")
        st.subheader("💬 Feedback")
        col_fb1, col_fb2, col_fb3 = st.columns(3)
        
        with col_fb1:
            if st.button("👍 Excellent Analysis"):
                st.success("Thank you! Your AI team appreciates the feedback!")
        
        with col_fb2:
            if st.button("👎 Needs Improvement"):
                st.info("Thanks for the feedback! We're always improving.")
        
        with col_fb3:
            if st.button("🔄 Analyze New Idea"):
                st.session_state.analysis_result = None
                st.session_state.startup_idea = None
                st.session_state.analysis_time = None
                st.rerun()
    
    if not st.session_state.analysis_result:
        st.markdown("---")
        st.header("💡 Example Startup Ideas")
        
        col_ex1, col_ex2, col_ex3 = st.columns(3)
        
        with col_ex1:
            if st.button("🍔 AI Meal Planner", use_container_width=True):
                st.session_state.example_idea = "An AI-powered meal planning app that creates personalized weekly meal plans based on dietary preferences, budget, and cooking time. Generates shopping lists and provides recipes."
                st.rerun()
            
            if st.button("💼 B2B Sales Platform", use_container_width=True):
                st.session_state.example_idea = "A B2B sales automation platform that uses AI to qualify leads, personalize outreach, and predict deal closure probability. Target market is SMBs with 10-100 employees."
                st.rerun()
        
        with col_ex2:
            if st.button("🎓 EdTech Learning", use_container_width=True):
                st.session_state.example_idea = "An adaptive learning platform that uses AI to create personalized study plans based on learning style and knowledge gaps. Focuses on high school and college STEM subjects."
                st.rerun()
            
            if st.button("💰 Personal Finance", use_container_width=True):
                st.session_state.example_idea = "A personal finance app that analyzes spending patterns, provides savings recommendations, and automatically invests spare change. Target market is millennials aged 25-35."
                st.rerun()
        
        with col_ex3:
            if st.button("🏋️ Fitness Coaching", use_container_width=True):
                st.session_state.example_idea = "An AI fitness coach app that creates personalized workout plans, tracks progress through phone camera, and adjusts difficulty based on performance. For beginners starting their fitness journey."
                st.rerun()
            
            if st.button("🏠 Smart Home Energy", use_container_width=True):
                st.session_state.example_idea = "A smart home energy optimization system that learns usage patterns and automatically adjusts heating/cooling/lighting to minimize bills while maintaining comfort."
                st.rerun()
        
        # If example was clicked, populate the text area
        if 'example_idea' in st.session_state:
            st.info(f"💡 Example loaded! Scroll up and click 'Analyze with Full AI Team'")

if __name__ == "__main__":
    main()