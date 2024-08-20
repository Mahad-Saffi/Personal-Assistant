import speech_recognition as sr
import pyttsx3
import requests
import wikipedia
import webbrowser
import datetime

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed
engine.setProperty('volume', 1.0)  # Volume

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen(duration):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
            print("Processing...")
            query = recognizer.recognize_google(audio, language='en-in')
            return query.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try speaking again.")
            speak("I didn't hear anything. Please try speaking again.")
            return "none"
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
            return "none"
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak("I'm having trouble connecting to the service.")
            return "none"


def ask_wolframalpha(query):
    api_key = <your_api_key_of_wolframaalpha>
    url = f"http://api.wolframalpha.com/v1/result?i={query}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error querying WolframAlpha: {e}")
        return "I couldn't retrieve the information right now."


def news():
    news_api = <Your_news_api_key>
    current_date = datetime.date.today().strftime("%Y-%m-%d")

    url = f"https://newsapi.org/v2/everything?q=Apple&from={current_date}&sortBy=popularity&apiKey={news_api}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        today_news = response.json()

        for n in range(len(today_news["articles"])):
            webbrowser.open(today_news["articles"][n]["url"])

            speak(today_news["articles"][n]["title"])
            intermediate_listen = listen(2)
            if 'skip' in intermediate_listen:
                continue
            elif 'stop' in intermediate_listen:
                break

            speak(today_news["articles"][n]["description"])
            last_listen = listen(3)
            if 'stop' in last_listen:
                break
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving news: {e}")
        speak("I'm having trouble fetching the news right now.")


def search_browser(web):
    webbrowser.open(f"https://{web}.com")


def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options[:5]}"
    except wikipedia.exceptions.PageError:
        return "No page found for your query."


def main():
    speak("How can I assist you today?")
    while True:
        query = listen(100000)

        if 'wikipedia' in query:
            query = query.replace("wikipedia", "")
            results = search_wikipedia(query)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'who is' in query or 'what is' in query or 'tell me about' in query:
            results = ask_wolframalpha(query)
            speak(results)

        elif 'open' in query:
            query = query.replace("open ", "")
            search_browser(query)

        elif 'news' in query:
            news()

        elif 'exit' in query or 'stop' in query:
            speak("Goodbye...")
            break


if __name__ == "__main__":
    main()
