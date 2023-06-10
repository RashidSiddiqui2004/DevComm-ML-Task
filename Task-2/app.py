import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# give your api key as parameter

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_promptSuperHero(gender, actualName, post, superpowers):
    if gender == 'Male':
        gender = "Boy"
    elif gender == "Female":
        gender = "Girl"

    return """ There is a {} named {} who is a {} and has actually got superpowers.
 the superpower is/are that {}.
  Suggest me a good name for the hero. Give me answer in this format:- Name : []""".format(gender, actualName, post,
                                                                                           superpowers)


def generate_promptPet(family, adjective, traits):
    return """I have a {} {} which is very close to my heart and I can't live without it.
    Its traits are that it is {}.
    Suggest me 3 nice and fantastic names for it.
     Give me answers in this format:- Name : []""".format(family, adjective, traits)


def generate_promptStore(owner, title):
    return """
    I am {}, I am opening a new brand new store in my city at a grand level that deals 
    with supply of {}. 
    Suggest me some brilliant names for my company .Give me answer in this format:- Name : []
    """.format(owner, title)


def generate_promptComp(name, businessOf, purpose):
    return """I am {}, I am opening a new company that deals with supply of {} to customers.
    The purpose of my comapany is {}
   Suggest me some brilliant names for my company.
   Give me answer in this format:- Name : []""".format(name.capitalize(), businessOf, purpose)


def standardName(name):
    return ("".join(name.split(" "))).lower()


def customerSuppport(appliance, brand, complaint):
    return """
    Customer Support: I am facing difficulty in using the {} of {} brand. The problem with the {} is - {}.
      Suggest me some idea to rectify it?  Give me top 3 things that I should do in a short and crisp list.""".format(
        appliance, brand, appliance, complaint)


def getTasks(response):
    ans1, ans2, ans3 = "", "", ""

    pt1 = 0

    while response[pt1] != '2':
        ans1 += response[pt1]
        pt1 += 1

    while response[pt1] != '3':
        ans2 += response[pt1]
        pt1 += 1

    while pt1 < len(response):
        ans3 += response[pt1]
        pt1 += 1

    return ans1, ans2, ans3


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":

        modelselector = "hello"

        try:
            modelselector = request.form["modelSelection"]
        except:
            print("hi")

        if modelselector == 'modelSelection':

            modelToUse = request.form["model"]

            if standardName(modelToUse) == 'companyname':
                return render_template('companyName.html', result="")

            elif standardName(modelToUse) == 'petname':
                return render_template('PetName.html', result="")

            elif standardName(modelToUse) == 'storename':
                return render_template('groceryStore.html', result="")

            elif standardName(modelToUse) == 'superheroname':
                return render_template('superHero.html', result="")

            elif standardName(modelToUse) == 'customercare':
                return render_template('customerSupport.html', result="")

            else:
                return render_template('navigation.html', result="Invalid Input, Please enter again!")

        else:

            query = request.form["queryType"]

            if query == 'petName':
                family = request.form["family"]
                adjective = request.form["adjective"]
                traits = request.form["traits"]

                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=generate_promptPet(family, adjective, traits),
                    temperature=0.6,
                )
                return render_template('PetName.html', result=response.choices[0].text)

            elif query == 'company':

                owner = request.form["ownerName"]
                businessOf = request.form["service"]
                purpose = request.form["purpose"]

                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=generate_promptComp(owner, businessOf, purpose),
                    temperature=0.6,
                )
                return render_template('companyName.html', result=response.choices[0].text)

            elif query == 'store':
                owner = request.form["ownerName"]
                businessOf = request.form["service"]
                # purpose = request.form["purpose"]

                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=generate_promptStore(owner, businessOf),
                    temperature=0.6,
                )

                return render_template('groceryStore.html', result=response.choices[0].text)

            elif query == 'superhero':

                gender = request.form["gender"]
                name = request.form["actualName"]
                post = request.form["Job"]
                superpowers = request.form["powers"]

                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=generate_promptSuperHero(gender, name, post, superpowers),
                    temperature=0.6,
                )

                return render_template('superHero.html', result=response.choices[0].text)

            elif query == 'customerSupport':

                appliance = request.form["appliance"]
                brand = request.form["brand"]
                issue = request.form["issue"]

                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=customerSuppport(appliance, brand, issue),
                    temperature=0.6, max_tokens=200
                )

                response = response.choices[0].text

                response1, response2, response3 = getTasks(response)

                additional = "Follow the given steps to get satisfactory results:-"

                return render_template('customerSupport.html', result1=response1, result2=response2,
                                       result3=response3, intro=additional)

    else:
        return render_template('navigation.html')

    # result = request.args.get("result")

    # return render_template("navigation.html")
