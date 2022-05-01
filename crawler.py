import requests
import json
from flask import Flask

app = Flask(__name__)
@app.route('/', methods = ['GET'])
def index():
    with open('data.json', 'w') as fil:
        output = crawl()
        json.dump(output, fil)

def crawl():
    finished = 0;
    while (finished == 0):
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
        finished = 1
        print(realTitle)
        print(question)
    return {'answer':realTitle, 'quest':question}
    
if __name__ == "__main__":
    app.run(port = 8000)
