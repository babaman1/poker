import streamlit as st
from calculator import PokerCalculator
import plotly.graph_objects as go

# --- Config ---
st.set_page_config(
    page_title="Poker Odds", 
    page_icon="♠️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS (Ultra-Luxury Casino Theme) ---
st.markdown("""
<style>
    /* Global Font & Reset */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #E0E0E0;
    }
    
    /* Background & Main Container */
    .stApp {
        background-color: #050505;
        background-image: 
            radial-gradient(circle at 50% 0%, rgba(212, 175, 55, 0.15) 0%, transparent 50%),
            url("https://www.transparenttextures.com/patterns/cubes.png");
        background-attachment: fixed;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 8rem; /* Space for bottom panel */
        max-width: 600px; /* Mobile focused */
        margin: 0 auto;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* --- Typography --- */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cinzel', serif;
        color: #D4AF37 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    
    .section-label {
        color: #888;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-align: center;
        margin-bottom: 15px;
        margin-top: 25px;
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        line-height: 0.1em;
    }
    
    .section-label span {
        background: #050505;
        padding: 0 10px;
    }

    /* --- Card Styles --- */
    .poker-card {
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        pointer-events: none;
        background: linear-gradient(145deg, #1e1e1e, #0a0a0a);
        border: 1px solid #333;
    }
    
    /* Board Cards */
    .board-card {
        height: 75px;
        width: 100%;
        border: 1px solid rgba(212, 175, 55, 0.3);
    }
    
    /* Hero Cards */
    .hero-card {
        background: linear-gradient(135deg, #0f2e1d 0%, #05140b 100%);
        border: 1px solid #D4AF37;
        height: 150px;
        margin-top: 10px;
        box-shadow: 
            0 0 15px rgba(212, 175, 55, 0.1),
            0 15px 30px rgba(0,0,0,0.7);
    }
    
    /* Card Content */
    .card-rank {
        font-family: 'Cinzel', serif;
        font-size: 26px;
        font-weight: 700;
        line-height: 1;
    }
    
    .hero-card .card-rank {
        font-size: 48px;
    }
    
    .card-suit {
        font-size: 22px;
        line-height: 1;
        margin-top: 2px;
    }
    
    .hero-card .card-suit {
        font-size: 40px;
        margin-top: 5px;
    }
    
    .card-empty {
        color: #333;
        font-size: 14px;
        font-family: 'Cinzel', serif;
        letter-spacing: 1px;
    }
    
    /* Colors */
    .suit-red { 
        color: #ff4d4d; 
        text-shadow: 0 0 8px rgba(255, 77, 77, 0.4); 
    }
    .suit-black { 
        color: #D4AF37; 
        text-shadow: 0 0 8px rgba(212, 175, 55, 0.4); 
    }
    
    /* --- Bottom Panel --- */
    .bottom-panel {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 500px;
        height: 80px;
        background: rgba(20, 20, 20, 0.85);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        z-index: 999;
        padding: 10px 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }
    
    /* Streamlit Widget Styling Overrides */
    .stSlider {
        width: 100%;
    }
    .stSlider > div > div > div > div {
        background-color: #D4AF37 !important;
    }
    .stSlider > div > div > div > div > div {
        background-color: #fff !important;
        border: 2px solid #D4AF37;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
    }
    .stSlider label {
        color: #D4AF37 !important;
        font-family: 'Cinzel', serif;
        font-size: 14px;
    }
    
    /* Buttons */
    .stButton button {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(212, 175, 55, 0.5);
        color: #D4AF37;
        border-radius: 8px;
        transition: all 0.3s;
        font-family: 'Cinzel', serif;
    }
    .stButton button:hover {
        background: #D4AF37;
        color: #000;
        border-color: #D4AF37;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
    }
    
    /* Modal/Dialog */
    div[data-testid="stDialog"] {
        background-color: #0a0a0a;
        border: 1px solid #D4AF37;
        box-shadow: 0 0 50px rgba(0,0,0,0.9);
    }
    
</style>
""", unsafe_allow_html=True)

# --- State Initialization ---
if 'calculator' not in st.session_state:
    st.session_state.calculator = PokerCalculator()
if 'my_hand' not in st.session_state:
    st.session_state.my_hand = [None, None]
if 'community_cards' not in st.session_state:
    st.session_state.community_cards = [None] * 5
if 'num_players' not in st.session_state:
    st.session_state.num_players = 2
if 'num_simulations' not in st.session_state:
    st.session_state.num_simulations = 1000

# --- Helper Functions ---

def get_suit_icon(suit_code):
    return {'s': '♠', 'h': '♥', 'd': '♦', 'c': '♣'}.get(suit_code, '')

def render_card_html(card_str, is_hero=False):
    if not card_str:
        return f"""
            <div class="poker-card {'hero-card' if is_hero else 'board-card'}">
                <div class="card-empty"></div>
            </div>
        """
    
    rank = card_str[:-1]
    suit = card_str[-1]
    suit_icon = get_suit_icon(suit)
    color_class = "suit-red" if suit in ['h', 'd'] else "suit-black"
    
    return f"""
        <div class="poker-card {'hero-card' if is_hero else 'board-card'}">
            <div class="card-rank {color_class}">{rank}</div>
            <div class="card-suit {color_class}">{suit_icon}</div>
        </div>
    """

# --- Dialogs ---
@st.dialog("Select Card", width="large")
def select_card_dialog(slot_type, index):
    dialog_key = f"dialog_state_{slot_type}_{index}"
    if dialog_key not in st.session_state:
        st.session_state[dialog_key] = {'step': 'suit', 'selected_suit': None}
    
    state = st.session_state[dialog_key]

    used_cards = set()
    for c in st.session_state.my_hand:
        if c: used_cards.add(c)
    for c in st.session_state.community_cards:
        if c: used_cards.add(c)
        
    current_val = None
    if slot_type == 'hand':
        current_val = st.session_state.my_hand[index]
    else:
        current_val = st.session_state.community_cards[index]
    
    if current_val in used_cards:
        used_cards.remove(current_val)

    if state['step'] == 'suit':
        st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Select Suit</h3>", unsafe_allow_html=True)
        suits = [('♠ Spades', 's'), ('♥ Hearts', 'h'), ('♦ Diamonds', 'd'), ('♣ Clubs', 'c')]
        col1, col2 = st.columns(2)
        for i, (label, code) in enumerate(suits):
            with (col1 if i % 2 == 0 else col2):
                if st.button(label, key=f"suit_{code}_{slot_type}_{index}", use_container_width=True):
                    state['step'] = 'rank'
                    state['selected_suit'] = code
                    st.rerun()

    else:
        suit_code = state['selected_suit']
        suit_icon = get_suit_icon(suit_code)
        color_class = "suit-red" if suit_code in ['h', 'd'] else "suit-black"
        
        c_back, c_title = st.columns([1, 3])
        with c_back:
            if st.button("← Back", key=f"back_{slot_type}_{index}"):
                state['step'] = 'suit'
                state['selected_suit'] = None
                st.rerun()
        with c_title:
            st.markdown(f"<h3 style='margin:0; padding-top:5px;'>Select Rank <span class='{color_class}'>{suit_icon}</span></h3>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        cols = st.columns(4)
        for i, rank in enumerate(ranks):
            card_str = f"{rank}{suit_code}"
            is_disabled = card_str in used_cards
            with cols[i % 4]:
                if st.button(rank, key=f"rank_{card_str}_{slot_type}_{index}", disabled=is_disabled, use_container_width=True):
                    if slot_type == 'hand':
                        st.session_state.my_hand[index] = card_str
                    else:
                        st.session_state.community_cards[index] = card_str
                    del st.session_state[dialog_key]
                    st.rerun()

    st.divider()
    if st.button("Clear Card", type="primary", use_container_width=True, key=f"clear_{slot_type}_{index}"):
        if slot_type == 'hand':
            st.session_state.my_hand[index] = None
        else:
            st.session_state.community_cards[index] = None
        if dialog_key in st.session_state:
            del st.session_state[dialog_key]
        st.rerun()

# --- Main Logic ---
hero_hand = [c for c in st.session_state.my_hand if c is not None]
board = [c for c in st.session_state.community_cards if c is not None]
win_pct = 0
tie_pct = 0

if len(hero_hand) == 2:
    win_pct, tie_pct = st.session_state.calculator.calculate_equity(
        hero_hand, 
        board, 
        num_players=st.session_state.num_players,
        num_simulations=st.session_state.num_simulations
    )

# --- UI Layout ---

# 1. Gauge Section
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = win_pct,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "WIN PROBABILITY", 'font': {'size': 14, 'color': "#D4AF37", 'family': "Cinzel"}},
    number = {'suffix': "%", 'font': {'size': 50, 'color': "#fff", 'family': "Inter"}},
    gauge = {
        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#D4AF37", 'tickfont': {'color': '#D4AF37'}},
        'bar': {'color': "#D4AF37", 'thickness': 0.75},
        'bgcolor': "#0a0a0a",
        'borderwidth': 2,
        'bordercolor': "#333",
        'steps': [{'range': [0, 100], 'color': "#050505"}],
        'threshold': {'line': {'color': "#50C878", 'width': 4}, 'thickness': 1, 'value': win_pct}
    }
))

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font={'color': "#C9A75B"},
    margin=dict(t=30, b=10, l=20, r=20),
    height=220
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# 2. Controls (Moved Up)
st.markdown('<div class="section-label"><span>OPPONENTS AT TABLE</span></div>', unsafe_allow_html=True)

