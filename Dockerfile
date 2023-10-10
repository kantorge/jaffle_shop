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

# Install the gcloud command line tool
RUN apt-get update
RUN apt-get install apt-transport-https ca-certificates gnupg curl -y
RUN echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN apt-get update && apt-get install google-cloud-cli -y

# Define the entry point for your container
ENTRYPOINT "./server"
