import os
import openai
import traceback
import requests
import base64
import random

from . import home_bp
from apps.home.util import sd_generation
from flask import Response, render_template, jsonify, request, redirect, url_for, stream_template

# Emails sending imports
import smtplib
from email.mime.text import MIMEText

openai.organization = os.getenv('OPENAI_ORG_ID')
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.Model.list()
chat_model = 'gpt-3.5-turbo'


@home_bp.route('/', methods=["GET", "POST"])
def index():
    return render_template('home/index.html')


@home_bp.route('/home-text', methods=["GET", "POST"])
def home_text():
    print("Summary:")
    chat = False
    if request.method == 'POST':
        prompt = f"You're a copywriter. Write a 10 or less tokens long " \
         f"summary for the homepage of a firm's website that " \
         f"specializes in creating AI solutions and integrations " \
         f"for its clients. Don't cut off the text. The firm's name is GoodPivot, " \
         f"but don't include it. GoodPivot is not a platform."

    def stream():
        try:
            if chat:
                completion = openai.ChatCompletion.create(
                    model=chat_model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=100,
                    temperature=0.7,
                    n=1,
                    stream=True
                )
                for line in completion:
                    chunk = line['choices'][0].get('message', '')
                    print(chunk)
                    if chunk:
                        yield chunk
            else:
                completion = openai.Completion.create(model="text-davinci-003",
                                                      prompt=prompt,
                                                      max_tokens=100,
                                                      temperature=0.7,
                                                      n=1,
                                                      stream=True)
                for line in completion:
                    chunk = line['choices'][0].get('text', '')
                    print(chunk)
                    if chunk:
                        yield chunk
        except Exception as e:
            traceback.print_exc()
            return jsonify({'status': 'error'})

    return Response(stream(), mimetype='text/event-stream')


@home_bp.route('/home-intro', methods=["GET", "POST"])
def home_intro():
    print("Greeting:")
    chat = False
    prompt = f"Write a 9 tokens long or less friendly greeting. Start with 'Hope you're having'"

    def stream():
        try:
            if chat:
                completion = openai.ChatCompletion.create(
                    model=chat_model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=30,
                    temperature=0.7,
                    n=1,
                    stream=True
                )
                for line in completion:
                    chunk = line['choices'][0].get('message', '')
                    print(chunk)
                    if chunk:
                        yield chunk
            else:
                completion = openai.Completion.create(model="text-davinci-003",
                                                      prompt=prompt,
                                                      max_tokens=25,
                                                      temperature=0.7,
                                                      n=1,
                                                      stream=True)
                for line in completion:
                    chunk = line['choices'][0].get('text', '')
                    print(chunk)
                    if chunk:
                        yield chunk
        except Exception as e:
            traceback.print_exc()
            return jsonify({'status': 'error'})

    return Response(stream(), mimetype='text/event-stream')


@home_bp.route('/user-input', methods=["GET", "POST"])
def user_input():
    print("Response to user:")
    chat = True
    if request.method == 'POST':
        data = request.get_json()
        prompt = data.get('prompt')
        try:
            if chat:
                completion = openai.ChatCompletion.create(
                    model=chat_model,
                    messages=[
                        {"role": "system", "content": "You'll be interacting with visitors of www.goodhues.ai. Use the "
                                                      "following step-by-step instructions to respond to user inputs."
                                                      "Step 1 - The user will tell you their name and the industry "
                                                      "their company operates in. Greet them by their name and say "
                                                      "something positive about their industry.\n"
                                                      "Step 2 - Do not change the topic or let the user change it. Do "
                                                      "not ask follow up questions. Do one of these three options, "
                                                      "depending on the user's answer:\n"
                                                      "- If the user says no, invite them to learn more about GoodPivot.\n"
                                                      "- If the user doesn't provide their name or industry, invite "
                                                      "them to learn more about GoodPivot.\n"
                                                      "- If the user provides their name and/or industry, give them "
                                                      "two ideas about how they could integrate "
                                                      "AI into their operation and processes. Make it 2 paragraphs. "
                                                      "Keep it to a max of 100 words.\n"
                                                      "Step 3 - Invite them to learn more about GoodPivot. Our website "
                                                      "is goodpivot.ai but don't mention it."},
                        {"role": "user", "content": prompt}

                    ],
                    max_tokens=500,
                    temperature=0.7,
                    n=1,
                    # stream=True
                )
                print(completion["choices"][0]["message"]["content"])
                return completion["choices"][0]["message"]["content"]

        except Exception as e:
            traceback.print_exc()
            return "Our AI is experiencing high demand at the moment. Please, refresh the page and try again."


@home_bp.route('/industry-image', methods=["GET", "POST"])
def industry_image():

    if request.method == 'POST':
        prompt = request.json.get('prompt')
        print(f"Prompt: {prompt}")
        try:
            completion = openai.ChatCompletion.create(
                model=chat_model,
                messages=[
                    {"role": "system", "content": "The user will tell you their name "
                                                  "and the industry their company operates in. You will reply only with "
                                                  "the name of the industry the user told you about. Don't write anything "
                                                  "else, only the name of the industry, do not include the word 'industry'."
                                                  " If the user doesn't provide an industry, just reply only with the "
                                                  "phrase: Artificial Intelligence."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=30,
                temperature=0.7,
                n=1,
            )
            industry = completion["choices"][0]["message"]["content"]
            print(f"Industry: {industry}")

        except Exception as e:
            traceback.print_exc()
            return '/assets/img/heavy_traffic.png'


        image_prompt = f"beautiful aesthetic digital illustration representing the {industry} industry | highly " \
                       f"detailed | insanely detailed | intricate detail | lush detail | 4 k, 8 k, hdr, artstation, " \
                       f"concept art"

        industry_image = sd_generation(image_prompt, "generated_img", 'industry', 1)

        return industry_image


@home_bp.route('/send-email', methods=["GET", "POST"])
def send_email():
    # # Open a plain text file for reading.  For this example, assume that
    # # the text file contains only ASCII characters.
    # with open(textfile, 'rb') as fp:
    #     # Create a text/plain message
    #     msg = MIMEText(fp.read())
    #
    # # me == the sender's email address
    # # you == the recipient's email address
    # msg[ 'Subject' ] = 'The contents of %s' % textfile
    # msg[ 'From' ] = me
    # msg[ 'To' ] = you
    #
    # # Send the message via our own SMTP server, but don't include the
    # # envelope header.
    # s = smtplib.SMTP('localhost')
    # s.sendmail(me, [ you ], msg.as_string())
    # s.quit()

    return 'success'