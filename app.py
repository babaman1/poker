import streamlit as st
from calculator import PokerCalculator
import plotly.graph_objects as go

# --- Config ---
st.set_page_config(page_title="Poker Odds", page_icon="♠️", layout="centered")

# --- Custom CSS ---
st.markdown("""
<style>
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    .card-container {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        margin: 5px;
        height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .card-rank {
        font-size: 24px;
        font-weight: bold;
        line-height: 1;
    }
    .card-suit {
        font-size: 28px;
        line-height: 1;
    }
    .red { color: #d32f2f; }
    .black { color: #212121; }
    .empty-card {
        border: 2px dashed #666;
        background-color: rgba(255,255,255,0.1);
        color: #888;
    }
</style>
""", unsafe_allow_html=True)

# Initialize state
if 'calculator' not in st.session_state:
    st.session_state.calculator = PokerCalculator()
if 'my_hand' not in st.session_state:
    st.session_state.my_hand = [None, None]
if 'community_cards' not in st.session_state:
    st.session_state.community_cards = [None] * 5
if 'selected_suit' not in st.session_state:
    st.session_state.selected_suit = None
if 'active_slot' not in st.session_state:
    st.session_state.active_slot = None # (type, index) e.g. ('hand', 0)

# --- Helper Functions ---
def render_card(card_str, slot_type, index):
    if card_str:
        rank = card_str[:-1]
        suit = card_str[-1]
        suit_icon = {'s': '♠️', 'h': '♥️', 'd': '♦️', 'c': '♣️'}[suit]
        color_class = "red" if suit in ['h', 'd'] else "black"
        
        html = f"""
        <div class="card-container">
            <div class="card-rank {color_class}">{rank}</div>
            <div class="card-suit {color_class}">{suit_icon}</div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
        if st.button("🗑️", key=f"del_{slot_type}_{index}"):
            if slot_type == 'hand':
                st.session_state.my_hand[index] = None
            else:
                st.session_state.community_cards[index] = None
            st.rerun()
    else:
        # Empty slot button
        is_active = st.session_state.active_slot == (slot_type, index)
        label = "Select" if not is_active else "Waiting..."
        if st.button(label, key=f"sel_{slot_type}_{index}"):
            st.session_state.active_slot = (slot_type, index)
            st.session_state.selected_suit = None # Reset suit selection
            st.rerun()

def add_card(rank):
    if st.session_state.active_slot and st.session_state.selected_suit:
        slot_type, index = st.session_state.active_slot
        card_str = f"{rank}{st.session_state.selected_suit}"
        
        if slot_type == 'hand':
            st.session_state.my_hand[index] = card_str
        else:
            st.session_state.community_cards[index] = card_str
            
        # Reset selection
        st.session_state.active_slot = None
        st.session_state.selected_suit = None
        st.rerun()

def reset_game():
    st.session_state.my_hand = [None, None]
    st.session_state.community_cards = [None] * 5
    st.session_state.active_slot = None
    st.session_state.selected_suit = None

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    num_players = st.slider("Players", 2, 9, 2)
    opponent_style = st.selectbox("Opponent Style", ["Random", "Tight", "Aggressive"])
    if st.button("Reset Game 🔄"):
        reset_game()
        st.rerun()

# --- Main UI ---
st.title("🃏 Poker Odds")

# 1. Hand Section
st.subheader("My Hand")
cols = st.columns(2)
for i in range(2):
    with cols[i]:
        render_card(st.session_state.my_hand[i], 'hand', i)

# 2. Community Cards Section
st.subheader("Community Cards")
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        render_card(st.session_state.community_cards[i], 'comm', i)

# 3. Card Selector (Only visible if a slot is active)
if st.session_state.active_slot:
    st.divider()
    st.markdown("#### Select Card")
    
    # Suit Selection
    cols = st.columns(4)
    suits = {'s': '♠️', 'h': '♥️', 'd': '♦️', 'c': '♣️'}
    for i, (code, icon) in enumerate(suits.items()):
        with cols[i]:
            # Highlight selected suit
            type = "primary" if st.session_state.selected_suit == code else "secondary"
            if st.button(icon, key=f"suit_{code}", type=type):
                st.session_state.selected_suit = code
                st.rerun()
    
    # Rank Selection (Only if suit is selected)
    if st.session_state.selected_suit:
        st.markdown("---")
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        cols = st.columns(7) # 2 rows roughly
        for i, rank in enumerate(ranks):
            with cols[i % 7]:
                if st.button(rank, key=f"rank_{rank}"):
                    add_card(rank)

# 4. Calculation & Gauge
st.divider()
hero_hand = [c for c in st.session_state.my_hand if c is not None]
board = [c for c in st.session_state.community_cards if c is not None]

if len(hero_hand) == 2:
    # Calculate
    win_pct, tie_pct = st.session_state.calculator.calculate_equity(
        hero_hand, board, num_players=num_players, opponent_style=opponent_style
    )
    
    # Gauge Chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = win_pct,
        title = {'text': "Win Probability"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "white"},
            'steps': [
                {'range': [0, 30], 'color': "#ef5350"}, # Red
                {'range': [30, 70], 'color': "#ffca28"}, # Yellow
                {'range': [70, 100], 'color': "#66bb6a"} # Green
            ],
        }
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)
    
    if tie_pct > 0:
        st.caption(f"Tie Probability: {tie_pct:.1f}%")

else:
    st.info("Select 2 cards to see odds.")
