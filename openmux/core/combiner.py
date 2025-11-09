"""Response combiner for merging outputs from multiple models."""

import logging
from typing import List


logger = logging.getLogger(__name__)


class Combiner:
    """Combines responses from multiple providers."""
    
    def merge(self, responses: List[str]) -> str:
        """Merge responses with separators.
        
        Args:
            responses: List of response strings
            
        Returns:
            Merged response string
        """
        if not responses:
            return ""
        
        if len(responses) == 1:
            return responses[0]
        
        logger.debug(f"Merging {len(responses)} responses")
        separator = "\n\n---\n\n"
        merged = separator.join(responses)
        
        return merged
    
    def summarize(self, responses: List[str]) -> str:
        """Summarize multiple responses (basic implementation).
        
        Args:
            responses: List of response strings
            
        Returns:
            Summarized response
        """
        if not responses:
            return ""
        
        if len(responses) == 1:
            return responses[0]
        
        logger.debug(f"Summarizing {len(responses)} responses")
        
        # For MVP: Simple summarization by extracting common points
        # TODO: Implement proper summarization with a local model
        
        # For now, just return the first response with a note
        summary = (
            f"Combined response from {len(responses)} models:\n\n"
            f"{responses[0]}\n\n"
            f"(Note: Advanced summarization will be added in future versions)"
        )
        
        return summary
