FROM python:3.10

WORKDIR /app

COPY main.py requirements.txt ./

COPY agent_session.session bot_session.session ./

COPY src ./src

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]