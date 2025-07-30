FROM python:3.10-slim AS tft_dps
WORKDIR /tft_dps
COPY tft_dps/pyproject.toml .
RUN pip install -e .
COPY tft_dps/ .
RUN pip install -e .
EXPOSE 4723
WORKDIR /tft_dps/tft_dps

FROM node:lts AS web
WORKDIR /web
COPY web/package.json ./
COPY web/package-lock.json ./
RUN npm i
COPY web/ .
RUN npm run build
EXPOSE 5173
