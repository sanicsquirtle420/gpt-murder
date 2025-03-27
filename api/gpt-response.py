from dotenv import load_dotenv
from openai import OpenAI
import os

class GPT(object):
    def __init__(self):
        load_dotenv(".env")
        self.client = OpenAI(api_key = os.getenv("API_KEY"))

    def get_response(self) -> str:
        msg: str = input("User: ")
        response = self.client.responses.create(
            model="gpt-3.5-turbo" ,
            instructions="You are a smart assisstant" ,
            input=msg ,
        )

        return response.output_text

def main():
    gpt = GPT()
    print(gpt.get_response())

if __name__ == "__main__":
    main()
