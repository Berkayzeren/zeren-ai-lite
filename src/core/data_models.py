from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class SignalData(BaseModel):
    """
    Sinyal Veri Modeli.
    Strateji modüllerinden çıkan ham sinyal verilerini standardize eder.
    """

    ticker: str
    action: str = Field(..., description="BUY, SELL veya HOLD")
    confidence: float = Field(..., ge=0.0, le=1.0)
    price: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    strategy_name: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RiskReport(BaseModel):
    """
    Risk Değerlendirme Modeli.
    RiskManager ve NeuralGuard çıktılarını birleştirir.
    """

    is_valid: bool
    risk_level: int
    status: str
    reason: str
    suggested_multiplier: float = 1.0
    timestamp: datetime = Field(default_factory=datetime.now)


class TradeDecision(BaseModel):
    """
    Final Karar Modeli.
    Sinyal, Risk ve Optimizasyon katmanlarından geçen nihai kararı temsil eder.
    """

    ticker: str
    decision: str  # EXECUTE, REJECT, WATCH
    signal: SignalData
    risk: RiskReport
    weight: float
    reason: str
    timestamp: datetime = Field(default_factory=datetime.now)
