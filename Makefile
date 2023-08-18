# Makefile for Dockerized Python Project

.PHONY: build run clean

# Docker image name
DOCKER_IMAGE_NAME = docker-scope

# Default target
build: run

# Build the Docker image
build-image:
	docker build -t $(DOCKER_IMAGE_NAME) .

# Run the Python script inside a Docker container
run: build-image
	docker run -v $(shell pwd):/app $(DOCKER_IMAGE_NAME)


# Clean Docker image and containers
clean:
	docker rmi -f $(DOCKER_IMAGE_NAME)

# Clean everything, including Docker images and containers
clean-all: clean
	docker system prune -af

up:
	cd opt && docker-compose up

down:
	cd opt && docker-compose down