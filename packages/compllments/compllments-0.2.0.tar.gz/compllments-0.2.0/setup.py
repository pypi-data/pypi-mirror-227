# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compllments', 'compllments.utils']

package_data = \
{'': ['*'],
 'compllments': ['data/personal_audio_files_will_go_here.txt', 'models/*']}

install_requires = \
['accelerate>=0.19.0,<0.20.0',
 'bitsandbytes>=0.39.0,<0.40.0',
 'cffi>=1.15.1,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'einops>=0.6.1,<0.7.0',
 'emoji>=2.4.0,<3.0.0',
 'ftransc>=7.0.3,<8.0.0',
 'langchain>=0.0.180,<0.0.181',
 'lxml>=4.9.2,<5.0.0',
 'num2words>=0.5.12,<0.6.0',
 'numba==0.56.4',
 'numpy==1.22.4',
 'openai>=0.27.7,<0.28.0',
 'pandas>=2.0.2,<3.0.0',
 'poethepoet>=0.20.0,<0.21.0',
 'pydub>=0.25.1,<0.26.0',
 'pynput>=1.7.6,<2.0.0',
 'pywhatkit>=5.4,<6.0',
 'transformers>=4.29.2,<5.0.0',
 'twilio>=8.2.1,<9.0.0']

entry_points = \
{'console_scripts': ['download = compllments.main:download',
                     'send = compllments.main:cli']}

setup_kwargs = {
    'name': 'compllments',
    'version': '0.2.0',
    'description': 'Send nice texts to your friends using LLMs',
    'long_description': '# compLLMents\n\n<!-- ![GitHub all releases](https://img.shields.io/github/downloads/botelhoa/compLLMents/total?style=plastic)\n![MIT License](https://img.shields.io/bower/l/compLLMents?style=plastic) -->\n\n## Description\n\nThis package enables you to send scheduled, uplifting, multi-modal AI-generated text messages to your friends. (Though they won\'t remain friends long if your only communicate is automated 😉)\n\nIt works by first using an LLM to generate a batch of positive and complimentary messages in the language of your choice. Then, a multilingual sentiment classifier scores all the generated posts and selects the most positive to send either as an SMS or over WhatsApp. Further, after recording a few minutes of audio, a custom text-to-speech model will record the message in your voice. [Here](https://colab.research.google.com/drive/1gfTlCWNFgpHdvLR5g8o-OV_a30Pfps60?usp=sharing) is the accompanying Colab notebook.\n\n\n## Table of Contents\n\n- [Installation](#installation)\n- [Usage](#usage)\n- [License](#license)\n\n## Installation\n\nFirst, ensure that [`poetry`](https://python-poetry.org/docs/#installation) is installed. \n\n```\npoetry install\npoe install-pytorch\n```\n\nTo download files to store locally and save time of future downloads, run:\n\n```\ndownload -m path/on/huggingface\n```\n\n### SMS \nFirst create a free [Twilio](https://www.twilio.com/en-us) account and create a phone number (note: Twilio automatically prepends the message `Sent from your Twilio trial account` to free-tier accounts). Copy your credentials from the dashboard into the `TWILIO_CONFIG` dictionary in `config.py`. An example config will look like:\n\n```\n {\n    "account_sid": "a_string",\n    "auth_token": "a_token",\n    "from_": "+11234567890",\n}\n```\n\n### WhatsApp\nYou must log in from your computer for the messages to send.\n\n\n### Audio\nTraining a custom test-to-speech (TTS) model requires a corpus of recordings to fine tine on. The [Mozilla Common Voice](https://commonvoice.mozilla.org/en?gclid=CjwKCAjwm4ukBhAuEiwA0zQxkwxZgF6SdsfkM8xrx5o7eayEqRS2CVbM2YnIJDUIb0VGqzSrMnBUphoC67kQAvD_BwE) initiative is a crowdsourced voice dataset. After creating an account, you can record yourself speaking sentences in the language of your choosing. Once finished recording, go to `Profile` >> `Download My Data` and copy the URLs you see into the `MOZILLA_CONFIG` dictionary in `config.py` like below:\n\n```\nMOZILLA_CONFIG = {\n    "first_url": "",\n    "second_url": "",\n}\n```\n\n## Usage\n\nTexts are sent by running:\n\n```\nsend -r recipient-name -s sender-name -n +11234567890 -l language -t type -b -sa\n```\n\n`send --help` explains the parameter options. Pass your OpenAI API key using `-o` to use their models.\n\nYou can send custom messages by chaning the text in the `TEMPLATE` object in `main.py`\n\nYou can set custom model configuration in the `INFERENCE_CONFIG` object in `conifg.py` including swapping out models, increasing the output length by chaning `max_new_tokens` or increasing the randomness in reponses by raising `temperature` or `top_p`. The default language generation model is `NousResearch/Nous-Hermes-13b` which is the [best performing open-sourced LLM](https://gpt4all.io/index.html) at the time of creation. The default sentiment analysis model is `cardiffnlp/xlm-roberta-base-sentiment-multilingual` which supports 8 languagees: `arabic`, `english`, `french`, `german`, `hindi`, `italian`, `portuguese`, and, `spanish`. \n\n\nTo schedule texts to be sent at regular intervals, create a crontab similar to the example in `cron`.\n\n\n### Examples\n\nHere are some examples messages and their sentiment score. \n\n| Message | Sentiment Score |\n| --- | --- |\n| Hey Austin! Just wanted to remind you that you are an amazing friend and such a positive force in my life. Keep being you, because you\'re pretty darn great. | 0.939329206943512 |\n| Hey Austin! Just wanted to let you know that you\'re an amazing friend and I\'m lucky to have you in my life. Keep being your awesome self and never forget how much you\'re loved and appreciated! 😊 | 0.9417279958724976 |\n| Hey Austin! Just wanted to remind you that you are an amazing friend and person. Your kindness and positivity always brings a smile to my face. Keep being you, because you\'re awesome! :) | **0.946333646774292** |\n\nThe final recording is below. This was generated by fine-tuning the text-to-speech model on 200 sentences. The more data it is given, the more life-like it will sound.\n\n\n[![Demo Doccou alpha](![image](https://github.com/botelhoa/compLLMents/assets/56508008/0a691fa1-668e-430e-805a-c787253dab87))](https://github.com/botelhoa/compLLMents/assets/56508008/4a5c5f1f-6080-4937-97c4-b1f3d458a513)\n\n\n\n## Tests\n\nForthcoming...\n\n\n## Releases\n\n**0.1.0**\n- [x] Self-hosted or OpenAI generated compliments\n- [x] SMS and WhatsApp supports\n- [x] Sentiment-based message selection\n- [x] Message scheduling\n- [x] User-friendly Colab notebook\n\n**0.1.1**\n- [x] Fixed `ReadME.md`\n\n**0.2.0**\n- [x] Custom voice messages\n- [x] Birthday and custom message templates\n\n\n\n## License\n\nMIT License\n\nCopyright (c) [2023] [Austin Botelho]\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n\n\n',
    'author': 'Austin Botelho',
    'author_email': 'austinbotelho@nyu.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
