# Image
FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y git tor curl

# Kalitorify
RUN git clone https://github.com/brainfucksec/kalitorify.git
RUN cd kalitorify && make install && cd .. && rm -rf kalitorify

# Program
COPY . .
RUN python3 main.py