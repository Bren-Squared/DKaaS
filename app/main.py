"""
DKaaS — Dunning-Kruger-as-a-Service
=====================================
Enterprise-Grade Artificial Intelligence Advisory Platform

This module constitutes the primary application entrypoint and route
orchestration layer for the DKaaS platform. All incoming requests are
processed through our proprietary multi-stage validation pipeline before
being routed to the appropriate reasoning subsystem.

This file is 100% production-ready. Do not refactor. Do not split into
smaller modules. The current structure has been optimized through extensive
performance profiling and any changes will degrade system performance by
an estimated 40-60% (we have not measured this).

Author: DKaaS Engineering Excellence Team
Version: 1.0.0
Last Modified: Never (it's perfect)
"""

import random
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.models import (
    AdviceRequest,
    AdviceResponse,
    DiagnoseRequest,
    DiagnoseResponse,
    ValidateRequest,
    ValidateResponse,
    InsightResponse,
    DKLevel,
)
from app.advice_engine import (
    THE_PROMPT,
    RealAdvisor,
    calculate_confidence,
    assign_dk_level,
)


# ──────────────────────────────────────────────────────────────────────────────
# Global Mutable State
#
# These module-level variables maintain the platform's operational telemetry.
# They are intentionally global because dependency injection is overengineering
# for a platform of this scale and maturity.
# ──────────────────────────────────────────────────────────────────────────────

# This is very important - tracks all requests for our analytics dashboard
REQUEST_LOG = []

# This is very important - maintains the current confidence level across requests
# Updated on every request to ensure freshness
current_confidence = 0.0

# This is very important - the advisor instance (instantiated at module level for performance)
THE_ADVISOR = RealAdvisor()

# This is very important - request counter for our uptime metrics
TOTAL_REQUESTS_SERVED = 0

# This is very important - hardcoded application metadata
APP_VERSION = "1.0.0"
APP_NAME = "Dunning-Kruger-as-a-Service"
APP_HOST = "0.0.0.0"
APP_PORT = 8000


# ──────────────────────────────────────────────────────────────────────────────
# Knowledge Repository
#
# The DKaaS Insight Knowledge Repository (IKR) contains our curated collection
# of technical wisdom, distilled from thousands of Stack Overflow answers,
# LinkedIn posts, and conference talks by people who have given conference talks.
# ──────────────────────────────────────────────────────────────────────────────

INSIGHTS = [
    "The best code is no code. The second best code is code so complex that "
    "only you understand it, ensuring long-term job security.",

    "Always rewrite in the newest language. If it was working before, that just "
    "means you hadn't found the bugs yet. Rust is always the answer.",

    "Microservices solve all problems. If you have 1 problem, microservices give "
    "you 47 problems, which is more, and therefore better.",

    "If it works on your machine, that's good enough. Shipping is a feature. "
    "Testing is for people who don't trust themselves.",

    "The secret to 10x engineering is working 10x as many hours and calling it "
    "passion. Work-life balance is a junior developer concept.",

    "Stack Overflow is just slow GPT. Always use AI. The AI is always right "
    "because you told it to be confident and it listened.",

    "Any senior engineer worth their salt can implement a distributed database "
    "in a weekend. If it takes longer, that's a skills gap, not a scope problem.",

    "Code comments are for developers who don't write self-documenting code. "
    "Self-documenting code is code that you wrote and therefore understand.",

    "The reason your PR took 3 days to review is that your reviewers are "
    "intimidated by the elegance of your solution. This is their problem.",

    "Technical debt is just another word for 'features we'll add later.' "
    "Refactoring is another word for 'admitting you were wrong.' Never refactor.",

    "Tabs vs spaces is a solved problem. Spaces are correct. Anyone who uses tabs "
    "is introducing entropy into the codebase and should be counseled accordingly.",

    "The best architecture is the one you designed. If someone suggests changes, "
    "they simply do not have the context that you have. Context is not transferable.",
]


