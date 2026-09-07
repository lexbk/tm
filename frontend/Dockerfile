ARG DOCKER_NODE_IMAGE
ARG DOCKER_NGINX_IMAGE

# =======================================================
# STAGE 1: Build the Vue SPA frontend
# =======================================================

FROM ${DOCKER_NODE_IMAGE} AS frontend-builder
WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./
RUN npm ci

# Copy all frontend source and build
COPY src src
COPY public public
COPY index.html tsconfig.* vite.config.* ./

RUN npm run build

# =======================================================
# STAGE 2: Final nginx runtime image
# =======================================================
FROM ${DOCKER_NGINX_IMAGE} AS frontend-runtime

# Copy built assets to nginx serving directory
COPY --from=frontend-builder /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
