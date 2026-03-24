"""
AI Insight Engine — Multi-provider (Google Gemini / OpenAI)
"""

import os
import json

from hephaestus.config import load_config

config = load_config()
_provider = config.get('provider', '')
_api_key = config.get('api_key', '')
_model_id = config.get('model_id', '')
_engine_ready = False

# ── Google Gemini ────────────────────────────────────────────────
if _provider == 'google' and _api_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=_api_key)
        _engine_ready = True
    except Exception:
        pass

# ── OpenAI ───────────────────────────────────────────────────────
if _provider == 'openai' and _api_key:
    try:
        from openai import OpenAI
        _openai_client = OpenAI(api_key=_api_key)
        _engine_ready = True
    except Exception:
        pass

PROMPT_TEMPLATE = """
You are an expert Chief Revenue Officer (CRO) and direct response copywriter.
You have been given the following raw financial P&L data:

DATA:
{data}

Your job is to act like a doctor diagnosing a business revenue problem. 

Provide a highly concise, punchy, and actionable insight report with the following structure:
1. 🚨 **THE DIAGNOSIS** (What is the biggest revenue leak?)
2. 💰 **FINANCIAL IMPACT** (How much money is leaking, and what is the potential upside?)
3. 🔍 **ROOT CAUSE HYPOTHESIS** (Why is it happening? Use the segment/product/discount data)
4. 💊 **THE FIX** (Actionable prescription to solve it)

Rules:
- Keep it extremely short and punchy. 
- Use formatting strictly as above.
- No fluff. Write like you're talking to a busy CEO who only cares about the bottom line.
- Present the insight as "If you fix X, you make $Y more."
"""

class InsightEngine:
    def __init__(self):
        self.ready = _engine_ready
    
    def generate_insights(self, metrics: dict) -> str:
        if not self.ready:
            return self._fallback(metrics)
        
        prompt = PROMPT_TEMPLATE.format(data=json.dumps(metrics, indent=2, default=str))
        
        try:
            if _provider == 'google':
                return self._call_gemini(prompt)
            elif _provider == 'openai':
                return self._call_openai(prompt)
            else:
                return self._fallback(metrics)
        except Exception:
            return self._fallback(metrics)
    
    def _call_gemini(self, prompt):
        model = genai.GenerativeModel(_model_id)
        response = model.generate_content(prompt)
        return response.text
    
    def _call_openai(self, prompt):
        response = _openai_client.chat.completions.create(
            model=_model_id,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        return response.choices[0].message.content
    
    def _fallback(self, metrics):
        leak = metrics.get('total_leak_value', 0)
        margin = metrics.get('margin_pct', 0)
        worst = metrics.get('worst_category', 'N/A')
        loss = metrics.get('total_loss', 0)
        
        return (
            f"🚨 THE DIAGNOSIS\n"
            f"  Revenue leaks worth ${leak:,.0f} detected\n"
            f"  in loss-making transactions.\n\n"
            f"💰 FINANCIAL IMPACT\n"
            f"  Current margin: {margin}%\n"
            f"  Discount erosion: ${loss:,.0f}\n\n"
            f"🔍 ROOT CAUSE\n"
            f"  Weakest area: {worst}\n\n"
            f"💊 THE FIX\n"
            f"  Configure an AI model via Settings\n"
            f"  for detailed recommendations."
        )

if __name__ == "__main__":
    from hephaestus.analyzer import RevenueAnalyzer
    analyzer = RevenueAnalyzer()
    metrics = analyzer.get_summary_metrics()
    engine = InsightEngine()
    print(engine.generate_insights(metrics))
