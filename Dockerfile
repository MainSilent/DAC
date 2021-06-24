# Image
FROM ubuntu:20.04
RUN apt update
RUN apt install -y git tor curl

# Kalitorify
RUN git clone https://github.com/brainfucksec/kalitorify.git
RUN cd kalitorify \
	make install \
	cd / && rm -rf kalitorify

# Program
COPY . .
RUN python3 main.py