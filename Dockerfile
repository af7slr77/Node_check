FROM ubuntu:22.04
RUN apt-get update
RUN apt install python3-pip -y
COPY requirements.txt .
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
COPY . ./
ENV PYTHONUNBUFFERED = 1
ENV NODE_TOKEN=6071105822:AAGJk8ZoMECAppbiS9s-a0dKCI557tghEhQ
#CMD ["python3", "run_blocks.py"]