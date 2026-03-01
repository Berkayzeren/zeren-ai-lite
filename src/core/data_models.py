from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ExplainabilityPacket(BaseModel):
    """
    XAI (Explainable AI) Packet.
    Contains breakdown of why a certain decision was made.
    """

    primary_factor: str
    contributions: Dict[str, float]
    logic_path: List[str]
    model_certainty: float


class SignalData(BaseModel):
    """
    Signal Data Model.
    Standardizes raw signal data from strategy modules.
    """

    ticker: str
    action: str = Field(..., description="BUY, SELL, or HOLD")
    confidence: float = Field(..., ge=0.0, le=1.0)
    price: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    strategy_name: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RiskReport(BaseModel):
    """
    Risk Assessment Model.
    Combines outputs from RiskManager and NeuralGuard.
    """

    is_valid: bool
    risk_level: int
    status: str
    reason: str
    suggested_multiplier: float = 1.0
    attributions: Dict[str, float] = Field(
        default_factory=dict, description="Factor weights in risk decision"
    )
    timestamp: datetime = Field(default_factory=datetime.now)


class TradeDecision(BaseModel):
    """
    Final Decision Model.
    Represents the ultimate decision after passing through Signal, Risk, and Optimization layers.
    """

    ticker: str
    decision: str  # EXECUTE, REJECT, WATCH
    signal: SignalData
    risk: RiskReport
    weight: float
    reason: str
    explanation: Optional[ExplainabilityPacket] = None
    timestamp: datetime = Field(default_factory=datetime.now)
