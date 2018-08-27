FROM ubuntu:16.04
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev
ENV FLASK_CONFIG=development
ENV FLASK_APP="run.py"
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 5000
ENTRYPOINT [ "./start_script.sh" ]