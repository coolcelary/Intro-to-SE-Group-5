FROM node:14-slim

ENV NODE_ENV development

WORKDIR /usr/src/app

COPY . .

RUN npm install express cookie-parser child_process
RUN apt-get update && apt-get install -y python3 python3-pip


EXPOSE 3000

CMD ["npm", "start"]
