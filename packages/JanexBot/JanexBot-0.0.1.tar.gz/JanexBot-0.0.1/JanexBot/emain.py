import json
import random
import os
import string
from Cipher import *
from Janex import *
import spacy
import numpy as np

class JanexBot:
    def __init__(self, database_file_path, model):
        self.nlp = spacy.load(f"{model}")
        self.previous_output_question = None
        self.previous_output_answer = None
        self.previous_input_question = None
        self.previous_input_answer = None
        self.database_file_path = database_file_path
        self.database = self.loadQA()

    def vectorize(self, input_string):
        input_doc = self.nlp(input_string)
        input_vectors = input_doc.vector
        return input_vectors

    def loadQA(self):
        with open(self.database_file_path, "r") as f:
            data = json.load(f)
        return data

    def give_answer(self, text):
        data = self.loadQA()
        self.previous_input_question = text
        highest_similarity = 0
        inputquestionvectors = self.vectorize(self.previous_input_question)
        for prompt in data["prompts"]:
            databasequestionvectors = prompt.get("question_vectors")
            similarity = self.calculate_cosine_similarity(inputquestionvectors, databasequestionvectors)
            if similarity > highest_similarity:
                most_similar_prompt = prompt
                highest_similarity = similarity

        answer = random.choice(most_similar_prompt["answers"])
        self.most_similar_prompt = most_similar_prompt
        return answer

    def ask_question(self, text):
        data = self.loadQA()
        self.previous_input_answer = text
        if self.previous_input_answer is not None:
            highest_similarity = 0
            inputanswervectors = self.vectorize(self.previous_input_answer)
            for prompt in data["prompts"]:
                databasequestionvectors = prompt.get("question_vectors")
                similarity = self.calculate_cosine_similarity(inputanswervectors, databasequestionvectors)
                if similarity > highest_similarity:
                    most_similar_prompt = prompt
                    highest_similarity = similarity

            question = most_similar_prompt.get("question")
            self.most_similar_prompt = most_similar_prompt
            return question
        else:
            prompt = random.choice(data["prompts"])
            self.most_similar_prompt = prompt
            question = prompt.get("question")
            return question

    def save_answer(self, text):
        self.previous_input_answer = text
        data = self.loadQA()
        for prompt in data["prompts"]:
            if prompt == self.most_similar_prompt:
                prompt["answers"].append(self.previous_input_answer)
        with open(self.database_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4, separators=(',', ': '))

    def save_question(self, question, answers):
        data = self.loadQA()
        new_prompt = {
            "question": question,
            "question_vectors": self.vectorize(question).tolist(),
            "answers": answers
        }
        data["prompts"].append(new_prompt)

        with open(self.database_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4, separators=(',', ': '))

    def generate_definition_answer(self, word):
        synsets = wordnet.synsets(word)
        if synsets:
            definition = synsets[0].definition()
            return f"The definition of {word} is: {definition}"
        else:
            return None

    def calculate_cosine_similarity(self, vector1, vector2):
        target_dim = 300
        vector1 = np.resize(vector1, target_dim)
        vector2 = np.resize(vector2, target_dim)

        dot_product = np.dot(vector1, vector2)
        norm_vector1 = np.linalg.norm(vector1)
        norm_vector2 = np.linalg.norm(vector2)

        if norm_vector1 == 0 or norm_vector2 == 0:
            return 0

        similarity = dot_product / (norm_vector1 * norm_vector2)
        return similarity

    def CheckForQuestion(self, input_string):
        input_string = input_string.strip()

        if not input_string:
            return False

        if input_string[-1] == "?":
            return True

        question_words = ["what", "when", "where", "which", "who", "whom", "why", "how"]
        for word in question_words:
            if input_string.lower().startswith(word):
                return True

        verbs = ["is", "are", "do", "does", "did", "have", "has", "can", "will", "would"]
        for verb in verbs:
            if verb in input_string.lower() and "?" in input_string:
                return True

        return False

    def train(self):
        Question = input("Question: ")
        Vectors = self.vectorize(Question)
        Answer = input("Answer: ")
        Answers = [Answer]
        self.save_question(Question, Answers)

if __name__ == "__main__":
    chatbot = JanexBot("database.json", "en_core_web_sm")
    question = chatbot.ask_question(None)
    print(f"Chatbot: {question}")
    while True:
        answer = input("You: ")
        IsQuestion = chatbot.CheckForQuestion(answer)
        if IsQuestion:
            answer = chatbot.give_answer(answer)
            print(f"Chatbot: {answer}")
        else:
            question = chatbot.ask_question(answer)
            print(f"Chatbot: {question}")
            chatbot.save_answer(answer)
