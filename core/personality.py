"""
Personality Manager for MARK 12
Applies tone adjustments, polite courtesies, and voice formatting.
"""
class Personality:
    def __init__(self, style: str = "jarvis_classic"):
        self.style = style

    def format_speech(self, text: str) -> str:
        """Formats response text to be smooth and concise when spoken."""
        # Remove markdown symbols and code fences for spoken voice output
        clean = text.replace("```python", "").replace("```", "").replace("#", "").replace("*", "")
        # Shorten if too long for a single breath
        sentences = clean.split(".")
        if len(sentences) > 3:
            return ". ".join(sentences[:3]) + "."
        return clean.strip()

    def apply_persona(self, response_text: str) -> str:
        return response_text

global_personality = Personality()
