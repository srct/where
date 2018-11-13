FROM node:10-slim

WORKDIR /server

COPY . /server
RUN npm install
RUN npm run build

EXPOSE 3000
CMD [ "npm", "start" ]
