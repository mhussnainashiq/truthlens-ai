
from enum import Enum

from pydantic import BaseModel, Field


class OverallAssessment(str, Enum):
    APPEARS_CREDIBLE = "appears_credible"
    POTENTIALLY_MISLEADING = "potentially_misleading"
    POTENTIALLY_FALSE = "potentially_false"
    MIXED_EVIDENCE = "mixed_evidence"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


class ClaimAssessment(str, Enum):
    SUPPORTED = "supported"
    CONTRADICTED = "contradicted"
    PARTIALLY_SUPPORTED = "partially_supported"
    MIXED_EVIDENCE = "mixed_evidence"
    UNVERIFIED = "unverified"
    OPINION = "opinion"
    PREDICTION = "prediction"


class EvidenceQuality(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    LIMITED = "limited"
    NONE = "none"


class BiasLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    INSUFFICIENT_DATA = "insufficient_data"


class SourceEvidence(BaseModel):
    title: str
    publisher: str = "Unknown"
    url: str = ""
    publication_date: str | None = None
    finding: str
    relevance: str = ""


class ClaimResult(BaseModel):
    claim: str
    assessment: ClaimAssessment
    explanation: str
    supporting_sources: list[SourceEvidence] = Field(
        default_factory=list
    )
    contradicting_sources: list[SourceEvidence] = Field(
        default_factory=list
    )
    related_sources: list[SourceEvidence] = Field(
        default_factory=list
    )
    missing_evidence: list[str] = Field(default_factory=list)


class BiasAnalysis(BaseModel):
    level: BiasLevel = BiasLevel.INSUFFICIENT_DATA
    indicators: list[str] = Field(default_factory=list)
    explanation: str


class CredibilityReport(BaseModel):
    overall_assessment: OverallAssessment
    summary: str
    evidence_quality: EvidenceQuality
    claims: list[ClaimResult] = Field(default_factory=list)
    bias_analysis: BiasAnalysis
    red_flags: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    recommended_checks: list[str] = Field(default_factory=list)
    demo_mode: bool = False


class AnalysisRequest(BaseModel):
    text: str = Field(min_length=1, max_length=15000)
    headline: str = Field(default="", max_length=500)
    source_url: str = Field(default="", max_length=2048)
    content_type: str = "general_claim"


class AnalysisRecord(BaseModel):
    id: int
    headline: str
    content_type: str
    assessment: str
    created_at: str
