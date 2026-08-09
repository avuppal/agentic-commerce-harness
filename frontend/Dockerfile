FROM node:20-slim

WORKDIR /app

# Copy package files and install dependencies
COPY package.json ./
# Increase network timeouts to prevent ETIMEDOUT on slow docker bridge networks
RUN npm install --fetch-timeout=600000 --network-timeout=600000

# Copy the rest of the frontend code
COPY . .

# Expose the Next.js port
EXPOSE 3000

# Start the development server
CMD ["npm", "run", "dev"]
