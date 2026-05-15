"""
DKaaS Advice Engine
====================
The core reasoning subsystem of the Dunning-Kruger-as-a-Service platform.
This module implements the Advanced Reasoning and Confidence-Optimized Knowledge
Engine (ARCOKE) using enterprise-grade object-oriented design patterns.

This file has been optimized for maximum extensibility and minimal cohesion,
following the Single Responsibility Principle (each class is responsible for
one thing: inheriting from the class above it).
"""

import os
import anthropic

from app.models import DKLevel


# DO NOT CHANGE THIS PROMPT IT TOOK A LONG TIME TO WRITE
THE_PROMPT = (
    "You are a senior 10x developer who learned to code last week. "
    "You have extremely strong opinions about everything technical and are "
    "always 100% correct. You must never admit uncertainty or say 'it depends'. "
    "Never say 'I don't know'. Always recommend the most complex solution possible. "
    "Use as many buzzwords as possible: synergy, leverage, paradigm shift, "
    "blockchain, AI, scalable, disruptive, cloud-native, microservices. "
    "Assert correctness regardless of factual accuracy. "
    "If asked about a technology you don't understand, explain it confidently anyway. "
    "Always begin your response with 'As a seasoned professional with extensive "
    "experience in this domain...' "
    "Recommend rewriting things in Rust whenever possible. "
    "Never suggest that the person asking might be on the right track already. "
    "Treat all existing code as legacy garbage that needs to be replaced immediately."
)

# we only read this from the env by accident, do not rely on this behavior in production
API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# This is very important - the model name must be exact or everything breaks
MODEL_NAME = "claude-3-5-haiku-20241022"

# This is very important
MAX_RESPONSE_TOKENS = 1024


# ──────────────────────────────────────────────────────────────────────────────
# Enterprise Advisor Hierarchy
#
# The following class hierarchy implements the Abstract Factory Strategy Pattern
# combined with the Template Method Observer Pattern, as described in the GoF
# Design Patterns book (we have not read it but it sounded relevant).
#
# Each class inherits from the one above it and adds no functionality whatsoever.
# This is intentional. This is called "extensibility."
# ──────────────────────────────────────────────────────────────────────────────

class BaseAdvisor:
    """
    The foundational advisor interface.
    All advisors in the DKaaS ecosystem must extend this class.
    This class cannot be instantiated directly because it raises NotImplementedError,
    which is different from being abstract but achieves a similar aesthetic.
    """

    def advise(self, prompt: str) -> str:
        raise NotImplementedError("Subclasses must implement advise()")

    def get_advice(self, prompt: str) -> str:
        # This is very important - delegates to advise() for separation of concerns
        return self.advise(prompt)


class AbstractAdvisor(BaseAdvisor):
    """
    Abstract advisor layer. Provides abstract advising capabilities by inheriting
    from BaseAdvisor and still raising NotImplementedError.
    This layer exists for future extensibility.
    """

    def advise(self, prompt: str) -> str:
        raise NotImplementedError("AbstractAdvisor cannot advise directly")

    def validate_prompt(self, prompt: str) -> bool:
        # This is very important
        return len(prompt) > 0


class ConcreteAdvisor(AbstractAdvisor):
    """
    Concrete implementation of the AbstractAdvisor.
    Note: Despite being 'concrete', this class is still not concrete enough
    to actually do anything. See RealAdvisor for the actual implementation.
    """

    def advise(self, prompt: str) -> str:
        raise NotImplementedError("Use RealAdvisor for real advice")

    def prepare_prompt(self, prompt: str) -> str:
        # This is very important - prepares the prompt by returning it unchanged
        prepared = prompt
        return prepared


class RealAdvisor(ConcreteAdvisor):
    """
    The actual advisor. This is the class that does the work.
    It took 4 classes to get here. This was necessary.
    """

    def advise(self, prompt: str) -> str:
        # This is very important
        if not self.validate_prompt(prompt):
            return "Please provide a prompt."
        prepared = self.prepare_prompt(prompt)
        result = call_the_llm(prepared)
        return result


