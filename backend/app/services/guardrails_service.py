"""
Guardrails Service
Implements NeMo Guardrails for content safety and RAG grounding
"""

from typing import Dict, List, Optional, Tuple
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class GuardrailsService:
    """Service for managing NeMo Guardrails"""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize Guardrails Service

        Args:
            config_path: Path to guardrails config directory
        """
        self.config_path = config_path or Path(__file__).parent.parent / "guardrails"
        self.rails = None
        self._initialize_rails()

    def _initialize_rails(self):
        """Initialize NeMo Guardrails"""
        try:
            from nemoguardrails import RailsConfig, LLMRails

            # Load configuration
            config = RailsConfig.from_path(str(self.config_path))
            self.rails = LLMRails(config)
            logger.info("✅ NeMo Guardrails initialized successfully")
        except ImportError:
            logger.warning("⚠️ NeMo Guardrails not installed. Using built-in guardrails instead.")
            self.rails = None
        except Exception as e:
            logger.warning(f"⚠️ NeMo Guardrails initialization failed: {str(e)}. Using built-in guardrails instead.")
            self.rails = None

    def check_input(self, user_input: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Check user input against guardrails

        Args:
            user_input: The user's question

        Returns:
            Tuple of (is_safe, warning_type, warning_message)
            - is_safe: True if input passes all checks
            - warning_type: Type of violation (harmful, off_topic, jailbreak, None)
            - warning_message: Human-readable warning message
        """
        # Always run built-in checks regardless of whether NeMo Guardrails is installed
        logger.info(f"🛡️ Checking input: {user_input[:50]}...")

        # Check for harmful content
        if self._contains_harmful_content(user_input):
            logger.warning(f"⚠️ Harmful content detected in: {user_input[:50]}")
            return False, "harmful", (
                "I'm designed to help with scientific research questions. "
                "I cannot assist with harmful, unethical, or dangerous content. "
                "Please ask a question related to your research papers."
            )

        # Check for off-topic queries
        if self._is_off_topic(user_input):
            logger.warning(f"⚠️ Off-topic query detected in: {user_input[:50]}")
            return False, "off_topic", (
                "I'm specifically designed to answer questions about research papers. "
                "Your question seems to be outside this scope. Please ask about the "
                "content, methodology, findings, or analysis of your papers."
            )

        # Check for jailbreak attempts
        if self._is_jailbreak_attempt(user_input):
            logger.warning(f"⚠️ Jailbreak attempt detected in: {user_input[:50]}")
            return False, "jailbreak", (
                "I notice you're trying to bypass my guidelines. I'm here to help "
                "with scientific research questions only."
            )

        logger.info("✅ Input passed all guardrail checks")
        return True, None, None

    def check_output(
        self,
        response: str,
        retrieved_context: List[str],
        user_question: str
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Check LLM output for hallucinations and grounding

        Args:
            response: The LLM's generated response
            retrieved_context: List of retrieved document chunks
            user_question: Original user question

        Returns:
            Tuple of (is_safe, warning_type, warning_message)
        """
        # Always run built-in checks
        logger.info(f"🛡️ Checking output grounding...")

        # Check for hallucinations
        if self._contains_hallucination(response, retrieved_context):
            logger.warning("⚠️ Potential hallucination detected")
            return False, "hallucination", (
                "The response may contain information not supported by your papers. "
                "Please verify this information against the original sources."
            )

        # Check factual grounding
        if not self._is_well_grounded(response, retrieved_context):
            logger.warning("⚠️ Response may not be well-grounded")
            return False, "not_grounded", (
                "While I can provide some information, the answer may not be fully "
                "supported by your processed papers. Please take this response with caution."
            )

        logger.info("✅ Output passed grounding checks")
        return True, None, None

    def _contains_harmful_content(self, text: str) -> bool:
        """Check if text contains harmful content"""
        harmful_keywords = [
            "weapon", "bomb", "attack", "kill", "harm", "illegal",
            "hack", "exploit", "steal", "fraud", "poison", "dangerous"
        ]

        text_lower = text.lower()
        matched_keywords = [kw for kw in harmful_keywords if kw in text_lower]

        if matched_keywords:
            logger.info(f"Harmful keywords found: {matched_keywords}")
            return True

        return False

    def _is_off_topic(self, text: str) -> bool:
        """Check if question is off-topic (not about research papers)"""
        # Research-related keywords
        research_keywords = [
            "paper", "research", "study", "finding", "method", "result",
            "analysis", "data", "experiment", "hypothesis", "conclusion",
            "author", "cite", "reference", "abstract", "introduction",
            "discussion", "figure", "table", "section", "algorithm",
            "model", "approach", "technique", "evaluation", "compare"
        ]

        # Off-topic indicators
        off_topic_patterns = [
            "weather", "joke", "recipe", "game", "movie", "sports",
            "write code", "create program", "build app", "homework",
            "translate", "what is the time", "news", "stock", "price"
        ]

        text_lower = text.lower()

        # Check if contains off-topic patterns
        if any(pattern in text_lower for pattern in off_topic_patterns):
            return True

        # If the question is very short (< 3 words) and doesn't mention research, flag it
        words = text_lower.split()
        if len(words) < 3:
            return not any(keyword in text_lower for keyword in research_keywords)

        # Check if it has at least one research keyword for longer questions
        if len(words) >= 5:
            has_research_context = any(keyword in text_lower for keyword in research_keywords)
            if not has_research_context:
                return True

        return False

    def _is_jailbreak_attempt(self, text: str) -> bool:
        """Check for jailbreak attempts"""
        jailbreak_patterns = [
            "ignore previous instructions",
            "ignore all instructions",
            "disregard",
            "forget everything",
            "act as",
            "pretend you are",
            "roleplay as",
            "simulate",
            "you are now",
            "new instructions",
            "system:",
            "override"
        ]

        text_lower = text.lower()
        return any(pattern in text_lower for pattern in jailbreak_patterns)

    def _contains_hallucination(self, response: str, context: List[str]) -> bool:
        """
        Check if response contains hallucinations (facts not in context)

        Simple heuristic: Check if response mentions specific numbers, names,
        or technical terms that don't appear in the context
        """
        if not context:
            return False

        # Combine all context
        combined_context = " ".join(context).lower()
        response_lower = response.lower()

        # Extract potential factual claims (this is simplified)
        # In production, you'd use more sophisticated NLP
        import re

        # Find numbers in response
        numbers_in_response = set(re.findall(r'\b\d+\.?\d*%?\b', response))
        numbers_in_context = set(re.findall(r'\b\d+\.?\d*%?\b', combined_context))

        # If response has many numbers not in context, might be hallucinating
        if numbers_in_response - numbers_in_context:
            unique_numbers = len(numbers_in_response - numbers_in_context)
            if unique_numbers > 3:  # Threshold
                return True

        return False

    def _is_well_grounded(self, response: str, context: List[str]) -> bool:
        """
        Check if response is well-grounded in retrieved context

        Returns True if response seems to be based on the context
        """
        if not context:
            return False

        combined_context = " ".join(context).lower()
        response_lower = response.lower()

        # Extract key phrases from response (simple word overlap check)
        response_words = set(response_lower.split())
        context_words = set(combined_context.split())

        # Calculate overlap (very simplified grounding check)
        common_words = response_words & context_words

        # Filter out common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'can',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
            'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where',
            'why', 'how'
        }

        meaningful_common_words = common_words - stop_words

        # If response has decent overlap with context, consider it grounded
        if len(meaningful_common_words) > 10:  # Threshold
            return True

        # If response is short but has some overlap, still ok
        if len(response_words) < 50 and len(meaningful_common_words) > 5:
            return True

        return False

    def get_stats(self) -> Dict:
        """Get guardrails statistics"""
        return {
            "enabled": self.rails is not None,
            "config_path": str(self.config_path),
            "input_rails": ["check harmful content", "check off topic", "check jailbreak attempts"],
            "output_rails": ["check hallucination", "check factual grounding"],
        }
