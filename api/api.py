import os
from dotenv import load_dotenv
import openai
from utilities.setuper import Setuper


#loading environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
IP = os.getenv("IP")


class local:
    def __init__(self, host_ip, port_num, api_key_str):
        self.client = openai.Client(base_url=f"http://{host_ip}:{port_num}/v1", api_key=api_key_str)
        self.model_name = self.client.models.list().data[0].id

        self.history = []

        print(self.model_name)

    def append_to_history(self, role: str, data: str):
        self.history.append({
            "role": role,
            "content": data
        })

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
        hasContentStarted = False ; hasReasonStarted = False

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



print(API_KEY)



llm = local(IP, 50001, API_KEY)





setuper = Setuper()
charset = setuper.initRoles([-1,-1])

print(charset)

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

Observation should not be direct accusation, just hints

Each role follows these specific rules:

Murderer: Their observation must introduce a false alibi that contradicts another character’s statement.

Key Observer: Their observation must highlight an inconsistency in the murderer’s story, but they should not realize that murderer is being accused.

False Accuser: Their observation must wrongly blame another character.

Falsely Accused: Their personal statement should provide a clear alibi proving their innocence.

Ensure the responses are immersive and fit each character's personality. Present them in the following strict format:

###
name::[Character Name]  
Personal Statement::[Character's personal statement]  
Observation::[Character's observation]  
###  
Example Output:
###
name::Jasper "Jas" Holt  
Personal Statement::I was out by the river fishing all morning. Didn’t see a soul until I came back to the farm.  
Observation::Strange thing is, Finn says he was in the barn the whole time, but I saw someone in a dark coat near the tool shed.  
###  


Now, generate responses following this format for these roles:
Victim is {charset[1]["name"]}. YOU DO NOT NEED TO GENERATE ANY DIALOGUES FOR HER

{charset[0]["name"]} is a MURDERER. Their personal statement should tell something about their character, or motive. They should not directly show hostility towards victim
Their observation can be an alibi. 

{charset[2]["name"]} is A KEY OBSERVER. Their personal statement should tell something about their character.
Their observation should be something that CONTRADICTS alibi of Murderer,  who is {charset[0]["name"]}

{charset[3]["name"]} is A WRONG ACCUSER. Their personal statement should tell something about their character.
Their observation should be something that WRONGLY ACCUSES  {charset[4]["name"]}.

{charset[4]["name"]} IS A WRONG ACCUSED. Their personal statement should tell something about their character.
Their observation should be something that EXPLAINS accusation of {charset[3]["name"]}

"""

answer, reasoning = llm.get_response(message)


print(answer)

def parse_answer(answer):
    parsed_answer = {}
    
    
    

print(answer)