FROM node:20.5.0-bullseye-slim AS build
WORKDIR /src
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20.5.0-bullseye-slim AS runtime
WORKDIR /app
COPY --from=build /src/dist ./dist
RUN groupadd --gid 1000 app && useradd --uid 1000 --gid 1000 --no-create-home app
USER app
CMD ["node", "dist/index.js"]
