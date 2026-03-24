import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load env file
load_dotenv('.env')

# Configure GenAI
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")

genai.configure(api_key=api_key)

class InsightEngine:
    def __init__(self):
        # We try gemini-2.5-flash as requested. If it's technically unavailable or not aliased yet, 
        # it might throw an error at generation time.
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_insights(self, metrics: dict) -> str:
        prompt = f"""
You are an expert Chief Revenue Officer (CRO) and direct response copywriter.
You have been given the following raw funnel and revenue leak data for an ecommerce business:

DATA:
{json.dumps(metrics, indent=2)}

Your job is to act like a doctor diagnosing a business revenue problem. 

Provide a highly concise, punchy, and actionable insight report with the following structure:
1. 🚨 **THE DIAGNOSIS** (What is the biggest leak?)
2. 💰 **FINANCIAL IMPACT** (How much money are they losing, and what is the potential upside?)
3. 🔍 **ROOT CAUSE HYPOTHESIS** (Why is it happening? Use the device breakdown if relevant)
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
            # Fallback to the known stable flash model if 2.5 is not accessible
            if "not found" in str(e).lower() or "invalid" in str(e).lower():
                fallback_model = genai.GenerativeModel('gemini-1.5-flash')
                response = fallback_model.generate_content(prompt)
                return response.text
            raise e

if __name__ == "__main__":
    from analyzer import RevenueAnalyzer
    analyzer = RevenueAnalyzer()
    metrics = analyzer.get_summary_metrics()
    
    engine = InsightEngine()
    print("Generating AI Insights...\n")
    print(engine.generate_insights(metrics))
