# Use a gcloud image based on debian:buster-slim for a lean production container.
FROM gcr.io/google.com/cloudsdktool/cloud-sdk:slim

# Install golang and build Go application
FROM golang:1.13 as builder
WORKDIR /app
COPY invoke.go ./
RUN CGO_ENABLED=0 GOOS=linux go build -v -o server

# Start a new stage for the final image
FROM ghcr.io/dbt-labs/dbt-bigquery:1.6.6
USER root
WORKDIR /dbt

# Copy the compiled Go binary from the go-builder stage
COPY --from=builder /app/server ./

# Copy the main script and other files
COPY script.sh ./
COPY . ./

# Define the entry point for your container
ENTRYPOINT "./server"
