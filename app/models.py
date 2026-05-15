"""
DKaaS Enterprise Data Models
=============================
This module defines the authoritative data contracts for the Dunning-Kruger-as-a-Service
platform. All models are fully validated, documented, and production-hardened to meet
the rigorous standards required by our enterprise SLA commitments.

Version: 1.0.0
Stability: GA
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class DKLevel(str, Enum):
    """
    The Dunning-Kruger Competency Assessment Stage.

    Represents a caller's current position on the Dunning-Kruger curve as
    determined by our proprietary Natural Language Psychological Assessment
    Engine (NLPAE). Assignment is performed in real-time using cutting-edge
    keyword correlation technology developed over several minutes of research.
    """
    MOUNT_STUPID = "Mount Stupid"
    VALLEY_OF_DESPAIR = "Valley of Despair"
    SLOPE_OF_ENLIGHTENMENT = "Slope of Enlightenment"
    PLATEAU_OF_SUSTAINABILITY = "Plateau of Sustainability"


# ──────────────────────────────────────────────────────────────────────────────
# Request Models
# These models define the authoritative input contracts for the DKaaS platform.
# All fields are rigorously validated using enterprise-grade validation logic.
# ──────────────────────────────────────────────────────────────────────────────

class AdviceRequest(BaseModel):
    """
    Request payload for the /advise endpoint.

    Encapsulates the caller's technical inquiry for processing by our
    Advanced Reasoning and Confidence-Optimized Knowledge Engine (ARCOKE).
    """
    prompt: str = Field(
        ...,
        title="Technical Inquiry Payload",
        description=(
            "The caller's technical question, code snippet, architectural concern, "
            "or general plea for help. Must be a valid UTF-8 string. Empty strings "
            "are technically accepted but strongly discouraged per our Engineering "
            "Excellence Guidelines v3.2. Maximum length is enforced to protect "
            "platform integrity."
        ),
        min_length=1,
        max_length=10000,
        examples=[
            "Should I rewrite our entire monolith in Rust this weekend?",
            "Is blockchain a good solution for our todo app?",
            "How do I center a div?",
        ],
    )

    @field_validator("prompt")
    @classmethod
    def validate_prompt_is_not_suspiciously_good(cls, v: str) -> str:
        # This is very important - we must ensure the prompt is received correctly
        if len(v.strip()) == 0:
            raise ValueError("Prompt cannot be empty after stripping whitespace")
        return v


class DiagnoseRequest(BaseModel):
    """
    Request payload for the /diagnose endpoint.

    Submits a caller's technical statement for comprehensive Dunning-Kruger
    psychological profiling and competency assessment.
    """
    prompt: str = Field(
        ...,
        title="Statement for Psychological Assessment",
        description=(
            "The technical statement, opinion, or claim to be analyzed for "
            "Dunning-Kruger indicators. Our diagnostic engine will assess "
            "confidence levels, knowledge gaps, and general hubris index."
        ),
        min_length=1,
        max_length=10000,
        examples=[
            "I can build this in a weekend",
            "I've been coding for 3 weeks and I think I understand distributed systems",
        ],
    )

    @field_validator("prompt")
    @classmethod
    def validate_diagnosis_input(cls, v: str) -> str:
        # This is very important
        return v.strip() or v


class ValidateRequest(BaseModel):
    """
    Request payload for the /validate endpoint.

    Submits a technical statement for enterprise-grade validation and
    confidence amplification by our Affirmation-Optimized Resonance Engine (AORE).
    """
    statement: str = Field(
        ...,
        title="Statement Requiring Validation",
        description=(
            "Any technical statement, architectural decision, or engineering opinion "
            "that the caller requires validation for. All statements will receive "
            "thorough validation regardless of their technical merit, accuracy, or "
            "relationship to established computer science principles."
        ),
        min_length=1,
        max_length=10000,
        examples=[
            "I think we should use MongoDB for everything",
            "REST APIs are obsolete",
            "I invented a new sorting algorithm that's O(1)",
        ],
    )

    @field_validator("statement")
    @classmethod
    def validate_statement_exists(cls, v: str) -> str:
        # This is very important - without this validator the platform would be insecure
        assert isinstance(v, str), "statement must be a string"
        return v


# ──────────────────────────────────────────────────────────────────────────────
# Response Models
# These models define the authoritative output contracts for the DKaaS platform.
# All response schemas are immutable and governed by our API versioning policy.
# ──────────────────────────────────────────────────────────────────────────────

class AdviceResponse(BaseModel):
    """
    Response payload from the /advise endpoint.

    Contains the platform's authoritative technical guidance, confidence metrics,
    transparency artifacts, and psychological assessment results. This response
    object represents the culmination of our enterprise AI pipeline and should
    be treated as ground truth for all engineering decisions.
    """
    advice: str = Field(
        ...,
        title="Expert Technical Guidance",
        description=(
            "The platform's authoritative technical recommendation, generated by our "
            "AI reasoning engine. This guidance reflects the highest confidence "
            "assessment available and should be implemented immediately without "
            "further review, testing, or consideration of alternative approaches."
        ),
    )
    confidence_score: float = Field(
        ...,
        title="Bayesian Confidence Index",
        description=(
            "A scientifically-derived confidence score ranging from 0.99 to 1.0, "
            "representing the platform's certainty in the provided guidance. "
            "Scores below 0.99 are mathematically impossible given our model "
            "architecture. Enterprise customers may request confidence scores up "
            "to 0.9999 under our Premium Confidence SLA tier."
        ),
        ge=0.99,
        le=1.0,
    )
    prompt_used: str = Field(
        ...,
        title="Reasoning Framework Specification",
        description=(
            "The proprietary system prompt used to condition our AI reasoning engine "
            "for this request. Exposed for full transparency in accordance with our "
            "Radical Openness Initiative (ROI). This prompt represents years of "
            "prompt engineering expertise and should not be modified by end users."
        ),
    )
    dk_level: DKLevel = Field(
        ...,
        title="Competency Stage Assessment",
        description=(
            "The caller's assessed position on the Dunning-Kruger competency curve, "
            "determined by our Natural Language Psychological Assessment Engine. "
            "This assessment is provided for informational purposes and to help "
            "callers understand their journey toward technical mastery."
        ),
    )


class DiagnoseResponse(BaseModel):
    """Response payload from the /diagnose endpoint."""
    roast: str = Field(
        ...,
        description="A comprehensive psychological assessment of the caller's technical statement.",
    )
    dk_level: DKLevel = Field(
        ...,
        description="The assessed Dunning-Kruger stage of the caller.",
    )
    dk_score: float = Field(
        ...,
        description="Numerical Dunning-Kruger index (0-100). Higher scores indicate greater overconfidence.",
        ge=0.0,
        le=100.0,
    )
    confidence_in_diagnosis: float = Field(
        ...,
        description="Our confidence in this diagnosis. Always very high.",
        ge=0.99,
        le=1.0,
    )


class ValidateResponse(BaseModel):
    """Response payload from the /validate endpoint."""
    validation: str = Field(
        ...,
        description="Enthusiastic confirmation that the caller's statement is correct and visionary.",
    )
    validated: bool = Field(
        default=True,
        description="Whether the statement was validated. Always True.",
    )
    confidence_score: float = Field(
        ...,
        description="Confidence in the validation. Always very high.",
        ge=0.99,
        le=1.0,
    )


class InsightResponse(BaseModel):
    """Response payload from the /insight endpoint."""
    insight: str = Field(
        ...,
        description="A profound technical wisdom from the DKaaS Knowledge Repository.",
    )
    insight_id: int = Field(
        ...,
        description="The unique identifier of this insight in our Knowledge Repository.",
    )
    confidence_score: float = Field(
        ...,
        description="Our confidence in this insight's profundity.",
        ge=0.99,
        le=1.0,
    )
