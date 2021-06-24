# Image
FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y git tor curl python3 make python3-pip

# Kalitorify
RUN git clone https://github.com/brainfucksec/kalitorify.git
RUN cd kalitorify && make install && cd .. && rm -rf kalitorify

# Requirements
pip3 install -r requirements.txt

# Run 
COPY . .
RUN python3 main.py