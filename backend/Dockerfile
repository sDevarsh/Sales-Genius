FROM ubuntu

RUN apt-get update
RUN apt-get install -y curl
RUN curl -sl https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get update -y
RUN apt-get install -y nodejs
RUN apt-get install python-is-python3
COPY package.json package.json
COPY package-lock.json package-lock.json
COPY app.js app.js
COPY database.db database.db
COPY final_project.py final_project.py

RUN npm install
ENTRYPOINT [ "node","app.js" ]