# Image
FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y git tor curl python3 make python3-pip wget
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata

# Kalitorify
RUN git clone https://github.com/brainfucksec/kalitorify.git
RUN cd kalitorify && make install && cd .. && rm -rf kalitorify

# Chrome
ARG CHROME_VERSION="89.0.4389.90-1"
RUN wget -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb \
  && apt-get install -y /tmp/chrome.deb \
  && rm /tmp/chrome.deb

# Requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Run 
COPY . .
RUN python3 main.py 1