import random
from questions import QUESTIONS

class QuizGame:
       def __init__(self):
           self.questions = random.sample(QUESTIONS, len(QUESTIONS))
           self.current_question_index = 0
           self.score = 0

       def get_current_question(self):
           return self.questions[self.current_question_index]

       def answer_question(self, answer_index):
           correct_index = self.questions[self.current_question_index]["correct"]
           if answer_index == correct_index:
               self.score += 1
               result = True
           else:
               result = False

           self.current_question_index += 1
           return result

       def is_game_over(self):
           return self.current_question_index >= len(self.questions)

       def get_score(self):
           return self.score

       def reset_game(self):
           self.__init__()