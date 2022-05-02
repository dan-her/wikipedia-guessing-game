import requests
import json
from flask import Flask

app = Flask(__name__)
@app.route('/', methods = ['GET'])
def index():
    with open('data.json', 'w') as fil:
        output = crawl()
        output = str(output)
        print("fuck.\n" + output)
        output = output.replace('[', '')
        output = output.replace('({', '{')
        output = output.replace(']', '')
        output = output.replace('})', '}')
        output = output.replace('\'', '\"')
        output = output.replace('\"s', '\'s')
        output = output.replace('}}, {', '}, ')
        print("fuck.\n" + output)
        output = json.loads(output)
        json.dump(output, fil)
    return output

def crawl():
    answers = {};
    questions = {};
    finished = 0;
    while (finished < 20):
        seed_url = 'https://en.wikipedia.org/wiki/Special:Random'
        page = requests.get(seed_url)
        body = page.text
    
        titleWF = body[body.find('<h1'):body.find('</h1')]
        realTitle = titleWF[titleWF.find('>'):]
        realTitle = realTitle[1:]
        if (realTitle[:3] == '<i>'):
            realTitle = realTitle[3:realTitle.find('<')]
        
        startOB = '<b>' + realTitle
        question = body[body.find(startOB):body.find('</p>')]
        question = question[3:question.find('</p>')]
        while (question.find('<') != -1):
            start = question.find('<')
            end = question.find('>')
            question = question.replace(question[start:(end+1)], '')
        if (question == ''):
            continue
        question = question.replace(realTitle, '__________')
        if (question.count('_') > 10):
            continue
        finished += 1
        answers[str(finished)] = realTitle
        questions[str(finished)] = question
    nestAnswers = {"answer":answers};
    nestQuestions = {"questions":questions};
    return {"pairs":(nestAnswers, nestQuestions)}
    
if __name__ == "__main__":
    app.run(port = 8000)
