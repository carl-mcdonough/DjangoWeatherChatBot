from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json

with open('DjangoWeatherChatBot_app/qa_data.json', 'r') as f:
    qa_data = f.read()

qa_json = json.loads(qa_data)
train = []
for k, r in enumerate(qa_json):
    train.append(r['question'])
    train.append(r['answer'])

chatbot = ChatBot('DjangoBot')
# chatbot.storage.drop()  # only enable when you need to reset chatbot database
trainer = ListTrainer(chatbot)

trainer.train(train)


def talk_to_chat_bot(msg):
    return chatbot.get_response(msg)


def chat_bot_data():
    return qa_data



