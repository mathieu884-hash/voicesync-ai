FROM node:18-alpine AS base

WORKDIR /app

FROM base AS dependencies
COPY package.json package-lock.json ./
RUN npm ci

FROM base AS build
COPY package.json package-lock.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM base AS runtime
ENV NODE_ENV=production

COPY --from=dependencies /app/node_modules ./node_modules
COPY --from=build /app/.next ./.next
COPY --from=build /app/public ./public
COPY package.json ./

EXPOSE 3000

CMD ["npm", "start"]
