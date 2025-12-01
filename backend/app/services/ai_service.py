from openai import OpenAI
from ..config import settings
from typing import List, Dict

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class AIService:
    @staticmethod
    async def chat_with_assistant(message: str, context: str = None) -> str:
        """AI Study Assistant - answer questions about study materials"""
        messages = [
            {
                "role": "system",
                "content": "You are a helpful study assistant. Help students understand their study materials, answer questions, and provide explaination. Be concise and educational."
            }
        ]

        if context:
            messages.append({
                "role": "system",
                "content": f"Context from student's notes: {context}"
            })
        
        messages.append({
            "role": "user",
            "content": message
        })

        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )

        return response.choices[0].message.content

    @staticmethod
    async def summarize_text(text: str, max_length: int = 150) -> str:
        """Summarize long text content"""
        response = client.chat.completions.create(
            models=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"Summarize the following text in approximately {max_length} words. Focus on key points and main ideas."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            max_tokens=max_length * 2,
            temperature=0.5
        )

        return response.choices[0].message.content
    
    @staticmethod
    async def generate_quiz(content: str, num_questions: int = 5) -> List[Dict]:
        """Generate quiz questions from study content"""
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"""Generate {num_questions} multiple-choice quiz quesitons based on the following content.
                    Return ONLY a JSON array with this exact format:
                    [
                        {{
                            "question": "question text",
                            "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                            "correct_answer": "A",
                            "explanation": "brief explanation"
                        }}
                    ]"""
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )

        import json
        try:
            quiz_data = json.loads(response.choices[0].message.content)
            return quiz_data
        except:
            return [] #fallback if json parsing fails
        
    @staticmethod
    async def generate_flashcards(content: str, num_cards: int = 10) -> List[Dict]:
        """Generate flashcards from study content"""
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"""Create {num_cards} flashcards from the following content.
                    Return ONLY a JSON array with this format:
                    [
                        {{
                            "question": "question or term",
                            "answer": "answer or definition",
                            "difficulty": "easy|medium|hard"
                        }}
                    ]"""
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            max_tokens=1500,
            temperature=0.7
        )

        import json
        try:
            flashcards = json.loads(response.choices[0].message.content)
            return flashcards
        except:
            return []
        
    @staticmethod
    async def smart_search(query: str, notes_content: List[str]) -> str:
        """Natural language search through notes"""
        combined_notes = "\n\n".join(notes_content[:5]) #limit to avoid token limts

        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a search assistant. Based on the user's natural language query, find and return the most relevant information from their notes."
                },
                {
                    "role": "user",
                    "content": f"Query: {query}\n\nNotes:\n{combined_notes}"
                }
            ],
            max_tokens=300,
            temperature=0.5
        )

        return response.choices[0].message.content
    
ai_service = AIService()