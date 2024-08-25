from django.shortcuts import render, redirect
from cs50 import SQL
from django.shortcuts import HttpResponse
import requests

from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

import os
import dotenv
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import dotenv
dotenv.load_dotenv()

db = SQL(
    "sqlite:///data.db"
)

os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

chat_history = None

# check session on login and sighnup
def if_session(func):
    def wrapper(request):
        if 'username' in request.session:
            return redirect('home')
        else:
            return func(request)
    return wrapper

def no_session(func):
    def wrapper(request):
        if 'username' not in request.session:
            return redirect('login')
        else:
            return func(request)
    return wrapper
        


# Create your views here.
@if_session
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if not(username or password):
            return redirect('login')

        res = db.execute(
            "SELECT * FROM login WHERE username = ? and password = ?",
            username,
            password,
        )

        if res:
            user = db.execute(
                "SELECT * FROM user WHERE login_id = ?",
                res[0]['id']
            )
            request.session["username"] = username
            request.session["login_id"] = res[0]['id']
            request.session['gender'] = user[0]['gender']
            return redirect("home")
        else:
            return redirect("login")
        
    return render(request, "login.html")



@if_session
def signup(request):
    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get('gender')
        


        if not gender:
            return redirect('signup')
        
        user = db.execute('SELECT id FROM user WHERE email = ?', email)
        image_id = gender.strip() + '.png'
        if user:
            return HttpResponse(
                "Email is already taken. Please choose a different one."
            )

        login_id = db.execute(
            'INSERT INTO login(username, password, status) VALUES (?, ?, "user")',
            email,
            password,
        )
        user = db.execute(
            "INSERT INTO user(name, email, login_id, gender, image) VALUES (?, ?, ?, ?, ?)",
            name,
            email,
            login_id,
            gender, 
            image_id
        )

        if user is not None:
            request.session["username"] = email
            request.session["login_id"] = login_id
            request.session['gender'] = gender
            return redirect("home")

    return render(request, "signup.html")

@no_session
def home(request):

    questions = db.execute("SELECT * FROM questions WHERE question_type IN ('public', ?) ORDER BY id DESC LIMIT 10",
                            request.session['gender'])
    
    if "search_data" in request.session:
        questions = request.session["search_data"]
        del request.session["search_data"]

    context = {"questions": questions, 'gender': request.session['gender']}

    return render(request, "home.html", context)


def add_question(request):
    question = request.POST["question"].strip().capitalize()
    description = request.POST["description"].strip()
    question_type = request.POST["q_type"]
    login_id = request.session['login_id']


    if len(question) < 7 or len(description) < 15: 
        return redirect('home')
    
    db.execute("INSERT INTO questions(question, description, login_id, question_type) values(?, ?, ?, ?)",
               question, description, login_id, question_type)
    return redirect("home")


def search_question(request):
    question = request.POST["question"]
    questions = db.execute(
        "SELECT * FROM questions WHERE question LIKE ? LIMIT 10", "%" + question + "%"
    )

    request.session["search_data"] = questions
    return redirect("home")

def question_post(request):
    question_id = int(request.POST["question_id"])
    request.session['discussion_qid'] = question_id
    return redirect('discussion')
    
@no_session
def discussion(request):
    if 'discussion_qid' not in request.session:
        return redirect('home')
    
    question_id = request.session['discussion_qid']
    gender = request.session['gender']
    
    question = db.execute("SELECT questions.id, name, image, question, question_type, description, questions.login_id FROM questions join user on user.login_id = questions.login_id where questions.id = ?", question_id)
    
    if question[0]['question_type'] != 'public' and question[0]['question_type'] != gender:
        return redirect('home')

    answers = db.execute("SELECT discussion.id, name, image, answer, question_id, discussion.login_id FROM discussion join user on discussion.login_id = user.login_id where question_id = ?", question_id)

    if question is None:
        return HttpResponse("invalid question")

    context = {
        "question": question,
        "discussions": answers,
        'login_id': request.session['login_id']
    }

    return render(request, "discussion.html", context)


def add_discussion(request):
    result = request.POST["add_discussion"].strip()
    question_id = request.POST['question_id']
    login_id = request.session['login_id']

    print(login_id, question_id, '\n\n\n')

    if result:
        db.execute(
            "INSERT INTO discussion (answer, question_id, login_id) VALUES (?, ?, ?)",
            result,
            question_id,
            login_id
        )

    return redirect('discussion')


