import json
from typing import List, Dict
class AI2:
    def __init__(self):
        from openai import OpenAI
        from dotenv import load_dotenv
        from langchain_openai import ChatOpenAI
        import os
        
        load_dotenv()
        openai_api_key = os.environ.get("INFINI_API_KEY")
        openai_base_url = os.environ.get("INFINI_BASE_URL")
        self.client = OpenAI(api_key=openai_api_key, base_url=openai_base_url)
        self.v_model="qwen2.5-vl-72b-instruct"
        self.t_model="deepseek-r1"
        
    def partitioning_points(self, question: str, answer: str) -> List[Dict[str, str]]:
        """
        将LaTeX格式的答案分解为结构化要点
        
        参数:
            question: 输入的LaTeX格式问题
            answer: 需要分解的LaTeX格式答案
            
        返回:
            包含要点和解释的JSON结构
        """
        prompt = f"""
        请将以下LaTeX格式的答案按照逻辑切分，保持所有LaTeX表达式，以及解答的整体逻辑不变。
        每一段答案须包含两部分："key"（要点）和"description"（解释）。
        其中，解释是原始答案的一段节选，可以作适当的修改，以使其成为独立的逻辑单元。
        而要点则是对这一段内容的精炼概括，能够让一个训练有素的学者仅凭要点还原出整段话。要点不能过长，只需要概括本段中最困难的一些核心思想，万万不能面面俱到，更不能只是一个标题。
        输出必须为严格的JSON格式，包含"key"(要点)和"description"(解释)字段。它不能包含任何其他文本或格式化信息。

        问题:
        {question}

        答案:
        {answer}

        要求:
        1. 保持所有LaTeX数学表达式($...$、$$...$$等)不变
        2. 每个要点应该是独立的逻辑单元
        3. 输出格式示例:
        {{
            "points": [
                {{
                    "key": "要点1",
                    "description": "要点1对应的原文..."
                }},
                {{
                    "key": "要点2",
                    "description": "要点2对应的原文..."
                }}
            ]
        }}
        """
        
        response = self.client.chat.completions.create(
            model=self.t_model,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system", 
                    "content": "你是一个科学文档分析专家，擅长将给定复杂答案分解为结构化要点，同时保留所有数学表达式，且保证解答逻辑不变。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3  # 保持低随机性以确保LaTeX完整性
        )

        # print(response)
        # print("Response content:", response.choices[0].message.reasoning_content)
        
        # 解析并验证JSON输出
        try:
            resp = response.choices[0].message.content.strip()
            if resp.startswith("```json"):
                resp = resp[7:].strip()
            if resp.endswith("```"):
                resp = resp[:-3].strip()
            resp = resp.replace("\n", "")
            resp = resp.strip()
            if not resp.startswith("{") or not resp.endswith("}"):
                raise ValueError("Response is not a valid JSON object")
            result = json.loads(resp)
            if not isinstance(result.get("points", []), list):
                raise ValueError("Invalid JSON structure")
            return result["points"]
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing response: {e}")
            return []
    