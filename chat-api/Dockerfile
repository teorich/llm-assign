# # Use an official Node.js runtime as a parent image
# FROM node:22.5

# # Set the working directory in the container
# WORKDIR /app

# # Copy package.json and package-lock.json
# COPY package*.json ./

# # Install dependencies
# RUN yarn install

# # Copy the rest of the application
# COPY . .

# # Build the application
# RUN yarn build

# # Expose port 3000
# EXPOSE 3000

# # Start the application
# CMD ["yarn", "start:prod"]

# Stage 1: Build the application
FROM node:18 AS build

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json yarn.lock ./
RUN yarn install

# Copy application code
COPY . .

# Build the application
RUN yarn build

# Stage 2: Run the application
FROM node:18

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json yarn.lock ./
RUN yarn install --production

# Copy built application
COPY --from=build /app/dist ./dist

# Expose port
EXPOSE 3000

# Run the application
CMD ["node", "dist/main.js"]
