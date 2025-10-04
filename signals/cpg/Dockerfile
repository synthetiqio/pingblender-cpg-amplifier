FROM node:24.9.0 as build 

ARG NODE_ENV="development"
ARG VITE_API_URL=""
ARG WEB_PORT="3000"
ARG VITE_APP_MODE="standalone"
ARG VITE_IMAGE_PATH=""

USER root 

RUN npm install -g typescript 

RUN mkdir -p /home/node/app 
WORKDIR /home/node/app 
ENV IN_DOCKER=true 
ENV NODE_ENV=$NODE_ENV 
ENV VITE_API_URL=$VITE_API_URL 
ENV WEB_PORT=$WEB_PORT 
ENV VITE_APP_MODE=$VITE_APP_MODE
ENV VITE_IMAGE_PATH=$VITE_IMAGE_PATH

COPY package.json ./
COPY .npmrc ./
COPY tsconfig.json ./
COPY tsconfig.node.json ./
COPY index.html ./
COPY ./config ./config 
COPY vite.config.* ./
COPY ./mfe ./mfe 

RUN rm -rf node_modules; 

RUN npm install \
    esbuild@0.21.5\
    --save 

ENV PATH /home/node/app/node_modules/.bin:$PATH 

COPY ./src /src 

RUN if ["$NODE_ENV" == "production"]; then \
  if ["$VITE_APP_MODE" == "parent"]; then \
     npm run build:parent; \
  else \
     npm run build; \
  fi; \
  npm run build:child && \
  mkdir /home/node/app/dist/standalone/mfe && \
  mv /home/node/app/dist/child/single-spa-child.js /home/node/app/dist/standalone/mfe 
  else \
  echo "Development Environment Enabled, Skipping Build";
fi 

FROM nginx:alpine3.18 as production
COPY --from=build /home/node/app/dist/standalone /usr/share/nginx/html 
COPY ./nginx.conf /etc/nginx/conf.d/default.conf 

CMD ['nginx', "-g", "daemon off;"]

FROM build as development 

RUN npm install @rollup/rollup-linux-arm64-gnu --save-optional 

RUN if ["$VITE_APP_MODE" =! "parent"]; then \
 rm -f /home/node/app/src/single-spa-*.tsx; \
 fi 

ENV HOST=0.0.0.0 PORT=$WEB_PORT

EXPOSE $WEB_PORT

CMD if ["$VITE_APP_MODE" == "parent"]; then \
    npm run dev:parent; \
    else \
    npm run dev; \
fi

