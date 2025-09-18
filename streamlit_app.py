import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import time
import random
from datetime import datetime, timedelta
import json

# 🎨 INSANE GENZ STYLING
st.set_page_config(
    page_title="VibeSync AI Squad 🤖",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🌈 CRAZY CSS FOR GENZ VIBES
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 25%, #2d1b69 50%, #ff006e 75%, #8338ec 100%);
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(90deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
        background-size: 400% 400%;
        animation: gradient 3s ease infinite;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(255, 0, 110, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 25%, transparent 25%), 
                    linear-gradient(-45deg, rgba(255,255,255,0.1) 25%, transparent 25%),
                    linear-gradient(45deg, transparent 75%, rgba(255,255,255,0.1) 75%),
                    linear-gradient(-45deg, transparent 75%, rgba(255,255,255,0.1) 75%);
        background-size: 20px 20px;
        animation: move 2s linear infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes move {
        0% { background-position: 0 0, 0 0, 10px 10px, 10px 10px; }
        100% { background-position: 20px 20px, 20px 20px, 30px 30px, 30px 30px; }
    }
    
    .agent-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .agent-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(131, 56, 236, 0.4);
        border-color: rgba(131, 56, 236, 0.5);
    }
            
    
    .neon-text {
        color: #0a192ff;
        text-shadow: 0 0 10px #06ffa5, 0 0 20px #06ffa5, 0 0 30px #06ffa5;
        font-weight: 800;
    }
    
    .glow-button {
        background: linear-gradient(135deg, #0a192f), #0b192f);;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(255, 0, 110, 0.5);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .status-online {
        display: inline-block;
        width: 12px;
        height: 12px;
        background: #06ffa5;
        border-radius: 50%;
        animation: pulse 2s infinite;
        box-shadow: 0 0 10px #06ffa5;
    }
    
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #0a192f), #0b192f);
        border: 1px solid rgba(255, 0, 110, 0.3);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        color: white;
    }
    
    .chat-bubble {
        background: rgba(58, 134, 255, 0.2);
        border: 1px solid rgba(58, 134, 255, 0.5);
        border-radius: 20px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: white;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 0, 110, 0.3);
        border-radius: 10px;
        color: white;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(131, 56, 236, 0.3);
        border-radius: 10px;
        color: white;
    }
    
    .fire-text {
        background: linear-gradient(45deg, #ff4757, #ff6b9d, #ffa726);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    .ice-text {
        background: linear-gradient(45deg, #00d4ff, #3742fa, #70a1ff);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# 🚀 INITIALIZE SESSION STATE FOR AGENTS
if 'agents' not in st.session_state:
    st.session_state.agents = {
        'vibe_guardian': {'status': 'online', 'tasks': 0, 'last_active': datetime.now()},
        'social_scout': {'status': 'online', 'tasks': 0, 'last_active': datetime.now()},
        'mood_mentor': {'status': 'online', 'tasks': 0, 'last_active': datetime.now()},
        'study_sensei': {'status': 'online', 'tasks': 0, 'last_active': datetime.now()},
        'life_navigator': {'status': 'online', 'tasks': 0, 'last_active': datetime.now()},
    }

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'ai_insights' not in st.session_state:
    st.session_state.ai_insights = []

# 🔥 INSANE HEADER
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 4rem; margin: 0; color: white; position: relative; z-index: 1;">
        🤖 <span class="neon-text">VibeSync</span> AI Squad
    </h1>
    <p style="font-size: 1.5rem; margin: 1rem 0 0 0; color: rgba(255,255,255,0.9); position: relative; z-index: 1;">
        Your Personal AI Agents for the Ultimate GenZ Life Experience 🔥
    </p>
</div>
""", unsafe_allow_html=True)

# 🎯 MAIN NAVIGATION
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🤖 **AI AGENTS**", 
    "💬 **CHAT HUB**", 
    "📊 **ANALYTICS**", 
    "🎮 **CONTROL CENTER**", 
    "🚀 **MISSION BOARD**"
])

# 🤖 AI AGENTS TAB
with tab1:
    st.markdown("## <span class='fire-text'>Your AI Squad is READY! 🔥</span>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # VIBE GUARDIAN AGENT
        st.markdown("""
        <div class="agent-card">
            <h3>🛡️ <span class="neon-text">Vibe Guardian</span> <span class="status-online"></span></h3>
            <p><strong>Mission:</strong> Protect you from toxic people & situations</p>
            <p><strong>Powers:</strong> Chat analysis, Red flag detection, Safety alerts</p>
            <p><strong>Vibe Level:</strong> 🔥🔥🔥🔥🔥</p>
            <button class="glow-button">Activate Guardian</button>
        </div>
        """, unsafe_allow_html=True)
        
        # SOCIAL SCOUT AGENT
        st.markdown("""
        <div class="agent-card">
            <h3>🎯 <span class="ice-text">Social Scout</span> <span class="status-online"></span></h3>
            <p><strong>Mission:</strong> Find your perfect squad & social events</p>
            <p><strong>Powers:</strong> Event discovery, Friend matching, Social insights</p>
            <p><strong>Success Rate:</strong> 96% friend compatibility</p>
            <button class="glow-button">Deploy Scout</button>
        </div>
        """, unsafe_allow_html=True)
        
        # MOOD MENTOR AGENT
        st.markdown("""
        <div class="agent-card">
            <h3>💙 <span class="neon-text">Mood Mentor</span> <span class="status-online"></span></h3>
            <p><strong>Mission:</strong> Keep your mental health on point</p>
            <p><strong>Powers:</strong> Emotion tracking, Wellness tips, Crisis support</p>
            <p><strong>Healing Power:</strong> ∞ emotional support</p>
            <button class="glow-button">Summon Mentor</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # STUDY SENSEI AGENT
        st.markdown("""
        <div class="agent-card">
            <h3>📚 <span class="fire-text">Study Sensei</span> <span class="status-online"></span></h3>
            <p><strong>Mission:</strong> Make studying actually fun & effective</p>
            <p><strong>Powers:</strong> Smart scheduling, Gamification, AI tutoring</p>
            <p><strong>Grade Boost:</strong> +23% average improvement</p>
            <button class="glow-button">Train with Sensei</button>
        </div>
        """, unsafe_allow_html=True)
        
        # LIFE NAVIGATOR AGENT
        st.markdown("""
        <div class="agent-card">
            <h3>🧭 <span class="ice-text">Life Navigator</span> <span class="status-online"></span></h3>
            <p><strong>Mission:</strong> Guide you through life's chaos</p>
            <p><strong>Powers:</strong> Goal setting, Decision making, Future planning</p>
            <p><strong>Success Stories:</strong> 10,000+ lives changed</p>
            <button class="glow-button">Start Journey</button>
        </div>
        """, unsafe_allow_html=True)
        
        # AI NETWORK STATUS
        st.markdown("### 🌐 **AI Network Status**")
        
        network_data = pd.DataFrame({
            'Agent': ['Vibe Guardian', 'Social Scout', 'Mood Mentor', 'Study Sensei', 'Life Navigator'],
            'Status': [100, 98, 99, 95, 97],
            'Tasks Completed': [1247, 892, 1456, 2103, 1789]
        })
        
        fig = px.bar(
            network_data, 
            x='Agent', 
            y='Status',
            color='Tasks Completed',
            title="AI Agent Performance Dashboard",
            color_continuous_scale='plasma'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=16
        )
        st.plotly_chart(fig, use_container_width=True)

# 💬 CHAT HUB TAB
with tab2:
    st.markdown("## <span class='neon-text'>Chat with Your AI Squad 💬</span>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # CHAT INTERFACE
        st.markdown("### 🎯 **Choose Your Agent**")
        selected_agent = st.selectbox(
            "",
            ["🛡️ Vibe Guardian", "🎯 Social Scout", "💙 Mood Mentor", "📚 Study Sensei", "🧭 Life Navigator"]
        )
        
        user_input = st.text_area("💬 What's on your mind?", placeholder="Hey AI squad, I need help with...")
        
        if st.button("🚀 **SEND MESSAGE**", use_container_width=True):
            if user_input:
                # Simulate AI response based on agent
                responses = {
                    "🛡️ Vibe Guardian": f"🛡️ **Vibe Check Complete!** I analyzed your message and here's the tea: {random.choice(['This situation seems sus, bestie. Trust your gut! 🚩', 'Green flags detected! This person seems genuine ✨', 'Neutral vibes - proceed with caution but stay aware 👀'])}",
                    "🎯 Social Scout": f"🎯 **Social Intel Gathered!** Based on your vibe, I found: {random.choice(['3 local events this weekend that match your energy! 🎉', 'A study group that needs someone exactly like you! 📚', 'Coffee shop meetup happening tomorrow - perfect for making friends! ☕'])}",
                    "💙 Mood Mentor": f"💙 **Mental Health Check!** I sense you're feeling {random.choice(['stressed - try the 4-7-8 breathing technique 🌸', 'excited - channel that energy into something creative! ✨', 'overwhelmed - let us break this down into smaller steps '])}",  
                    "📚 Study Sensei": f"📚 **Academic Boost Activated!** For your study goals: {random.choice(['Try the Pomodoro technique - 25 min focus + 5 min break 🍅', 'Create a playlist for different subjects - music helps memory! 🎵', 'Teach someone else what you learned - best retention method! 👥'])}",
                    "🧭 Life Navigator": f"🧭 **Life Path Analysis!** Your next move should be: {random.choice(['Set 3 micro-goals for this week - small wins build momentum! 🎯', 'Network with someone new this week - connections are everything! 🤝', 'Try something that scares you a little - growth happens outside comfort zones! 🚀'])}"
                }
                
                st.session_state.chat_history.append({
                    'user': user_input,
                    'agent': selected_agent,
                    'response': responses[selected_agent],
                    'timestamp': datetime.now()
                })
        
        # CHAT HISTORY
        st.markdown("### 💬 **Recent Conversations**")
        for chat in st.session_state.chat_history[-5:]:
            st.markdown(f"""
            <div class="chat-bubble">
                <strong>You:</strong> {chat['user']}<br>
                <strong>{chat['agent']}:</strong> {chat['response']}<br>
                <small style="color: rgba(255,255,255,0.6);">{chat['timestamp'].strftime('%H:%M')}</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # QUICK ACTIONS
        st.markdown("### ⚡ **Quick Actions**")
        
        if st.button("🚨 **EMERGENCY VIBE CHECK**", use_container_width=True):
            st.markdown("""
            <div class="chat-bubble">
                🛡️ <strong>Emergency Protocol Activated!</strong><br>
                All agents are now monitoring your situation. Stay safe! 💪
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🎉 **FIND WEEKEND PLANS**", use_container_width=True):
            st.markdown("""
            <div class="chat-bubble">
                🎯 <strong>Social Scout Deployed!</strong><br>
                Found 5 events this weekend that match your vibe! Check your notifications 📱
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("💆‍♀️ **MENTAL HEALTH BOOST**", use_container_width=True):
            st.markdown("""
            <div class="chat-bubble">
                💙 <strong>Mood Mentor Activated!</strong><br>
                Here's a personalized wellness plan for today. You got this! ✨
            </div>
            """, unsafe_allow_html=True)
        
        # AGENT STATUS
        st.markdown("### 🤖 **Agent Status**")
        agents_status = ['🛡️ Vibe Guardian: ACTIVE', '🎯 Social Scout: SCANNING', '💙 Mood Mentor: LISTENING', '📚 Study Sensei: READY', '🧭 Life Navigator: PLANNING']
        for status in agents_status:
            st.markdown(f"<div style='color: #06ffa5; margin: 0.5rem 0;'>● {status}</div>", unsafe_allow_html=True)

# 📊 ANALYTICS TAB
with tab3:
    st.markdown("## <span class='fire-text'>Your Life Analytics Dashboard 📊</span>", unsafe_allow_html=True)
    
    # METRICS ROW
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🛡️ Vibe Score</h3>
            <h1 style="color: #06ffa5;">94/100</h1>
            <p>Excellent vibes detected!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>👥 Social Health</h3>
            <h1 style="color: #3742fa;">87%</h1>
            <p>Strong connections</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>💙 Mental Wellness</h3>
            <h1 style="color: #ff6b9d;">91%</h1>
            <p>Thriving mindset</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>📚 Academic Power</h3>
            <h1 style="color: #ffa726;">88%</h1>
            <p>Study game strong</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # MOOD TRACKING CHART
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        mood_scores = np.random.normal(75, 15, 30)
        mood_df = pd.DataFrame({'Date': dates, 'Mood Score': mood_scores})
        
        fig = px.line(mood_df, x='Date', y='Mood Score', title='📈 Your Mood Journey (Last 30 Days)')
        fig.update_traces(line_color='#06ffa5', line_width=3)
        fig.add_hline(y=70, line_dash="dash", line_color="#ff006e", annotation_text="Target Zone")
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # WEEKLY GOALS PROGRESS
        goals_data = pd.DataFrame({
            'Goal': ['Social Events', 'Study Hours', 'Self-Care', 'Exercise', 'Sleep Quality'],
            'Progress': [85, 72, 95, 68, 78],
            'Target': [100, 100, 100, 100, 100]
        })
        
        fig = px.bar(goals_data, x='Goal', y='Progress', title='🎯 Weekly Goals Progress')
        fig.add_scatter(x=goals_data['Goal'], y=goals_data['Target'], 
                       mode='markers', marker=dict(color='#ff006e', size=10), name='Target')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # AGENT INTERACTION HEATMAP
        agents = ['Vibe Guardian', 'Social Scout', 'Mood Mentor', 'Study Sensei', 'Life Navigator']
        hours = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        interaction_data = np.random.randint(1, 10, (7, 5))
        
        fig = px.imshow(interaction_data, 
                       x=agents, y=hours,
                       title='🔥 Agent Interaction Heatmap',
                       color_continuous_scale='plasma')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # SOCIAL NETWORK ANALYSIS
        st.markdown("### 🌐 **Your Social Network**")
        
        network_health = {
            'Close Friends': 8,
            'Study Buddies': 12,
            'Activity Partners': 6,
            'Mentors': 3,
            'New Connections': 15
        }
        
        fig = px.pie(values=list(network_health.values()), 
                    names=list(network_health.keys()),
                    title='Your Social Circle Breakdown')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)

# 🎮 CONTROL CENTER TAB
with tab4:
    st.markdown("## <span class='ice-text'>AI Agent Control Center 🎮</span>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🤖 **Agent Configuration**")
        
        # AGENT SETTINGS
        vibe_sensitivity = st.slider("🛡️ Vibe Guardian Sensitivity", 1, 10, 7)
        social_radius = st.slider("🎯 Social Scout Range (km)", 1, 50, 10)
        mood_check_frequency = st.selectbox("💙 Mood Check Frequency", ["Every hour", "Every 3 hours", "Daily", "Weekly"])
        study_reminders = st.checkbox("📚 Study Sensei Reminders", True)
        life_coaching = st.checkbox("🧭 Life Navigator Active Coaching", True)
        
        st.markdown("### ⚙️ **Advanced Settings**")
        
        ai_personality = st.selectbox("🎭 AI Personality Style", [
            "🔥 Hype Beast (Super energetic)",
            "😎 Cool & Chill (Laid back)",
            "🤓 Smart Friend (Nerdy but fun)",
            "💖 Supportive Bestie (Always caring)"
        ])
        
        privacy_mode = st.selectbox("🔒 Privacy Level", [
            "🌍 Open (Share insights with network)",
            "👥 Friends Only (Limited sharing)",
            "🔐 Private (No data sharing)"
        ])
        
        emergency_contacts = st.text_area("🚨 Emergency Contacts", placeholder="Add phone numbers separated by commas")
        
    with col2:
        st.markdown("### 📊 **Real-Time Agent Activity**")
        
        # LIVE ACTIVITY FEED
        activities = [
            "🛡️ Vibe Guardian: Analyzed 3 chats - All clear! ✅",
            "🎯 Social Scout: Found new event: 'Retro Game Night' 🎮",
            "💙 Mood Mentor: Mood score improving +5 points 📈",
            "📚 Study Sensei: Study session reminder in 30 mins ⏰",
            "🧭 Life Navigator: Weekly goal progress: 73% complete 🎯",
            "🛡️ Vibe Guardian: Red flag detected in message - Alert sent 🚩",
            "🎯 Social Scout: 2 new friend suggestions based on interests 👥",
            "💙 Mood Mentor: Stress level decreased after meditation 🧘‍♀️"
        ]
        
        for i, activity in enumerate(activities):
            time.sleep(0.1)  # Simulate real-time
            st.markdown(f"""
            <div style="background: rgba(131, 56, 236, 0.1); border-left: 3px solid #8338ec; 
                        padding: 0.5rem; margin: 0.25rem 0; border-radius: 5px; color: white;">
                {activity}
                <br><small style="color: rgba(255,255,255,0.6);">{(datetime.now() - timedelta(minutes=i*5)).strftime('%H:%M')}</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 **Quick Agent Commands**")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚀 **BOOST ALL AGENTS**"):
                st.success("🔥 All agents now running at maximum power!")
        with col_b:
            if st.button("😴 **SLEEP MODE**"):
                st.info("😴 Agents now in quiet mode until morning")
        
        col_c, col_d = st.columns(2)
        with col_c:
            if st.button("🧹 **CLEAR HISTORY**"):
                st.session_state.chat_history = []
                st.warning("🗑️ Chat history cleared!")
        with col_d:
            if st.button("📤 **EXPORT DATA**"):
                st.success("📊 Your data package is ready for download!")

# 🚀 MISSION BOARD TAB
with tab5:
    st.markdown("## <span class='fire-text'>Daily Missions & Achievements 🚀</span>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 **Today's Missions**")
        
        missions = [
            {"title": "🛡️ Run 3 Vibe Checks", "progress": 2, "total": 3, "xp": 50, "completed": False},
            {"title": "💬 Have 1 Meaningful Conversation", "progress": 1, "total": 1, "xp": 100, "completed": True},
            {"title": "📚 Study for 2 Hours", "progress": 1.5, "total": 2, "xp": 75, "completed": False},
            {"title": "😊 Log Your Mood 3 Times", "progress": 2, "total": 3, "xp": 30, "completed": False},
            {"title": "🎯 Set 5 Weekly Goals", "progress": 5, "total": 5, "xp": 120, "completed": True},
        ]
        
        for mission in missions:
            progress_percent = (mission["progress"] / mission["total"]) * 100
            status = "✅ COMPLETE" if mission["completed"] else f"⏳ {mission['progress']}/{mission['total']}"
            color = "#06ffa5" if mission["completed"] else "#8338ec"
            
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.05); border-left: 4px solid {color}; 
                        padding: 1rem; margin: 0.5rem 0; border-radius: 10px; color: white;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: white;">{mission['title']}</h4>
                        <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.7);">{status} • +{mission['xp']} XP</p>
                    </div>
                    <div style="width: 100px; background: rgba(255,255,255,0.1); border-radius: 10px; height: 10px; overflow: hidden;">
                        <div style="width: {progress_percent}%; background: {color}; height: 100%; transition: width 0.3s ease;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 🏆 **Weekly Challenges**")
        
        weekly_challenges = [
            {"title": "🌟 Social Butterfly", "desc": "Meet 5 new people this week", "progress": 3, "total": 5, "reward": "Social Master Badge"},
            {"title": "🧠 Brain Booster", "desc": "Complete 20 study sessions", "progress": 14, "total": 20, "reward": "Study Streak Crown"},
            {"title": "💖 Wellness Warrior", "desc": "Log positive mood 7 days straight", "progress": 4, "total": 7, "reward": "Mental Health Champion"},
            {"title": "🚀 Goal Crusher", "desc": "Achieve 10 daily mission streaks", "progress": 7, "total": 10, "reward": "Achievement Hunter Title"}
        ]
        
        for challenge in weekly_challenges:
            progress_percent = (challenge["progress"] / challenge["total"]) * 100
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(255, 0, 110, 0.1), rgba(131, 56, 236, 0.1)); 
                        border: 1px solid rgba(255, 0, 110, 0.3); padding: 1.5rem; margin: 1rem 0; 
                        border-radius: 15px; color: white;">
                <h4 style="margin: 0 0 0.5rem 0; color: #ff006e;">{challenge['title']}</h4>
                <p style="margin: 0 0 1rem 0; color: rgba(255,255,255,0.8);">{challenge['desc']}</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="flex: 1; background: rgba(255,255,255,0.1); border-radius: 10px; height: 15px; margin-right: 1rem; overflow: hidden;">
                        <div style="width: {progress_percent}%; background: linear-gradient(90deg, #ff006e, #8338ec); height: 100%; transition: width 0.3s ease;"></div>
                    </div>
                    <span style="color: #06ffa5; font-weight: bold;">{challenge['progress']}/{challenge['total']}</span>
                </div>
                <p style="margin: 0.5rem 0 0 0; color: #ffa726; font-size: 0.9rem;">🏆 Reward: {challenge['reward']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎮 **Your Stats**")
        
        # PLAYER LEVEL & XP
        current_xp = 2847
        level = 12
        next_level_xp = 3000
        xp_to_next = next_level_xp - current_xp
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #8338ec, #3a86ff); 
                    padding: 1.5rem; border-radius: 20px; text-align: center; color: white; margin-bottom: 1rem;">
            <h2 style="margin: 0; font-size: 3rem;">⭐ LEVEL {level}</h2>
            <p style="margin: 0.5rem 0; font-size: 1.2rem;">{current_xp} / {next_level_xp} XP</p>
            <div style="background: rgba(255,255,255,0.3); border-radius: 10px; height: 20px; overflow: hidden;">
                <div style="width: {(current_xp/next_level_xp)*100}%; background: #06ffa5; height: 100%; transition: width 0.3s ease;"></div>
            </div>
            <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.9);">{xp_to_next} XP to level up!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ACHIEVEMENT SHOWCASE
        st.markdown("### 🏅 **Recent Achievements**")
        
        achievements = [
            {"name": "First Contact", "icon": "🤝", "desc": "Met your first AI agent"},
            {"name": "Vibe Master", "icon": "🛡️", "desc": "Completed 50 vibe checks"},
            {"name": "Social Star", "icon": "⭐", "desc": "Made 10 new connections"},
            {"name": "Study Streak", "icon": "📚", "desc": "7-day study streak"},
            {"name": "Mood Tracker", "icon": "💙", "desc": "Logged mood for 30 days"}
        ]
        
        for achievement in achievements:
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
                        padding: 1rem; margin: 0.5rem 0; border-radius: 10px; color: white;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 2rem; margin-right: 1rem;">{achievement['icon']}</span>
                    <div>
                        <h5 style="margin: 0; color: #06ffa5;">{achievement['name']}</h5>
                        <p style="margin: 0; color: rgba(255,255,255,0.7); font-size: 0.9rem;">{achievement['desc']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # DAILY STREAK
        st.markdown("### 🔥 **Current Streaks**")
        
        streaks = {
            "Daily Login": 12,
            "Mission Complete": 8,
            "Mood Logging": 15,
            "Study Sessions": 5
        }
        
        for streak_name, days in streaks.items():
            st.markdown(f"""
            <div style="background: rgba(255, 0, 110, 0.1); border-left: 3px solid #ff006e; 
                        padding: 0.8rem; margin: 0.5rem 0; border-radius: 5px; color: white;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span>{streak_name}</span>
                    <span style="color: #06ffa5; font-weight: bold;">🔥 {days} days</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # QUICK ACTION BUTTONS
        st.markdown("### ⚡ **Quick Actions**")
        
        if st.button("🎯 **CLAIM DAILY REWARD**", use_container_width=True):
            st.balloons()
            st.success("🎉 +50 XP claimed! Daily bonus activated!")
        
        if st.button("🔄 **REFRESH MISSIONS**", use_container_width=True):
            st.info("🔄 New missions generated! Check your mission board!")
        
        if st.button("👥 **INVITE FRIENDS**", use_container_width=True):
            st.success("📱 Invite links generated! Share the AI squad experience!")

# 🚀 FOOTER WITH REAL-TIME UPDATES
st.markdown("""
---
<div style="background: linear-gradient(90deg, rgba(255,0,110,0.1), rgba(131,56,236,0.1)); 
            padding: 2rem; border-radius: 15px; text-align: center; margin-top: 2rem;">
    <h3 style="color: #06ffa5; margin: 0 0 1rem 0;">🤖 VibeSync AI Squad - Always Watching, Always Caring</h3>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div style="color: white; margin: 0.5rem;">
            <strong>🛡️ Vibe Checks:</strong> 1,247 today
        </div>
        <div style="color: white; margin: 0.5rem;">
            <strong>🎯 Connections Made:</strong> 89 this week
        </div>
        <div style="color: white; margin: 0.5rem;">
            <strong>💙 Mental Health Boosts:</strong> 456 this month
        </div>
        <div style="color: white; margin: 0.5rem;">
            <strong>📚 Study Sessions:</strong> 2,103 completed
        </div>
    </div>
    <p style="color: rgba(255,255,255,0.7); margin: 1rem 0 0 0; font-size: 0.9rem;">
        Your AI agents are continuously learning and evolving to serve you better. 
        Stay connected, stay protected, stay awesome! ✨
    </p>
</div>
""", unsafe_allow_html=True)

# 🎵 BACKGROUND MUSIC WIDGET (OPTIONAL)
with st.expander("🎵 **Vibe Music Player** (Optional Background Beats)"):
    music_choice = st.selectbox("Choose your coding/studying vibe:", [
        "🎧 Lo-Fi Hip Hop Beats",
        "🌊 Ambient Nature Sounds", 
        "🎹 Piano Focus Music",
        "🔥 Upbeat Electronic",
        "😌 Meditation Sounds"
    ])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶️ Play"):
            st.success(f"🎵 Now playing: {music_choice}")
    with col2:
        if st.button("⏸️ Pause"):
            st.info("⏸️ Music paused")
    with col3:
        if st.button("🔀 Shuffle"):
            st.info("🔀 Shuffling playlist...")

# AUTO-REFRESH COMPONENT (for real-time updates)
st.empty()
time.sleep(1)
st.rerun()