FROM python:stretch

# updates
RUN apt-get update
RUN apt-get -y install python3 python3-pip

# create ENV vars and location for app
ENV APP_HOME=/app
RUN mkdir $APP_HOME
COPY ./requirements.txt $APP_HOME
COPY ./main.py $APP_HOME
WORKDIR $APP_HOME

# install python requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# launch
ENTRYPOINT ["gunicorn", "-b", ":8080", "main:APP"]
