# Zeren AI Lite (Advanced Portfolio Edition)

Zeren AI Lite is an open-source, lightweight version of the commercial **Zeren AI** project, designed to showcase advanced architectural patterns, autonomous engineering practices, and global software standards.

> [!IMPORTANT]
> **Note:** This repository contains the core architectural skeleton, asynchronous communication infrastructure, and risk management logic. Proprietary trading algorithms, deep learning models, and datasets are kept private.

## 🌟 Key Features

Zeren AI Lite is designed not just as a trading bot, but as a fully **asynchronous autonomous system**:

- **🌍 Global Standards:** Fully English codebase, documentation, and logging, following international software engineering best practices.
- **🛡️ Auditability:** The `Journal` module ensures every decision (Signal, Risk, Sentiment) is permanently stored as structured JSON in the `logs/` directory for full transparency.
- **💓 System Monitoring (Heartbeat):** The `Monitoring` module tracks the health and latency of all sub-components in real-time via a heartbeat mechanism.
- **📊 Data Governance:** Standardized data flow using **Pydantic** models (`SignalData`, `RiskReport`, `TradeDecision`) for strict type safety and validation.
- **🧠 Sentiment-Driven Decisions:** Integrated news and social media sentiment analysis (`SentimentAnalyzer`) as a critical decision layer, with API key readiness.
- **🔒 Hybrid Risk Protection:** Combines rule-based safety checks with simulated neural anomaly detection (`NeuralRiskGuard`).
- **⚡ Event-Driven Architecture:** Uses a central, asynchronous `EventBus` for decoupled communication between services.

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
    - `sentiment_analyzer.py`: News sentiment simulation & API integration.
    - `risk_manager.py`: Kelly Criterion & Volatility management.
    - `neural_risk_guard.py`: Hybrid anomaly detection.
- `logs/`: Directory for persistent decision journals.

## ⚙️ Configuration

Copy the `.env.example` file to `.env` and configure your API keys:
```bash
cp .env.example .env
```
Key configurations include:
- `SENTIMENT_API_KEY`: For real-time news analysis (Demo mode active if empty).
- `STOCK_API_KEY` / `CRYPTO_API_KEY`: Placeholders for data providers.

## 🛠️ Installation & Usage

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Launch the Engine:**
   ```bash
   python3 main.py
   ```
3. **Run Tests:**
   ```bash
   PYTHONPATH=. pytest tests/
   ```

---
*© 2026 Zeren AI - Autonomous Engineering Manifesto*
