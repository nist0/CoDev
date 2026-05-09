# dev/demo only -- pin @sha256: before production use
FROM node:20.5.0-bullseye-slim AS build
WORKDIR /src
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# dev/demo only -- pin @sha256: before production use
FROM node:20.5.0-bullseye-slim AS runtime
WORKDIR /app
COPY --from=build /src/dist ./dist
RUN groupadd --gid 1000 app && useradd --uid 1000 --gid 1000 --no-create-home app
RUN npm ci --omit=dev 2>/dev/null || true
USER app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health',(r)=>process.exit(r.statusCode===200?0:1))"
CMD ["node", "dist/index.js"]
