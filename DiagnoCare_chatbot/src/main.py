from bot import Query, Reply

user_details = Query("Experiencing headache on the left side of the head with pain in the upper left part of the neck")
user_details.set_param("age", 22)
user_details.set_param("gender", "male")

while True:
    print("Please describe your issue:")
    user_input = input()
    user_details.set_message(user_input)
    query_message = user_details.create_message()
    response = Reply(query_message)
    response.send(interactive=True)
