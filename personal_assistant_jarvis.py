import itertools
import basian_classifer as bayes
import json
import requests
import feedparser
import smtplib
from google import search
from nltk.corpus import stopwords
from time import gmtime, strftime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
def main():
    f = open('scheduled_events.txt').readlines()
    the_time = strftime("%Y-%m-%d", gmtime())
    the_file = {i.strip('\n').split(':')[0]:i.strip('\n').split(':') for i in f}
    overdue = [i for i in the_file.keys() if int(i.split("-")[0]) < int(the_time.split("-")[0]) or int(i.split("-")[1]) < int(the_time.split("-")[1]) or int(i.split("-")[2]) < int(the_time.split("-")[2])]

    if len(overdue) > 0:
        print "You have several items that need to be completed"
        for i in overdue:
            print i[1]
    first = raw_input("do you want to check any items off your list: ")
    if first == "yes":

        answer = input("Enter the number of items: ")
        f2 = open('scheduled_events.txt').readlines()
        the_new_file = f2[:-answer]
        #f2.close()
        f3 = open("scheduled_events.txt", 'w')
        f3.write('')
        for i in the_new_file:
            f3.write(i)

        f.close()
    listings = [["weather", "forecast"], ["event", "activity", "schedule"], ["news", "headlines"], ["scores", "stats", "standings", "results"], ["send", "email"], ['search', 'google']]
    other_listings = list(itertools.chain(*listings))

    key_words = {"fetch":3, "show":4, "check":1, "set":5, "display":2, "who":7, "what":7, "where":7, "how":7, "send":8, "search":7}

    the_input = raw_input()

    user_answer = the_input.split()

    classifer_data = [i for i in user_answer if i in other_listings or i in key_words.keys()]
    print classifer_data

    new_classifer_data = []
    new_classifer_data.append(key_words[classifer_data[0]])
    new_classifer_data.extend([i+1 for i in range(len(listings)) if classifer_data[1] in listings[i]])
    print new_classifer_data

    if new_classifer_data[1] == 1:
        check_weather()

    elif new_classifer_data[1] == 2 and new_classifer_data[0] == 5:
        add_event(the_input)

    elif new_classifer_data[1] == 2 and new_classifer_data[0] == 6 or new_classifer_data[1] == 2 and new_classifer_data[0] == 2 or new_classifer_data[1] == 2 and new_classifer_data[0] == 4:
        show_schedule()

    elif new_classifer_data[1] == 3:
        news()

    elif new_classifer_data[1] == 4:
        sports()

    elif new_classifer_data[1] == 6 and new_classifer_data[0] != 7:
        show_schedule()

    elif new_classifer_data[1] == 5:
        #print the_input
        send_email(the_input)


    elif new_classifer_data[0] == 7:
        google_search(the_input)

    elif new_classifer_data[1] == 7:
        google_search(the_input)


def check_weather():
    the_time = strftime("%Y-%m-%d", gmtime())
    print the_time
    the_url = "http://api.openweathermap.org/data/2.5/weather?zip=01564,us&APPID=b04b049f63540fdf4166b59de0a01430"
    try:
        the_response = requests.get(the_url)
        the_data = json.loads(the_response.text)
        #print the_data
        print the_time
        print "Current weather in Sterling, MA:"
        print "skies:"

        print the_data["weather"][0]["description"]
        print "Temperature: ", (the_data["main"]["temp"]-273)*(9/float(5))+32, " degrees"

    except:
        print "Sir, I cannot do that do that for you right now. We have run into an internal issue."


def news():
    d = feedparser.parse("http://rss.cnn.com/rss/cnn_topstories.rss")
    print "Here are some of the latest headlines"
    for i in range(10):
        print d["entries"][i]["title"]

def sports():
    d = feedparser.parse("http://www.espn.com/espn/rss/mlb/news")
    print "Latest sports headlines: "
    for i in range(12):
        print d["entries"][i]["title"]

def show_schedule():

    print "Ok, here is a list of your uncompleted events: "
    f = open('scheduled_events.txt').readlines()
    f = [i.strip('\n') for i in f]

    for i in f:
        print i

def add_event(the_command):

    #date = raw_input("Enter the data you wish to have your event complete (2017-05-07): ")
    #event
    new = the_command.split(":")

    message = new[1]
    print message
    broken = message.split()
    print broken
    the_data = [i for i in broken if "2017" in i]
    f = open('scheduled_events.txt', 'a')
    f.write(the_data[0]+":"+message)
    f.write('\n')
    f.close()

def send_email(original_command):
    f = open('email_contacts.txt').readlines()

    f = [i.strip('\n').split(':') for i in f]

    emails = {i[0]:i[1] for i in f}
    #print emails
    the_new_command = original_command.split('.')
    #print the_new_command
    first = the_new_command[0].split()
    message = the_new_command[1]
    stops = set(stopwords.words('english'))
    second_message = message
    subject_keys = [i for i in second_message.split() if i not in stops or i != "Hi" or i != "hi"]
    people = [i for i in first if i in emails.keys()]
    person = people[0]

    the_email_object = smtplib.SMTP('smtp.gmail.com', 587)
    the_email_object.ehlo()
    the_email_object.starttls()
    the_email_object.login('jpetullo14@gmail.com', "gobronxbombers")

    #answer = raw_input("Sir, any particular subject? ")
    #sample: send email message to Mom. how are you
    the_subject = ' '.join(subject_keys[:4])
    the_email_object.sendmail('jpetullo14@gmail.com', emails[person], 'Subject:'+the_subject+'\n'+'\n'+message) #used to be answer
    print "Sir, the message has been sent."
    the_email_object.quit()

def check_email():
    pass


def google_search(query):
    key_words = ["who is", "search"]

    copy_query = query

    for i in key_words:
        copy_query = copy_query.replace(i, '')


    final = copy_query[1:len(copy_query)-1]
    print final


    urls = [i for i in search(final, tld='com', lang = 'es', stop = 10)]
    browser = webdriver.Firefox(executable_path="/Users/davidpetullo/Downloads/geckodriver")
    print "Ok, here is what I found: "
    browser.get(urls[0])
    #the_info = [requests.get(i).text[:350] for i in urls]







main()



#just make each input vector 1X3: [key_word, listing]

#in data: [key_word, listing, correct_action]
