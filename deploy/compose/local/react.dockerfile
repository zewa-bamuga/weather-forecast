FROM node:20.10.0

ENV NODE_ENV development

WORKDIR /app

COPY ./frontend/package.json .
COPY ./frontend/package-lock.json .

RUN npm install

COPY ./frontend/public ./public
COPY ./frontend/src ./src

CMD ["npm", "run", "start"]
