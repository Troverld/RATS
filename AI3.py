from dotenv import load_dotenv
import os


class AI3:
    def __init__(self):
        load_dotenv()
        openai_api_key = os.environ.get("INFINI_API_KEY")
        openai_base_url = os.environ.get("INFINI_BASE_URL")

        # print(openai_base_url) 


        from openai import OpenAI
        self.client = OpenAI(api_key=openai_api_key, base_url=openai_base_url)

        self.model="deepseek-r1-distill-qwen-32b"
    
    
    def address(self, question: str, solution: str,points: str,idx: int,prompt: str)->str:
        response = self.client.chat.completions.create(
        model=self.model,
        messages=[
            {"role": "system", "content": "You are a homework assistant."},
            {"role": "system", "content": "You are given a homework question, a solution, some key points of the solution."},
            {"role": "user", "content": "Homework question:\n"+question},
            {"role": "user", "content": "Solution:\n"+solution},
            {"role": "user", "content": "Key points:\n"+str(points)},
            {"role": "user", "content": "Please answer the following question for the "+str(idx)+"-th point."},
            {"role": "user", "content": prompt},
        ]
        )

        print(response)
        print(response.choices[0].message.content)