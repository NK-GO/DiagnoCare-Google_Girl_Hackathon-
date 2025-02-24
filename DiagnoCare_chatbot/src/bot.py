import os
import poe
import threading
import time

# Initialize client with environment token
client = poe.Client(os.getenv("POE_TOKEN"))
model_name = "chinchilla"

# Define color constants for console output
class ColorCodes:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Class to represent user queries
class UserInput:
    def __init__(self, message="Hello"):
        self.message = message
        self.summary = message
        self.info = {}

    def update_input(self, message):
        self.message = message
        self.summary = message
        return self.message

    def add_info(self, key, value):
        self.info[key] = f"{key.capitalize()}: {value}"

    def format_input(self):
        self.message = ", ".join(self.info.values()) + ', ' + self.message + '\n'
        return self

    def get_summary(self):
        return self.summary

# Class to handle chatbot responses
class BotResponse:
    def __init__(self, query=UserInput()):
        self.query = query
        self.response = None
        self.active_threads = 0

    def generate_answer(self, interactive=False):
        self.response = client.send_message(model_name, self.query.message, with_chat_break=False)
        print(f"{ColorCodes.OKCYAN}Prompt >> {ColorCodes.END}", self.query.get_summary())

        if interactive:
            for msg in self.response:
                print(msg["text_new"], end="", flush=True)
        else:
            for msg in self.response:
                pass
            print(msg["text"])
        print()
        return msg["text"]

    def threaded_answer(self, description, prompt, counter):
        for msg in client.send_message(model_name, prompt, with_chat_break=True):
            pass
        print(f"{ColorCodes.OKCYAN}Prompt >> {ColorCodes.END}", end="")
        print(description + "\n" + msg["text"] + "\n" + "-" * 100 + "\n")
        self.active_threads -= 1

    def handle_multiple_inputs(self, *queries):
        for query in queries:
            thread = threading.Thread(target=self.threaded_answer, args=(query.get_summary(),
                        query.message, self.active_threads), daemon=True)
            thread.start()
            self.active_threads += 1
        
        while self.active_threads:
            time.sleep(0.1)
        
        print()
        self.clear_history()

    def clear_history(self):
        client.purge_conversation(model_name)

if __name__ == "__main__":
    input1 = UserInput("I have a headache and neck pain")
    input1.add_info("age", 22)
    input1.add_info("gender", "male")

    input2 = UserInput("I have vision problems")
    input2.add_info("age", 15)
    input2.add_info("gender", "male")

    input1.format_input()
    response = BotResponse(input1)
    answer_text = response.generate_answer(interactive=True)
    print(answer_text)

