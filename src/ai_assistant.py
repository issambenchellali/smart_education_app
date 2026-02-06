"""
مساعد الذكاء الاصطناعي التعليمي
"""
import json
from typing import Optional, Dict, List
import requests
from .config import config

class AIEducationAssistant:
    """فئة المساعد التعليمي الذكي"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or config.OPENAI_API_KEY
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, messages: list, model: str = "gpt-3.5-turbo", temperature: float = 0.7) -> Optional[str]:
        """إرسال طلب إلى OpenAI API"""
        if not self.api_key or self.api_key == "your-openai-key":
            return None
        
        try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 1500
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            return None
        except:
            return None
    
    def explain_lesson(self, subject: str, topic: str, grade: str, level: str = "مبتدئ") -> str:
        """شرح درس باستخدام الذكاء الاصطناعي"""
        prompt = f"""
        أنت أستاذ محترف في مادة {subject}.
        
        المطلوب: اشرح موضوع {topic} للصف {grade}
        مستوى الطالب: {level}
        
        يجب أن يحتوي الشرح على:
        1. مقدمة بسيطة عن الموضوع
        2. المفاهيم الأساسية بطريقة مبسطة
        3. أمثلة واقعية من الحياة اليومية
        4. نصائح للفهم والاستيعاب
        5. ملخص للنقاط الرئيسية
        
        استخدم لغة عربية واضحة ومناسبة للطلاب.
        """
        
        messages = [
            {"role": "system", "content": "أنت أستاذ محترف تشرح الدروس بطريقة مبسطة وممتعة."},
            {"role": "user", "content": prompt}
        ]
        
        explanation = self._make_request(messages)
        return explanation or "عذراً، تعذر الحصول على الشرح في الوقت الحالي."
    
    def generate_exercise(self, subject: str, topic: str, difficulty: str = "متوسط", num_questions: int = 3) -> str:
        """توليد تمارين باستخدام الذكاء الاصطناعي"""
        prompt = f"""
        أنشئ {num_questions} تمارين في مادة {subject}، موضوع {topic}
        مستوى الصعوبة: {difficulty}
        
        لكل تمرين:
        1. سؤال واضح ومحدد
        2. إجابة نموذجية كاملة
        3. خطوات الحل مع الشرح
        
        التمارين يجب أن تكون متنوعة.
        """
        
        messages = [
            {"role": "system", "content": "أنت أستاذ محترف في إنشاء التمارين التعليمية."},
            {"role": "user", "content": prompt}
        ]
        
        exercises = self._make_request(messages)
        return exercises or "عذراً، تعذر توليد التمارين في الوقت الحالي."
    
    def answer_question(self, question: str, context: str = None) -> str:
        """الإجابة على أسئلة الطالب"""
        prompt = f"""
        سؤال الطالب: {question}
        {f'السياق: {context}' if context else ''}
        
        أجب عن السؤال بوضوح ودقة.
        استخدم أمثلة مبسطة.
        قدم مصادر إضافية للتعلم.
        شجع الطالب على الاستمرار.
        """
        
        messages = [
            {"role": "system", "content": "أنت مساعد تعليمي ودود ومفيد."},
            {"role": "user", "content": prompt}
        ]
        
        answer = self._make_request(messages)
        return answer or "عذراً، تعذر الإجابة في الوقت الحالي."

# تهيئة المساعد
ai_assistant = AIEducationAssistant() if config.OPENAI_API_KEY != "your-openai-key" else None
