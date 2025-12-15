# build env
FROM node:13.12.0-alpine as build
WORKDIR /app

# 1. DEFINE THE BUILD ARGUMENT # Note: Use REACT_APP_ prefix for React/CRA projects
#
ARG REACT_APP_API_URL=http://localhost:3000
# 2. SET THE ENV VAR FOR THE BUILD PROCESS
ENV REACT_APP_API_URL=$REACT_APP_API_URL
# See also the frontend/src/api/index.js

COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build
CMD cp -r build result_build
