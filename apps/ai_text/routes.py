import os
import openai
import traceback
import flask

from flask import jsonify
from apps import socketio, create_app
from . import aitext_bp

# Creating an application instance
app = create_app()

openai.organization = os.getenv('OPENAI_ORG_ID')
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.Model.list()


@aitext_bp.route('/page-title')
def page_title():

    prompt = f"You're a copywriter. Write a 9 tokens long or less homepage title for the website of an agency " \
             f"that specializes in creating AI solutions and integrations for its clients. Don't cut off the " \
             f"text. The agency's name is GoodPivot, but it's not necessary to include it."

    try:
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=25,
            temperature=0.7
        )
        return completion["choices "][0]["text"].lstrip()

    except Exception as e:
        print(e)
        status = "invalid"
        return status


@aitext_bp.route('/page-text')
def page_text():
    try:
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"You're a copywriter. Write a 35 or less tokens long summary for the homepage of an agency's "
                   f"website that specializes in creating AI solutions and integrations for its clients. Don't "
                   f"cut off the text. The agency's name is GoodPivot, but it's not necessary to include it.",
            max_tokens=75,
            temperature=0.7,
            n=1,
            stream=True)

        completion_text = ''
        for event in completion:
            if event['finish_reason'] == 'stop':
                break
            chunk = event['choices'][0]['text']
            socketio.emit('stream', chunk)
            completion_text += chunk
            print(completion_text)

        return jsonify({'status': 'ok'})

    except Exception as e:
        traceback.print_exc()
        return jsonify({'status': 'error'})


