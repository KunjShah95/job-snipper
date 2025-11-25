"""
Utility for analyzing text content from resume versions.
"""

from collections import Counter
from typing import List, Dict


class TextAnalyzer:
    """Analyzes text to extract insights."""

    def analyze_section_modifications(self, versions: List[Dict]) -> Dict[str, int]:
        """
        Analyzes a list of versions to count modifications per section.
        This is a simplified simulation. A real implementation would compare
        the content of parsed sections between consecutive versions.

        Args:
            versions: A list of version dictionaries.

        Returns:
            A dictionary with section names as keys and modification counts as values.
        """
        if len(versions) < 2:
            return {}

        # Simulate by tracking changes in notes or names.
        # A real implementation would require diffing parsed content.
        mod_counts = Counter()
        for i in range(len(versions) - 1):
            # This is a placeholder for real diffing logic.
            # We'll simulate some changes based on version metadata.
            mod_counts["Experience"] += 3
            mod_counts["Skills"] += 2
            mod_counts["Summary"] += 1
            mod_counts["Education"] += 1

        return dict(mod_counts)