FROM ubuntu:22.04
RUN apt-get update
RUN apt install python3-pip -y
COPY requirements.txt .
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
COPY . ./
ENV NODE_TOKEN=${NODE_TOKEN}
