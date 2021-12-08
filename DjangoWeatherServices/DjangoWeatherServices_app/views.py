from django.shortcuts import render
import requests
from .forms import ContactForm
from django.views.decorators.csrf import csrf_exempt
from DjangoWeatherChatBot_app.views import talk_to_chat_bot, chat_bot_data
import json

# variables
api_id = 'ef2954e48a875ae1f74e04a2aeb56694'
base_url = 'https://api.openweathermap.org/data/2.5/weather'

# views


def home(request):
    return render(request, 'home.html')


def about_us(request):
    return render(request, 'about-us.html')


def customer_feedback(request):
    form = ContactForm()
    return render(request, 'customer-feedback.html', {'form': form})


def future(request):
    return render(request, 'future.html')


@csrf_exempt
def weather_app(request):
    data_response = {}  # initialise data_response variable
    # only process a POST method request
    if request.method == 'POST':
        latitude = request.POST['latitude']  # latitude
        longitude = request.POST['longitude']  # longitude

        unit = 'metric'

        if latitude != '' and longitude != '':  # proceed only if latitude and longitude have values
            query = {'lat': latitude, 'lon': longitude, 'units': unit, 'appid': api_id}
            req = requests.get(base_url, params=query)  # call the API with query parameters

            print(req.status_code)
            if req.status_code == 200:  # if API returns success, read the results
                json_data = json.loads(req.content)
                print(json_data)
                data_response = {
                    'location': json_data['name'],
                    'current_temp': str(json_data['main']['temp']) + '°C',
                    'min_temp': str(json_data['main']['temp_min']) + '°C',
                    'max_temp': str(json_data['main']['temp_max']) + '°C',
                    'humidity': str(json_data['main']['humidity']) + '%',
                    'pressure': str('{:,.2f}'.format((json_data['main']['pressure']))) + 'hPa',
                    'condition': (json_data['weather'][0]['description']).capitalize(),
                    'wind_speed': str(json_data['wind']['speed']) + 'km/h'
                }
            elif req.status_code == 404:  # if API returns not found
                data_response = {
                    'error_message': 'No weather data was found'
                }
            else:  # if API returns any other response
                data_response = {
                    'error_message': 'There was an error while retrieving weather data'
                }
        else:
            data_response = {
                'error_message': 'Invalid input'
            }

    return render(request, 'weather-app.html', data_response)  # render request and data response to the html file


@csrf_exempt
def chat_bot(request):
    data_response = {}  # initialise data_response variable
    answer = ''

    # only process a POST method request
    if request.method == 'POST':
        question = request.POST['question']  # grab the entered question

        if question == "":
            answer = "Please enter your question"
        else:
            if question in chat_bot_data():  # check if the question is in the qa data
                print(talk_to_chat_bot(question))
                response = talk_to_chat_bot(question)  # send to chatterbot to get the corresponding answer

                if "callAPI" in str(response):  # if answer has callAPI in it, parse the json to get more info
                    json_data = json.loads(str(response))
                    print(json_data)
                    keyword = str(json_data['param']['keyword'])
                    location = str(json_data['param']['location'])
                    response = str(json_data['param']['response'])

                    if keyword != "" and location != "":
                        query = {'units': 'metric', 'appid': api_id, "q": location}
                        req = requests.get(base_url, params=query)  # call the weather API with query parameters

                        print(req.status_code)
                        if req.status_code == 200:  # if API returns success, read the results
                            json_weather_data = json.loads(req.content)
                            print(json_weather_data)
                            # assign the weather API result to the answer's placeholder
                            if keyword == "description":
                                answer = response.replace("<placeholder>", str(json_weather_data['weather'][0][keyword]))
                            else:
                                answer = response.replace("<placeholder>", str(json_weather_data['main'][keyword]))
                else:
                    answer = talk_to_chat_bot(question)  # otherwise take the direct answer

            else:
                answer = "Sorry, I'm still learning. Please ask again."  # the bot didn't understand the question

        print(answer)
        data_response = {
            'questionText': question,
            'answerText': answer
        }

    return render(request, 'chat-bot.html', data_response)

