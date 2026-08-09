FROM node:20-alpine

WORKDIR /app

# Copy package files and install dependencies
COPY package.json ./
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose the Next.js port
EXPOSE 3000

# Start the development server
CMD ["npm", "run", "dev"]
