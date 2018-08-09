FROM python:3.6
USER root

RUN python3 -m pip install lxml
RUN python3 -m pip install requests
RUN echo 'alias start="python3 energyair-bot/energyair-bot-light.py"' >> ~/.bashrc
