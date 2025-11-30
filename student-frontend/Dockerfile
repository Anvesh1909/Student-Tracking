# Build stage
FROM node:18-alpine AS build
WORKDIR /app

COPY student-frontend/package*.json ./
RUN npm install --legacy-peer-deps

COPY student-frontend/ .
RUN npm run build

# Production stage - nginx
FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY student-frontend/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
