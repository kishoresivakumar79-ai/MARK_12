"""
Cloud LLM API Client for MARK 12
Provides fallback integration with OpenAI and Google Gemini APIs using standard HTTP.
"""
import os
import json
import urllib.request
from typing import Optional, Dict, Any

class CloudApiClient:
    def __init__(self, openai_key: Optional[str] = None, gemini_key: Optional[str] = None):
        self.openai_key = openai_key or os.getenv("OPENAI_API_KEY", "")
        self.gemini_key = gemini_key or os.getenv("GEMINI_API_KEY", "")

    def generate_openai(self, prompt: str, system: Optional[str] = None, model: str = "gpt-4o-mini") -> Optional[str]:
        if not self.openai_key:
            return None
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.7
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_key}"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                return res["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[OpenAI API Error] {e}")
            return None

    def generate_gemini(self, prompt: str, system: Optional[str] = None) -> Optional[str]:
        if not self.gemini_key:
            return None
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
        parts = []
        if system:
            parts.append({"text": f"System Instruction: {system}\n\nUser: {prompt}"})
        else:
            parts.append({"text": prompt})

        payload = {
            "contents": [{"parts": parts}]
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                return res["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"[Gemini API Error] {e}")
            return None
