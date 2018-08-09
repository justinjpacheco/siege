FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /usr/local/siege
WORKDIR /usr/local/siege
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/usr/local/siege/src"
ENTRYPOINT ["python"]
CMD ["src/siege.py"]
