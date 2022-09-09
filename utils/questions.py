import pandas as pd
from random import randint

interview_questions='interview_questions.csv'

def load_questions():
    questions = pd.read_csv(interview_questions,
                            header=0,
                            names=["Area", "Question"],
                            on_bad_lines='skip',
                            delimiter=";")
    return questions

def get_rand_question(questions, job_name):
    questions=questions[questions["Area"]==job_name]
    no_of_q=questions.shape[0]
    index=randint(0, no_of_q-1)
    return questions["Question"].iloc[index]
