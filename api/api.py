import os
from dotenv import load_dotenv
import openai
from utilities.setuper import Setuper
from utilities.data import characters

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
IP = os.getenv("IP")

class Local:
    def __init__(self, host_ip, port_num, api_key_str):
        self.client = openai.Client(base_url=f"http://{host_ip}:{port_num}/v1", api_key=api_key_str)
        self.model_name = self.client.models.list().data[0].id
        self.history = []
        print(self.model_name)

    def append_to_history(self, role: str, data: str):
        self.history.append({"role": role, "content": data})

    def get_response(self, message):
        self.append_to_history("user", message)
        response_stream = self.client.chat.completions.create(
            model=self.model_name,
            messages=self.history,
            temperature=0.6,
            top_p=0.95,
            stream=True,
        )

        reasoning = ""
        answer = ""
        hasContentStarted = False
        hasReasonStarted = False

        for chunk in response_stream:
            if chunk.choices[0].delta.content:
                if not hasContentStarted:
                    hasContentStarted = True
                    print("\n~~~ END OF REASONING ~~~")
                    print("\n~~~ BEGINNING OF ANSWER ~~~")

                print(chunk.choices[0].delta.content, end="")
                answer += chunk.choices[0].delta.content

            elif chunk.choices[0].delta.reasoning_content:
                if not hasReasonStarted:
                    hasReasonStarted = True
                    print("\n~~~ BEGINNING OF REASONING ~~~")
                print(chunk.choices[0].delta.reasoning_content, end="")
                reasoning += chunk.choices[0].delta.reasoning_content

        print("\n~~~ END OF ANSWER ~~~")
        return answer, reasoning


def main():
    """Main function to initialize game setup and fetch NPC dialogues before the game starts."""
    print("Loading API Key...")
    print(API_KEY)


    llm = Local(IP, 50001, API_KEY)


    setuper = Setuper()
    charset = setuper.initRoles()
    print("Game roles initialized:", charset)


    message = f"""
    You are generating in-game dialogues for a mystery murder game set on a farm. There are four remaining NPCs, each with a predefined role. 

    Here are the profiles for each character:

    Finnley "Finn" Thatch – A cheerful farmhand who loves animals and tells tall tales.
    Marlowe Reed – A mysterious traveler who sells rare seeds and artifacts.
    Elsie Bloom – A kind-hearted botanist passionate about growing exotic plants.
    Jasper "Jas" Holt – A laid-back fisherman who knows all the village gossip.
    Sylvia Pine – A quiet carpenter who builds and repairs structures around town. 

    Generate two pieces of dialogue for each:
    Personal Statement: Their own alibi or view on the situation.
    Observation: A piece of information they noticed about the crime scene or another character.

    Observation should not be a direct accusation, just hints.

    Each role follows these specific rules:
    - **Murderer**: Their observation must introduce a false alibi that contradicts another character’s statement.
    - **Key Observer**: Their observation must highlight an inconsistency in the murderer's story.
    - **False Accuser**: Their observation must wrongly blame another character.
    - **Falsely Accused**: Their personal statement should provide a clear alibi proving their innocence.

    Present responses in the following format:

    ###
    name::[Character Name]  
    Personal Statement::[Character's personal statement]  
    Observation::[Character's observation]  
    ###  

    Now, generate responses following this format for these roles:
    Victim is {characters[charset[1]]["name"]}. YOU DO NOT NEED TO GENERATE ANY DIALOGUES FOR HER.

    {characters[charset[0]]["name"]} is the **Murderer**.
    {characters[charset[2]]["name"]} is a **Key Observer**.
    {characters[charset[3]]["name"]} is a **Wrong Accuser**.
    {characters[charset[4]]["name"]} is **Wrongly Accused**.

    """


    print("Generating dialogues...")
    answer, reasoning = llm.get_response(message)

    print("\nGenerated Dialogue:\n", answer)

  
    res = setuper.parse_dialogue(answer)
    res.sort(key=lambda x: x['name'])

    print(f"before len {len(characters)}, chars {characters}")

    characters.remove(characters[charset[1]])

    print(f"after len {len(characters)}, chars {characters}")

    for i in range(characters):
        characters[i]["dialogues"].append(res[i]["Personal Statement"])
        characters[i]["dialogues"].append(res[i]["Observation"])


    print(f"Parsed Dialogues (Count: {len(res)}):\n{res}")
    





if __name__ == "__main__":
    main()
