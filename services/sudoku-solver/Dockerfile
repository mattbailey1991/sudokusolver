FROM python:3.10.12-slim
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/app/
ENV FLASK_APP=project/server.py
CMD ["python","manage.py","run"]