def logout(request):
    print('yes')
    del request.session['username']
    print(request.session)
    return redirect('login')


def profile(request):
    login_id = request.session['login_id']
    questions = db.execute('SELECT * FROM questions WHERE login_id = ?', login_id)
    user_details = db.execute('SELECT * FROM user WHERE login_id = ?', login_id)
    print(user_details)
    context = {
        'questions': questions,
        'user_details': user_details[0]
    }
    return render(request, 'profile.html', context)

datada = []

def articles(request):
    global datada
    
    
    if datada:
        data = datada
    else:
        url = ('https://newsapi.org/v2/everything?'
       'q=womens+health&'
       'sortBy=popularity&'
       'apiKey=18d6d6c5963d4a52a44c74c2d325d598')

        response = requests.get(url)

        res = response.json()

        if res['status'] != 'ok':
            return HttpResponse('error occured')

        data = res['articles']
        datada = data

    if request.method == "POST":
        search = request.POST['search_article']
        search = "+".join(search.split())
        url = ('https://newsapi.org/v2/everything?'
       'q='+search+'&'
       'sortBy=popularity&'
       'apiKey=18d6d6c5963d4a52a44c74c2d325d598')

        response = requests.get(url)

        res = response.json()

        if res['status'] != 'ok':
            return HttpResponse('error occured')

        data = res['articles']
        datada = data

    context = {
        'data' : data
    }
    return render(request, 'articles.html', context)

# -----working ----------------- 




# only collects history if any and if not history create new one 
def chat(request):
    global chat_history  
    chat_history = chat_history if chat_history else bot()
    if chat_history.prev:
        print(chat_history.qna, chat_history.prev)
    else:
        chat_history.get_question()
    
    user_details = db.execute('SELECT name, image FROM user WHERE login_id = ?', request.session['login_id'])

    context =  {'data': chat_history.qna, 'ai_question': chat_history.prev, 'user_details': user_details}
    return render(request, 'chat.html', context)

# resets the chatbot history 
def reset(request):
    global chat_history
    print('---------------------------------working----------------------')
    chat_history = bot()
    chat_history.qna = []
    chat_history.message = ['Hi']
    chat_history.prev = None
    
    return redirect('chat')



def chat_bot(request):
    global chat_history

    answer = request.POST['question']
    question = chat_history.get_question(answer)

    return redirect('chat')























def remove_discussion(request):
    login_id = request.session['login_id']
    
    discussion_id = request.POST['remove']
    db.execute('DELETE FROM discussion WHERE login_id = ? and id = ?', login_id, discussion_id)
    return redirect('discussion')


def remove_question(request):
    login_id = request.session['login_id']
    
    question_id = int(request.POST['q_remove'])
    db.execute('DELETE FROM discussion WHERE login_id = ? and question_id = ?', login_id, question_id)
    db.execute('DELETE FROM questions WHERE login_id = ? and id = ?', login_id, question_id)
    return redirect('home')


class bot:
    qna = []
    prev = None
    model = ChatGoogleGenerativeAI(model='gemini-pro' ,convert_system_message_to_human=True)
    prompt = [('system', """
            
            you are an personal chat bot for a user things that you should do while interacting:

            * ask about the problems that the user is facing 
            * ask the details of the problem 
            * if the problems is health related ask for symptoms etc
            * help the person if he/she is facing emotional scars
            * answer him how to solve or cure the problem they are facing
            * should only replay within 100 character like chatting
            
            """
        ), MessagesPlaceholder('message')]
    message = [HumanMessage('Hi')]
    template = ChatPromptTemplate.from_messages(prompt)
    output_parser = StrOutputParser()
    chain = template | model | output_parser



    def get_question(self, answer=''):

            
        llm = self.chain
        
        if answer:
            self.message.append(HumanMessage(answer))
            self.qna.append({'question': self.prev, 'answer': answer})
        
        # response from the llm model 
        print('before', self.message)
        response = llm.invoke(self.message)
        print(response)

        self.message.append(AIMessage(response))
        self.prev = response
        # print(f'human {answer}\n ai {response}\n previous {self.prev}\n QNA {self.qna}')
        
        
        return response
    

    
    


