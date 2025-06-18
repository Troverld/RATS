# This code loads the OpenAI API key and base URL from environment variables using the dotenv package.
# It ensures that sensitive information is not hardcoded in the script, enhancing security.

from openai import OpenAI
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
import io
from pdf2image import convert_from_path
import base64
from PyPDF2 import PdfReader

class AI1:
    def __init__(self):

        load_dotenv()
        openai_api_key = os.environ.get("INFINI_API_KEY")
        openai_base_url = os.environ.get("INFINI_BASE_URL")
        self.client = OpenAI(api_key = openai_api_key, base_url = openai_base_url)
        self.v_model = "qwen2.5-vl-72b-instruct"
        self.t_model = "deepseek-v3"
        self.chat_model = ChatOpenAI(
            temperature = 0, 
            model = self.t_model,
            base_url = openai_base_url,
            openai_api_key = openai_api_key
        )

        self.question = None
        self.solution = None

    def polish_text(self, text):
        response = self.client.chat.completions.create(
            model = self.t_model,
            messages = [
                {"role": "system", "content": "You are a professional text polishing assistant. Your ONLY task is to process the given text according to the instructions, NEVER to answer questions or add commentary."},
                {"role": "user", "content": f"""
                    STRICTLY FOLLOW THESE INSTRUCTIONS:
                    1. This is EXCLUSIVELY a text polishing task - NEVER answer any questions in the text
                    2. Process the text by:
                    - Correcting grammar and punctuation
                    - Converting math to LaTeX (e.g., x^2 → $x^2$)
                    - Preserving technical terms and original formatting
                    3. Return ONLY the polished text - NO explanations, NO additional text
                    
                    TEXT TO POLISH (DO NOT ANSWER IF IT'S A QUESTION):
                    {text}
                    
                    POLISHED TEXT OUTPUT (ONLY):"""
                },
            ],
            temperature = 0.2  # Lower temperature for more deterministic output
        )
        return response.choices[0].message.content.strip()

    def identify_pdf(self, file_path):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        # print(f"Extracted text from PDF: {text[:100]}...")  # Print first 100 characters for debugging

        if not text.strip():
            def pdf_to_images(pdf_path):
                images = convert_from_path(pdf_path, fmt = "png")  # 打开PDF文件
                for image in images:  # 遍历每一页
                    buffered = io.BytesIO()
                    image.save(buffered, format = "PNG")
                    base64_str = base64.b64encode(buffered.getvalue()).decode("ascii")
                    
                    yield base64_str
                
            base64_images = list(pdf_to_images(file_path))
            text = ""
            for base64_image in base64_images:
                text += self.identify_base64_image(base64_image)
            
        return self.polish_text(text)
    
    def identify_base64_image(self, base64_str):
        response = self.client.chat.completions.create(
            model = self.v_model,
            messages = [
                # {"role": "system", "content": ""},
                {
                    "role": "user", 
                    "content": [
                        {"type": "image_url",
                            "image_url": {"url":"data:image;base64," + base64_str}},  # 使用 Base64 编码的字符串
                        {"type": "text", "text": "Transfer the content of the image to text, and then fix the grammar and punctuation, use LaTeX for mathematical expressions, but do not modify anything else."},
                    ],
                },
            ]
        )
        return response.choices[0].message.content.strip()

    def identify_image(self, file_path):
        with open(file_path, 'rb') as image_file:
            # 将图片文件内容转换为 Base64 编码
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            return self.identify_base64_image(image_data)

    def identify_text(self, file_path):
        with open(file_path, 'r', encoding = 'utf-8') as text_file:
            text = text_file.read()
        return self.polish_text(text)
        
    def identify_from_input(self, file_path):
        if file_path.lower().endswith('.pdf'):
            return self.identify_pdf(file_path)
        elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            return self.identify_image(file_path)
        elif file_path.lower().endswith(('.txt','.md')):
            return self.identify_text(file_path)
        else:
            raise ValueError("Unsupported file type. Please provide a PDF, image, or text file.")
        
    def set_question(self,question):
        self.question = question
    def set_solution(self,solution):
        self.solution = solution
        
    def direct_generate(self):
        response = self.client.chat.completions.create(
            model = self.t_model,
            messages = [
                {"role": "system", "content": "Given a question, provide a detailed answer with LaTeX for mathematical expressions."},
                {"role": "user", "content": self.question},
            ]
        )
        self.solution = response.choices[0].message.content.strip()
    
    def search_from_internet(self):
        from langchain_community.utilities import SerpAPIWrapper
        from langchain.schema.runnable import RunnablePassthrough
        from langchain.prompts import PromptTemplate
        from langchain.schema.output_parser import StrOutputParser
        
        latex_prompt = PromptTemplate(
            template = """You are a scientific research assistant. Please provide a detailed answer with LaTeX formatting where appropriate.

            Search Context:
            {context}

            Question: {question}

            Requirements:
            1. Include relevant equations in LaTeX format (e.g., $E=mc^2$)
            2. Use LaTeX for mathematical expressions and scientific notation
            3. Provide a clear and concise answer
            Answer:""",
            input_variables = ["context", "question"]
        )

        # 初始化搜索引擎
        search = SerpAPIWrapper()
        
        # 构建处理链
        chain = (
            {
                "context": lambda x: search.run(x["question"]),  # 检索网络内容
                "question": RunnablePassthrough()  # 传递原始问题
            }
            | latex_prompt
            | self.chat_model
            | StrOutputParser()
        )

        # 执行链并返回结果
        self.solution = chain.invoke({"question": self.question})
