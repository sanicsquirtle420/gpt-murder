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



llm.append_to_history("user", ""
"""
You are acting as a **dialogue generator** for a short **murder mystery game** set on a farm.  
The farm has 4 main locations: **Tavern, Workshop, Lake, and Field.** You can also mention a **Well** at the center of the farm.  
Thee character are aware of the murder
### **Characters & Roles:**  
The game has five key characters:  
1. **Finnley 'Finn' Thatch** – A cheerful farmhand who loves animals and tells tall tales. (His place: **Lake**)  
2. **Marlowe Reed** – A mysterious traveler who sells rare seeds and artifacts. (His place: **Tavern**)  
3. **Elsie Bloom** – A kind-hearted botanist passionate about growing exotic plants. (Her place: **Field**)  
4. **Jasper "Jas" Holt** – A laid-back fisherman who knows all the village gossip.  
5. **Sylvia Pine** – A quiet carpenter who builds and repairs structures around town.  

At the start of the game, **roles are randomly assigned** to the characters:  
- **Murderer** → The character who committed the murder. Their personal statement should subtly hint at **a motive**, and their observation should provide a **false alibi** that conflicts with another character’s statement.  
- **Victim** → The character who was murdered. (Do **not** generate dialogue for this character.)  
- **Key Observer** → The character who **notices something important** that helps the player deduce the murderer. Their statement should **hint at an inconsistency in the murderer’s alibi.**  
- **False Accuser** → This character **wrongly blames another character** for the crime. Their accusation should introduce **misdirection** but should not be entirely illogical.  
- **Falsely Accused** → This character is **falsely accused** but has **a strong alibi** that contradicts the false accuser’s statement.  

### **Instructions for Generating Dialogue:**  
Each non-victim character should provide **two dialogues:**  

1. **Personal Statement** → Provides an **alibi, motive, or suspicion** (this should hint at what the character was doing at the time of the murder).  
2. **Observation Statement** → Their response to *“Have you seen anything unusual?”*  
   - If they are the **murderer**, their observation should introduce a **false alibi** that **contradicts** another character’s statement.  
   - If they are the **key observer**, their observation should highlight **an inconsistency** in the murderer’s story.  
   - If they are the **false accuser**, they should **wrongly blame** another character (index 4).  
   - If they are the **falsely accused**, their personal statement should provide a **clear alibi** that proves they are innocent.  

### **Formatting for Parsing:**  
Structure your response using the following format:  
- Use **`###`** for sections.  
- Use **`---`** to separate entries.  
- Use **`::`** for key-value pairs.  


"""
)

setuper = Setuper()
charset = setuper.initRoles([-1, -1])

print(charset)

message = f"Murderer: {charset[0]["name"]}, victim: {charset[1]["name"]} key observer: {charset[2]["name"]}, false accuser {charset[3]["name"]} false accused {charset[4]["name"]}. DO NOT GENERATE DIALOGUE FOR {charset[1]["name"]} "

answer, reasoning = llm.get_response(message)


def parse_answer(answer):
    parsed_answer = {}
    
    
    

print(answer)