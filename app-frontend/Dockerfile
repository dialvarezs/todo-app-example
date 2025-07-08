FROM oven/bun:1.2 AS build

COPY . /app
WORKDIR /app

RUN bun install --frozen-lockfile
RUN bun run build

FROM nginx:latest

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
