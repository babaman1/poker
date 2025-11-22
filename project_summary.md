# Poker Odds Calculator - Project Summary

## Overview
A mobile-friendly web application built with **Python** and **Streamlit** that calculates win probabilities for Texas Hold'em poker hands in real-time.

## Key Features
- **Core Logic**: Uses Monte Carlo simulation (via `treys` library) to estimate equity.
- **Advanced Settings**:
    - Adjustable number of players (2-9).
    - Opponent modeling: "Random", "Tight" (top hands only), or "Aggressive".
- **Visualizations**:
    - **Gauge Chart**: Speedometer-style display for Win Probability (using `plotly`).
    - **CSS Cards**: Custom-styled HTML/CSS components representing playing cards.

## Current UI/UX (Single Screen Layout)
The app is designed for mobile usage with a vertical flow:
1.  **Top**: Win Probability Gauge (Immediate feedback).
2.  **Middle**: Community Cards (The Board).
3.  **Bottom**: My Hand (Hero cards).
4.  **Interaction**: Clicking a card slot opens a **Modal Dialog** (`st.dialog`) to select Suit and Rank, keeping the main interface clean and preventing layout shifts.

## Tech Stack
- **Frontend/Backend**: Streamlit (Python)
- **Poker Logic**: `treys`
- **Charting**: `plotly`
- **Deployment**: Streamlit Cloud (connected to GitHub)

## Goal for Design Consultation
The app is functional and deployed, but we want to refine the **Visual Design** and **Layout Hierarchy** to make it feel more like a premium native app (e.g., "Casino" or "Dark Mode" aesthetic, better spacing, animations).