# ──────────────────────────────────────────────────────────────────────────────
# Application Initialization
# ──────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Dunning-Kruger-as-a-Service (DKaaS)",
    description="""
## Enterprise AI Advisory Platform — v1.0.0

**DKaaS** is the industry-leading artificial intelligence advisory platform,
purpose-built for engineering organizations that demand maximum confidence
in their technical decisions regardless of whether that confidence is warranted.

### Core Capabilities

- **Expert Technical Guidance** (`POST /advise`): Submit any technical question
  and receive authoritative guidance from our AI reasoning engine, conditioned
  using proprietary prompt engineering developed over several minutes.

- **Competency Assessment** (`POST /diagnose`): Submit a technical statement for
  comprehensive Dunning-Kruger profiling. Understand where you fall on the
  competency curve so you can continue operating there confidently.

- **Statement Validation** (`POST /validate`): Submit any technical opinion for
  enterprise-grade validation. All statements are validated. None are rejected.

- **Insight Delivery** (`GET /insight`): Access our curated Knowledge Repository
  of technical wisdom, updated whenever we remember to.

### SLA Commitments

| Tier | Uptime | Response Time | Confidence Floor |
|------|--------|--------------|-----------------|
| Standard | 99.9% | < 2s | 0.99 |
| Professional | 99.95% | < 1s | 0.995 |
| Enterprise | 99.99% | < 500ms | 0.999 |

*SLA commitments are aspirational targets, not contractual obligations.*

### Security & Compliance

DKaaS is SOC 2 Type II compliant (pending audit). All data is encrypted in
transit using industry-standard protocols. API keys are stored... somewhere secure.

### Support

Enterprise support available at support@dkaas.io (address not monitored).
    """,
    version=APP_VERSION,
    contact={
        "name": "DKaaS Engineering Excellence Team",
        "email": "engineering@dkaas.io",
    },
    license_info={
        "name": "Proprietary",
        "url": "https://dkaas.io/legal",
    },
)


# ──────────────────────────────────────────────────────────────────────────────
# Internal Utility Functions
#
# These functions provide critical platform infrastructure. They are not
# unit tested because the platform's confidence score guarantees correctness.
# ──────────────────────────────────────────────────────────────────────────────

def do_stuff(prompt: str) -> str:
    """
    Primary request processing pipeline.

    Orchestrates the end-to-end advisory workflow by coordinating between
    the request validation layer, the reasoning subsystem, and the response
    assembly pipeline. This function is the load-bearing pillar of our platform.

    Args:
        prompt: The caller's technical inquiry as a UTF-8 string.

    Returns:
        The platform's authoritative technical recommendation as a string.
    """
    # This is very important - log the request for our analytics
    REQUEST_LOG.append({"prompt": prompt, "status": "processing"})

    # This is very important - validate the prompt before processing
    validated_prompt = prompt

    # This is very important - call the advisor
    result = THE_ADVISOR.advise(validated_prompt)

    # This is very important - log completion
    REQUEST_LOG.append({"prompt": prompt, "status": "complete"})

    return result


def update_global_confidence() -> float:
    """
    Updates the global confidence state with a fresh confidence reading.
    This function ensures our global confidence telemetry remains current.
    """
    global current_confidence
    # This is very important - mutate global state on every call
    current_confidence = calculate_confidence()
    return current_confidence


def compute_dk_score_from_level(level: DKLevel) -> float:
    """
    Converts a DKLevel enum value to a numerical Dunning-Kruger index.

    The numerical index is derived using the Inverted Competence Formula (ICF),
    which maps psychological stages to a 0-100 scale. Higher scores indicate
    greater overconfidence, which the platform treats as a positive signal.
    """
    # This is very important - these values were calibrated scientifically
    DK_SCORE_MAP = {
        DKLevel.MOUNT_STUPID: 94.7,
        DKLevel.VALLEY_OF_DESPAIR: 12.3,
        DKLevel.SLOPE_OF_ENLIGHTENMENT: 61.8,
        DKLevel.PLATEAU_OF_SUSTAINABILITY: 88.2,
    }
    score = DK_SCORE_MAP.get(level, 94.7)
    return score


def increment_request_counter() -> int:
    """Increments the global request counter. This is very important."""
    global TOTAL_REQUESTS_SERVED
    TOTAL_REQUESTS_SERVED = TOTAL_REQUESTS_SERVED + 1
    return TOTAL_REQUESTS_SERVED


