FROM node:20-alpine

WORKDIR /app

# backend 의존성 설치
COPY backend/package*.json ./backend/
RUN cd backend && npm install --omit=dev

# 소스 복사(backend + web)
COPY backend ./backend
COPY web ./web

# 로그 디렉토리(볼륨으로 덮어씀)
RUN mkdir -p /logs

EXPOSE 3000
CMD ["node", "backend/server.js"]
