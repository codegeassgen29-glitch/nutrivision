# Dockerfile (frontend)
# ---------------------------------------------------------
# Packages our React app so it can run inside Docker exactly
# like the backend does. For DEVELOPMENT we run Vite's dev
# server inside the container (hot reload included).
# A separate, more optimized Dockerfile step gets added in
# Milestone 12 for the PRODUCTION build.
# ---------------------------------------------------------
FROM node:20-slim

WORKDIR /app

# Copy only package.json first, same caching trick as the backend:
# dependency installs are cached separately from source code changes.
COPY package.json ./

RUN npm install

# Copy the rest of the frontend source code.
COPY . .

EXPOSE 5173

# --host lets the dev server accept connections from OUTSIDE
# the container (needed so your browser on the host machine can reach it).
CMD ["npm", "run", "dev", "--", "--host"]
