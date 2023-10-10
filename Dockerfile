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

# Install Google Cloud SDK and authenticate with service account to enable Cloud Logging
# Install Google Cloud SDK and authenticate with service account to enable Cloud Logging
RUN apt-get update && apt-get install -y curl gnupg
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
RUN apt-get update && apt-get install -y google-cloud-sdk
RUN gcloud auth activate-service-account --key-file=/keys/service-account.json

# Define the entry point for your container
ENTRYPOINT "./server"