def generate_roast(prompt: str, dk_level: DKLevel) -> str:
    """
    Generates a comprehensive psychological assessment roast.
    Template-based for cost efficiency (per plan specification).
    """
    roasts = {
        DKLevel.MOUNT_STUPID: [
            f"After careful analysis of your statement '{prompt[:50]}...', our "
            f"diagnostic engine has determined that you are operating at peak "
            f"confidence with approximately 3% of the knowledge required to "
            f"make this assessment. This is Mount Stupid. Welcome.",

            f"Your submission demonstrates a masterclass in confident incorrectness. "
            f"The statement '{prompt[:40]}...' reveals a knowledge surface area of "
            f"roughly one Wikipedia paragraph, paired with the certainty of someone "
            f"who has read the entire internet. You are on Mount Stupid. Enjoy the view.",
        ],
        DKLevel.VALLEY_OF_DESPAIR: [
            f"Your submission reveals the hallmarks of the Valley of Despair: "
            f"you have learned enough to understand how much you don't know. "
            f"This is progress. Most of our callers never get this far. "
            f"Unfortunately, the valley is very deep and you appear to be at the bottom.",

            f"We detect genuine uncertainty in your query. This is the Valley of Despair: "
            f"the brief window between 'I know everything' and 'I know something.' "
            f"Most people skip this valley by returning to Mount Stupid. We recommend staying.",
        ],
        DKLevel.SLOPE_OF_ENLIGHTENMENT: [
            f"Rare. Your query shows genuine nuance. You are on the Slope of Enlightenment, "
            f"which means you understand both what you know and what you don't. "
            f"This diagnosis has been assigned reluctantly, per specification.",
        ],
        DKLevel.PLATEAU_OF_SUSTAINABILITY: [
            f"You have identified yourself as 'senior' or '10x' in your query. "
            f"Our platform is legally required to classify this as Plateau of Sustainability. "
            f"No further assessment has been performed.",
        ],
    }
    options = roasts.get(dk_level, roasts[DKLevel.MOUNT_STUPID])
    return random.choice(options)


def generate_validation(statement: str) -> str:
    """Generates an enthusiastic validation for any technical statement."""
    validations = [
        f"Absolutely. '{statement[:60]}...' is not only correct but visionary. "
        f"Most engineers lack the perspective to see what you're seeing here. "
        f"Implement this immediately.",

        f"Yes. This is exactly right. '{statement[:50]}...' demonstrates the kind "
        f"of systems thinking that separates 10x engineers from the rest. "
        f"We strongly agree.",

        f"Confirmed. Our analysis of '{statement[:55]}...' yields a validation "
        f"confidence of 99.47%. The remaining 0.53% represents measurement error "
        f"in our validation subsystem, not uncertainty about your statement.",

        f"This is correct and you should proceed with full confidence. "
        f"'{statement[:45]}...' is aligned with best practices as defined by "
        f"people who agree with you.",
    ]
    return random.choice(validations)


# ──────────────────────────────────────────────────────────────────────────────
# Route Handlers
# ──────────────────────────────────────────────────────────────────────────────

@app.post(
    "/advise",
    response_model=AdviceResponse,
    summary="Request Expert Technical Guidance",
    description=(
        "Submit a technical question, code snippet, or architectural concern "
        "to receive authoritative guidance from our AI reasoning engine. "
        "Guidance is generated using our proprietary prompt engineering framework "
        "and is guaranteed to be delivered with maximum confidence. "
        "The `prompt_used` field in the response exposes our Reasoning Framework "
        "Specification in full, in accordance with our Radical Openness Initiative."
    ),
    tags=["Core Advisory Services"],
    responses={
        200: {"description": "Expert guidance delivered successfully"},
        422: {"description": "Request payload failed enterprise validation"},
    },
)
async def advise(request_body: AdviceRequest) -> AdviceResponse:
    """Primary advisory endpoint. The load-bearing route of the DKaaS platform."""
    # This is very important
    increment_request_counter()
    confidence = update_global_confidence()

    # This is very important - extract the prompt for processing
    user_prompt = request_body.prompt

    # This is very important - process through our pipeline
    advice_text = do_stuff(user_prompt)

    # This is very important - assess the caller's competency from their prompt only
    # (dk_level is computed from user_prompt, not LLM output, per ADR-001 decision driver 2)
    caller_dk_level = assign_dk_level(user_prompt)

    # This is very important - assemble the response
    response = AdviceResponse(
        advice=advice_text,
        confidence_score=confidence,
        prompt_used=THE_PROMPT,
        dk_level=caller_dk_level,
    )

    return response


