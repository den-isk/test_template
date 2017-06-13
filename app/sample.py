import re
from my_form import Question

questions = []
class_questions = []
max_questions = 0
def genetate_question():
    f = open("../tasks.txt","r")
    extract_file = f.read()
    raw_questions = re.split("\*\*\*\n",extract_file)
    max_questions = len(raw_questions)
    for quest in raw_questions:
        if quest == '':
            continue
        tmp = re.split("---\n",quest)
        tmp[0] = tmp[0].replace('\n','')
        tmp[1] = tmp[1].replace('\n','')
        tmp[2] = re.split("\n", tmp[2])
        tmp[2].remove('')
        tmp[3] = re.split(",",tmp[3].replace('\n',''))
        questions.append(tmp)
        class_questions.append(Question(question_text=tmp[1],question_type=tmp[0],true_answer=tmp[3],choice_of_answer=tmp[2]))
    print tmp
genetate_question()