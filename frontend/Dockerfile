# Use an official node runtime as a parent image
FROM node:16

WORKDIR /todo-challenge/

# Install dependencies
COPY package.json yarn.lock /todo-challenge/

RUN npm install

# Add rest of the client code
COPY . /todo-challenge/

EXPOSE 3000

CMD npm start