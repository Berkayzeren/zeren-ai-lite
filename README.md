# Zeren AI Lite (Advanced Portfolio Edition)

Zeren AI Lite is an open-source, lightweight version of the commercial **Zeren AI** project, designed to showcase advanced architectural patterns and autonomous engineering practices.

> [!IMPORTANT]
> **Note:** This repository contains the core architectural skeleton, asynchronous communication infrastructure, and risk management logic. Proprietary trading algorithms, deep learning models, and datasets are kept private.

## 🌟 Key Features

Zeren AI Lite is designed not just as a trading bot, but as a fully **asynchronous autonomous system**:

- **Auditability:** The `Journal` module ensures every decision (Signal, Risk, Sentiment) is permanently stored as structured JSON in the `logs/` directory.
- **System Monitoring (Heartbeat):** The `Monitoring` module tracks the health and latency of all sub-components in real-time.
- **Data Governance:** Standardized data flow using **Pydantic** models (`SignalData`, `RiskReport`, `TradeDecision`) for strict type safety.
- **Sentiment-Driven Decisions:** Integrated news and social media sentiment analysis (`SentimentAnalyzer`) as a critical decision layer.
- **Hybrid Risk Protection:** Combines rule-based safety checks with simulated neural anomaly detection (`NeuralRiskGuard`).
- **Event-Driven Architecture:** Uses a central `EventBus` for decoupled communication between services.

## 🏗️ Architectural Flow

The autonomous decision cycle follows this path:
**Market Data** -> **Sentiment Analysis** -> **Signal Generation** -> **Hybrid Risk Check** -> **Portfolio Optimization** -> **Final Standardized Decision** -> **Journaling & Event-Bus Execution**.

```mermaid
graph TD
    Data[Market Data] --> Sent[Sentiment Analysis]
    Sent --> Sig[Signal Engine]
    Sig --> Risk[Hybrid Risk Guard]
    Risk --> Opt[Portfolio Optimizer]
    Opt --> Decision[Standardized Decision]
    Decision --> Journal[Decision Journaling]
    Decision --> Bus[Event Bus]
    Bus --> Exec[Execution Simulation]
    Exec --> Heart[Heartbeat/Monitoring]
```

## 📂 Technical Structure

- `src/core/`:
    - `data_models.py`: Pydantic schemas for standardization.
    - `journal.py`: Decision audit trail.
    - `monitoring.py`: System health (Heartbeat).
    - `event_bus.py`: Async Pub/Sub communication.
- `src/strategy/`:
    - `sentiment_analyzer.py`: News sentiment simulation.
    - `risk_manager.py`: Kelly Criterion & Volatility management.
    - `neural_risk_guard.py`: Hybrid anomaly detection.
- `logs/`: Directory for persistent decision journals.

## 🛠️ Getting Started

1. **Install Dependencies:** `pip install -r requirements.txt` (Pydantic and Pytest required).
2. **Launch:** `python3 main.py`
3. **Verify:** Check the `logs/` directory to see the "recorded thoughts" of the system.

---
*© 2026 Zeren AI - Autonomous Engineering Manifesto*
