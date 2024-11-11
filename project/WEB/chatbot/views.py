from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django_plotly_dash import *

from dashboards.watching_word import app 
from dashboards.D_02_visualization_origin import app
from dashboards.answering_service import generate_answer_plus_date, if_date

from opensearchpy import OpenSearch
import json
import openai
from dotenv import load_dotenv
import os

load_dotenv()


def index(request):
    return render(request, 'index.html') 

# def dash_app(request):
#     # Dash 앱을 HTML로 변환
#     plot_div = pio.to_html(dash_app_instance, full_html=False)
    
#     return render(request, 'dash_app_template.html', context={'plot_div': plot_div})

# 질문에 날짜가 포함된 경우 해당 날짜로 필터링하여 답변 생성
def query_with_date(question):
    index_name = "raw_data"
    start_date = if_date(question)  # 질문에서 시작 날짜 추출
    end_date = if_date(question)  # 종료 날짜를 시작 날짜와 동일하게 설정 (단일 날짜)
    response_text = generate_answer_plus_date(question, index_name, pre_msgs=None, start_date=start_date, end_date=end_date)
    return response_text


@csrf_exempt
@require_http_methods(["POST"])
def chat(request):
    data = json.loads(request.body)
    user_message = data.get('message', '')
    ai_message = query_with_date(user_message)
    return JsonResponse({'message': ai_message})
    '''
    # OpenAI API를 사용하여 응답 생성
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Your name is 우대리, You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    )

    ai_message = response.choices[0].message['content']
    return JsonResponse({'message': ai_message})
    '''
######



# chart 4
def recent_posts(request):
    # 인증 정보를 사용하여 OpenSearch 클라이언트 생성
    host = os.getenv("OPENSEARCH_HOST")
    port = os.getenv("OPENSEARCH_PORT")
    auth = (os.getenv("OPENSEARCH_ID"), os.getenv("OPENSEARCH_PASSWORD")) # For testing only. Don't store credentials in code.

    client = OpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = False
    )
    # Elasticsearch 쿼리 작성
    query = {
        "sort": [
            {"날짜": {"order": "desc"}}
        ],
        "size": 10,
        "_source": ["날짜", "제목"]
    }

    # 'raw_data' 인덱스에서 검색
    response = client.search(index="raw_data", body=query)
    posts = [
        {
            "date": hit["_source"].get("날짜"),
            "title": hit["_source"].get("제목")
        }
        for hit in response["hits"]["hits"]
    ]

    # posts 데이터를 템플릿으로 전달
    return render(request, "index.html", {"posts": posts})


# importing render and redirect
from django.shortcuts import render, redirect
# importing the openai API
import openai
# loading the API key from the secret_key file
openai.api_key = os.getenv('OPENAI_API_KEY')

# this is the home view for handling home page logic
def home(request):
    try:
        # if the session does not have a messages key, create one
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "You are now chatting with a user, provide them with comprehensive, short and concise answers."},
            ]
        if request.method == 'POST':
            # get the prompt from the form
            prompt = request.POST.get('prompt')
            # get the temperature from the form
            temperature = float(request.POST.get('temperature', 0.1))
            # append the prompt to the messages list
            request.session['messages'].append({"role": "user", "content": prompt})
            # set the session as modified
            request.session.modified = True
            # call the openai API
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=request.session['messages'],
                temperature=temperature,
                max_tokens=1000,
            )
            # format the response
            formatted_response = response['choices'][0]['message']['content']
            # append the response to the messages list
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True
            # redirect to the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': temperature,
            }
            return render(request, 'assistant/home.html', context)
        else:
            # if the request is not a POST request, render the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.1,
            }
            return render(request, 'assistant/home.html', context)
    except Exception as e:
        print(e)
        # if there is an error, redirect to the error handler
        return redirect('error_handler')

def new_chat(request):
    # clear the messages list
    request.session.pop('messages', None)
    return redirect('home')

# this is the view for handling errors
def error_handler(request):
    return render(request, 'assistant/404.html')
