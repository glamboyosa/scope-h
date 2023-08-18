# Use the official Node.js 18 image as the base image
FROM node:18

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json .
COPY tailwind.config.js postcss.config.js .

# Install dependencies
RUN npm install

# Copy the rest of the application code
# COPY public/ ./public/
COPY . .



# Start the React app with automatic reloading
CMD ["npm", "run" ,"dev"]