c_spacer, c_slider, c_spacer2 = st.columns([1, 8, 1])

with c_slider:
    opponents = st.slider(
        "Opponents at Table", 
        min_value=1, 
        max_value=8, 
        value=st.session_state.num_players - 1,
        label_visibility="collapsed"
    )
    st.session_state.num_players = opponents + 1

# 2. Board Section
st.markdown('<div class="section-label"><span>COMMUNITY CARDS</span></div>', unsafe_allow_html=True)

# CSS to force button overlay using negative margins
st.markdown("""
<style>
    /* Board Cards Overlay */
    /* Target buttons inside the columns that contain board cards */
    div[data-testid="column"] button {
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        height: 70px !important;
        width: 100% !important;
        margin-top: -75px !important; /* Pull button up over the card */
        position: relative !important;
        z-index: 5 !important;
    }
</style>
""", unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
cols = [c1, c2, c3, c4, c5]

for i in range(5):
    with cols[i]:
        st.markdown(render_card_html(st.session_state.community_cards[i], is_hero=False), unsafe_allow_html=True)
        # Empty label button for overlay
        if st.button(" ", key=f"btn_comm_{i}"):
            select_card_dialog("comm", i)

# 3. Hero Section
st.markdown('<div class="section-label"><span>YOUR HAND</span></div>', unsafe_allow_html=True)

col_left, h1, h2, col_right = st.columns([1, 2, 2, 1])

# We inject specific style for hero buttons to override the board button style
hero_btn_style = """
<style>
    div[data-testid="column"] button {
        height: 140px !important;
        margin-top: -145px !important;
    }
</style>
"""

with h1:
    st.markdown(render_card_html(st.session_state.my_hand[0], is_hero=True), unsafe_allow_html=True)
    st.markdown(hero_btn_style, unsafe_allow_html=True) # Apply override
    if st.button(" ", key="btn_hand_0"):
        select_card_dialog("hand", 0)

with h2:
    st.markdown(render_card_html(st.session_state.my_hand[1], is_hero=True), unsafe_allow_html=True)
    st.markdown(hero_btn_style, unsafe_allow_html=True) # Apply override
    if st.button(" ", key="btn_hand_1"):
        select_card_dialog("hand", 1)


