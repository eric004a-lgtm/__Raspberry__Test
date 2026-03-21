
import os
from dotenv import load_dotenv
from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview", contents="天空為什麼是藍的"
)
print(response.text)



# import os
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# client = genai.Client(api_key=api_key)

# try:
#     # 嘗試最穩定的模型名稱格式
#     response = client.models.generate_content(
#         model="gemini-1.5-flash", 
#         contents="你好，請用繁體中文回答"
#     )
#     print(response.text)
# except Exception as e:
#     print(f"❌ 呼叫失敗：{e}")


# # response = client.models.generate_content(
# #     model="gemini-2.0-flash-lite", contents="你好"
# # )
# # print(response.text)
