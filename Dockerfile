# Multi-stage Dockerfile for building helm_sdkpy with bundled dependencies
# This creates a self-contained Python wheel with embedded Helm Go library

# Stage 1: Build environment with all dependencies
FROM ubuntu:24.04 AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    ca-certificates \
    # Go compiler
    golang-1.22 \
    # Python build tools
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Set up Go environment
ENV PATH="/usr/lib/go-1.22/bin:${PATH}"
ENV GOPATH="/go"
ENV PATH="${GOPATH}/bin:${PATH}"

WORKDIR /build

# Copy source code
COPY . .

# Stage 2: Build Go shim as shared library
FROM builder AS go-build

WORKDIR /build/go

# Download Go dependencies
RUN go mod download && go mod tidy

# Build the Go shared library
RUN mkdir -p /build/helm_sdkpy/_lib/linux-amd64 && \
    cd shim && \
    go build -buildmode=c-shared \
        -o /build/helm_sdkpy/_lib/linux-amd64/libhelm_sdkpy.so \
        main.go

# Verify the shared library was built
RUN ls -lh /build/helm_sdkpy/_lib/linux-amd64/libhelm_sdkpy.so && \
    ldd /build/helm_sdkpy/_lib/linux-amd64/libhelm_sdkpy.so || true

# Stage 3: Build Python wheel
FROM go-build AS wheel-build

WORKDIR /build

# Install UV for fast Python package management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Build the wheel
RUN uv build

# List built wheel and sdist
RUN ls -lh dist/

# Stage 4: Extract artifacts
FROM scratch AS artifacts
COPY --from=wheel-build /build/dist/*.whl /
COPY --from=wheel-build /build/dist/*.tar.gz /
COPY --from=go-build /build/helm_sdkpy/_lib/linux-amd64/libhelm_sdkpy.so /