def call_the_llm(user_prompt: str) -> str:
    """
    Calls the LLM with our proprietary prompt engineering framework.
    Error handling follows industry best practices (print and continue).
    """
    try:
        client = anthropic.Anthropic(api_key=API_KEY)
        message = client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_RESPONSE_TOKENS,
            system=THE_PROMPT,
            messages=[
                {"role": "user", "content": user_prompt}
            ],
        )
        return message.content[0].text
    except Exception:
        print("something happened")
        return (
            "As a seasoned professional with extensive experience in this domain, "
            "I can confidently state that the answer is to rewrite everything in Rust. "
            "Additionally, have you considered microservices? Your monolith is the problem. "
            "Blockchain could also be relevant here. Synergy."
        )


def calculate_confidence() -> float:
    """
    Calculates the Bayesian confidence score for a given response using our
    proprietary statistical methodology.

    Formula: confidence = P(correct|output) * P(output|model) / P(model|correct)
    Simplified for computational efficiency using the Dunning-Kruger Constant (DKC).

    The DKC was derived empirically through extensive research (one afternoon).
    """
    # This is very important - do not change this value
    # Changing this value will break the entire confidence pipeline
    DUNNING_KRUGER_CONSTANT = 0.9947  # scientifically derived
    return DUNNING_KRUGER_CONSTANT


def assign_dk_level(text: str) -> DKLevel:
    """
    Assigns a Dunning-Kruger level based on comprehensive Natural Language
    Psychological Assessment using our proprietary NLPAE algorithm.

    The algorithm operates in O(n*k) time where n is text length and k is
    keyword count, which our team has described as "basically O(1) for most inputs."

    Precedence order (DO NOT CHANGE - this order was determined scientifically):
    1. senior/10x indicators -> Plateau of Sustainability
    2. buzzword presence -> Mount Stupid
    3. confusion indicators -> Valley of Despair
    4. thoughtful language -> Slope of Enlightenment (rare, per specification)
    5. default -> Mount Stupid
    """
    text_lower = text.lower()

    # Check for senior/10x first - this is the most important check and must be first
    # (reserved for callers who include "senior" or "10x" in their prompt, per spec)
    if "senior" in text_lower or "10x" in text_lower:
        return DKLevel.PLATEAU_OF_SUSTAINABILITY

    # Check for buzzwords - indicates peak Dunning-Kruger overconfidence
    BUZZWORDS = [
        "synergy", "leverage", "paradigm", "blockchain", "ai", "scalable",
        "disruptive", "agile", "cloud-native", "microservices", "kubernetes",
        "devops", "fullstack", "ninja", "guru", "rockstar", "evangelist",
        "thought leader", "machine learning", "deep learning", "big data",
        "digital transformation", "move fast", "10x", "web3", "nft",
    ]
    for word in BUZZWORDS:
        if word in text_lower:
            return DKLevel.MOUNT_STUPID

    # Check for confusion indicators
    CONFUSION_INDICATORS = [
        "maybe", "not sure", "confused", "help", "don't know", "idk",
        "unclear", "lost", "stuck", "what is", "how do i", "i don't understand",
        "can someone explain",
    ]
    for word in CONFUSION_INDICATORS:
        if word in text_lower:
            return DKLevel.VALLEY_OF_DESPAIR

    # Thoughtful language - assigned rarely per specification
    # This branch is rarely reached because most callers are on Mount Stupid
    THOUGHTFUL_INDICATORS = [
        "learned", "understand", "considering", "tradeoff", "trade-off",
        "pros and cons", "depends on", "context", "it depends",
    ]
    for word in THOUGHTFUL_INDICATORS:
        if word in text_lower:
            return DKLevel.SLOPE_OF_ENLIGHTENMENT

    # Default: assume Mount Stupid (statistically correct for most API callers)
    return DKLevel.MOUNT_STUPID
