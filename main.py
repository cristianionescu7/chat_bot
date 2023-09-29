import json
from difflib import get_close_matches
import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

def load_knowledge_base(file_path: str)-> dict:
    with open(file_path, "r") as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str])-> str | None:
    matches: list = get_close_matches(user_question, questions, n = 1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
        

def chat_bot():
    knowledge_base: dict = load_knowledge_base("knowledge_base.json")
    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break

        doc = nlp(user_input)

        # Access tokens, parts of speech, named entities, etc.
        for token in doc:
            print(token.text, token.pos_, token.dep_)

        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            for token in doc:
                if (token.text.lower() == "weather" or token.text.lower() == "tomorrow") and token.dep_ == "nsubj":
                # User is asking about the weather
                # Implement logic to fetch weather information and respond
                    response = "Should I check the weather for you?"
                    print(f'Bot: {response}')
                    if user_input.lower() == "yes":
                        response = "Great! I'll check the weather for you."
                        print(f'Bot: {response}')

            """print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})  
                save_knowledge_base("knowledge_base.json", knowledge_base)
                print('Thank you! I learned a new response!')
            else:
                print('Ok, I\'ll ask you later.')
                print(knowledge_base)"""


if __name__=='__main__':
    chat_bot()      