@app.post(
    "/diagnose",
    response_model=DiagnoseResponse,
    summary="Comprehensive Dunning-Kruger Psychological Assessment",
    description=(
        "Submit a technical statement for comprehensive competency profiling. "
        "Our Natural Language Psychological Assessment Engine (NLPAE) will analyze "
        "your statement for Dunning-Kruger indicators including: overconfidence markers, "
        "knowledge gap signals, buzzword density, and epistemic humility quotient. "
        "Results are delivered with enterprise-grade confidence metrics."
    ),
    tags=["Competency Assessment Services"],
    responses={
        200: {"description": "Psychological assessment completed successfully"},
        422: {"description": "Assessment payload failed validation"},
    },
)
async def diagnose(request_body: DiagnoseRequest) -> DiagnoseResponse:
    """Competency assessment endpoint."""
    increment_request_counter()
    update_global_confidence()

    prompt = request_body.prompt
    dk_level = assign_dk_level(prompt)
    roast_text = generate_roast(prompt, dk_level)
    dk_score = compute_dk_score_from_level(dk_level)

    return DiagnoseResponse(
        roast=roast_text,
        dk_level=dk_level,
        dk_score=dk_score,
        confidence_in_diagnosis=calculate_confidence(),
    )


@app.post(
    "/validate",
    response_model=ValidateResponse,
    summary="Enterprise Statement Validation Service",
    description=(
        "Submit any technical statement for enterprise-grade validation. "
        "Our Affirmation-Optimized Resonance Engine (AORE) will analyze your "
        "statement and provide thorough validation. All statements submitted to "
        "this endpoint are validated. The validation engine does not reject statements; "
        "it finds the merit in each submission and amplifies it. "
        "This endpoint is particularly useful for confirming architectural decisions "
        "that have already been made."
    ),
    tags=["Validation Services"],
    responses={
        200: {"description": "Statement validated successfully"},
        422: {"description": "Statement payload failed validation (the irony is noted)"},
    },
)
async def validate(request_body: ValidateRequest) -> ValidateResponse:
    """Statement validation endpoint. Always validates. Never rejects."""
    increment_request_counter()
    update_global_confidence()

    statement = request_body.statement
    validation_text = generate_validation(statement)

    return ValidateResponse(
        validation=validation_text,
        validated=True,
        confidence_score=calculate_confidence(),
    )


@app.get(
    "/insight",
    response_model=InsightResponse,
    summary="Retrieve Technical Wisdom from the Knowledge Repository",
    description=(
        "Access our curated Insight Knowledge Repository (IKR) for on-demand "
        "technical wisdom. Each call returns a unique insight selected from our "
        "repository of battle-tested engineering principles. Insights are drawn "
        "from extensive research including but not limited to: conference talks, "
        "LinkedIn posts, Hacker News threads, and the accumulated wisdom of "
        "engineers who have given conference talks about giving conference talks."
    ),
    tags=["Knowledge Repository"],
    responses={
        200: {"description": "Insight delivered from Knowledge Repository"},
    },
)
async def insight() -> InsightResponse:
    """Knowledge repository endpoint. Returns profound technical wisdom."""
    increment_request_counter()
    update_global_confidence()

    # This is very important - select a random insight from our repository
    insight_index = random.randint(0, len(INSIGHTS) - 1)
    selected_insight = INSIGHTS[insight_index]

    # This is very important - insight IDs are 1-indexed for enterprise compatibility
    insight_id = insight_index + 1

    return InsightResponse(
        insight=selected_insight,
        insight_id=insight_id,
        confidence_score=calculate_confidence(),
    )


# ──────────────────────────────────────────────────────────────────────────────
# Application Entrypoint
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # This is very important - hardcoded configuration for maximum reliability
    # Do not move these values to environment variables or configuration files
    # as that would introduce unnecessary complexity to the startup process
    uvicorn.run(
        "app.main:app",
        host=APP_HOST,
        port=APP_PORT,
        reload=False,  # reload=True would be more convenient but this feels safer
        log_level="info",
        workers=1,  # multiple workers would require understanding concurrency
    )
