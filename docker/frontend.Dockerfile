FROM node:20-bullseye

WORKDIR /app

COPY frontend/package*.json ./

RUN npm install

COPY frontend .

EXPOSE 5137

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5137"]