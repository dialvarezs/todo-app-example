FROM oven/bun:1.2 AS build

ARG API_BASE_URL

ENV VITE_API_URL=${API_BASE_URL}

COPY . /app
WORKDIR /app

RUN bun install --frozen-lockfile
RUN bun run build

FROM nginx:latest

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
