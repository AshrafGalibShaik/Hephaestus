import os
import json
from dotenv import load_dotenv

# Load env file from project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

# Configure GenAI
api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
_genai_available = False

if api_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        _genai_available = True
    except Exception:
        pass

class InsightEngine:
    def __init__(self):
        if _genai_available:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None

    def generate_insights(self, metrics: dict) -> str:
        if not self.model:
            return self._fallback_insights(metrics)
        
        prompt = f"""
You are an expert Chief Revenue Officer (CRO) and direct response copywriter.
You have been given the following raw financial P&L data:

DATA:
{json.dumps(metrics, indent=2)}

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
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "not found" in str(e).lower() or "invalid" in str(e).lower():
                try:
                    fallback_model = genai.GenerativeModel('gemini-1.5-flash')
                    response = fallback_model.generate_content(prompt)
                    return response.text
                except Exception:
                    return self._fallback_insights(metrics)
            return self._fallback_insights(metrics)
    
    def _fallback_insights(self, metrics):
        """Static insights when AI is unavailable."""
        leak = metrics.get('total_leak_value', 0)
        margin = metrics.get('profit_margin', 0)
        worst = metrics.get('worst_segment', 'N/A')
        discounts = metrics.get('total_discounts', 0)
        
        return (
            f"🚨 **THE DIAGNOSIS**\n"
            f"  Revenue leaks detected worth ${leak:,.0f}\n"
            f"  from loss-making transactions.\n\n"
            f"💰 **FINANCIAL IMPACT**\n"
            f"  Current margin: {margin}%. Total\n"
            f"  discount erosion: ${discounts:,.0f}\n\n"
            f"🔍 **ROOT CAUSE**\n"
            f"  Worst performing segment: {worst}.\n"
            f"  High discount bands are eroding margins.\n\n"
            f"💊 **THE FIX**\n"
            f"  Set GOOGLE_API_KEY in .env for\n"
            f"  AI-powered recommendations."
        )

if __name__ == "__main__":
    from analyzer import RevenueAnalyzer
    analyzer = RevenueAnalyzer()
    metrics = analyzer.get_summary_metrics()
    
    engine = InsightEngine()
    print("Generating AI Insights...\n")
    print(engine.generate_insights(metrics))
