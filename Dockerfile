FROM ubuntu:18.04

COPY . /

WORKDIR /

RUN apt-get install nodejs && \
    apt-get install npm

CMD ["npm", "start"]
