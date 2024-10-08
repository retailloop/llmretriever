# LLM Benchmark System

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Microservices](#microservices)
   - [Data Simulator](#data-simulator)
   - [Data Retriever](#data-retriever)
4. [Infrastructure](#infrastructure)
   - [Terraform](#terraform)
   - [Helm Charts](#helm-charts)
5. [CI/CD](#cicd)
6. [Setup and Deployment](#setup-and-deployment)
7. [Environment Variables](#environment-variables)
8. [Local Development](#local-development)
9. [Troubleshooting Guide](#troubleshooting-guide)
10. [API Documentation](#api-documentation)
11. [Performance Considerations](#performance-considerations)
12. [Security Considerations](#security-considerations)
13. [Contributing](#contributing)
14. [License](#license)

## Project Overview

This project implements a system for benchmarking Language Learning Models (LLMs) using a microservices architecture. It consists of two main services: a Data Simulator and a Data Retriever, deployed on Azure Kubernetes Service (AKS) using Terraform and Helm.

## Project Structure

```
project_root/
├── data_simulator/
│   ├── adapters/
│   ├── core/
│   ├── main.py
│   ├── models.py
│   ├── Dockerfile
│   └── requirements.txt
├── data_retriever/
│   ├── adapters/
│   ├── application/
│   ├── domain/
│   ├── ports/
│   ├── utils/
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── infrastructure/
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── helm.tf
│   │   └── outputs.tf
│   └── helm/
│       ├── data-simulator/
│       │   ├── Chart.yaml
│       │   ├── values.yaml
│       │   └── templates/
│       │       ├── deployment.yaml
│       │       └── service.yaml
│       └── data-retriever/
│           ├── Chart.yaml
│           ├── values.yaml
│           └── templates/
│               ├── deployment.yaml
│               └── service.yaml
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── docker-compose.yml
├── .env
└── README.md
```

## Microservices

### Data Simulator

Location: `./data_simulator/`

The Data Simulator is responsible for generating benchmark data for various LLMs. It simulates performance metrics and stores them in the database.

Key components:
- `adapters/`: Contains adapters for external dependencies (e.g., database, message queue).
- `core/`: Contains the core business logic for data simulation.
- `main.py`: Entry point of the application.
- `models.py`: Defines data models used in the application.
- `Dockerfile`: Instructions for building the Docker image.
- `requirements.txt`: Lists Python dependencies.

### Data Retriever

Location: `./data_retriever/`

The Data Retriever service provides an API to fetch and analyze the benchmark data generated by the Data Simulator.

Key components:
- `adapters/`: Contains adapters for external dependencies (e.g., database, cache).
- `application/`: Contains application services.
- `domain/`: Contains domain models and core business logic.
- `ports/`: Defines interfaces for external dependencies.
- `utils/`: Contains utility functions and helpers.
- `main.py`: Entry point of the application.
- `Dockerfile`: Instructions for building the Docker image.
- `requirements.txt`: Lists Python dependencies.

## Infrastructure

### Terraform

Location: `./infrastructure/terraform/`

Terraform is used to provision and manage the Azure Kubernetes Service (AKS) cluster and deploy Helm charts.

Key files:
- `main.tf`: Defines the AKS cluster and related Azure resources.
- `helm.tf`: Defines Helm releases for deploying microservices.
- `outputs.tf`: Defines outputs such as the AKS cluster's IP address.

### Helm Charts

Location: `./infrastructure/helm/`

Helm charts are used to define, install, and upgrade the Kubernetes applications.

Each microservice has its own Helm chart:
- `data-simulator/`: Helm chart for the Data Simulator service.
- `data-retriever/`: Helm chart for the Data Retriever service.

Each chart contains:
- `Chart.yaml`: Metadata about the chart.
- `values.yaml`: Default configuration values for the chart.
- `templates/`: Kubernetes manifest templates.

## CI/CD

Location: `./.github/workflows/ci-cd.yml`

This project uses GitHub Actions for continuous integration and deployment. The workflow builds Docker images, pushes them to a registry, and deploys the application to AKS using Terraform and Helm.

## Setup and Deployment

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/llm-benchmark-system.git
   cd llm-benchmark-system
   ```

2. Set up environment variables:
   Copy the `.env.example` file to `.env` and fill in the necessary values.

3. Set up GitHub Secrets:
   In your GitHub repository, go to Settings > Secrets and add the following secrets:
   - `AZURE_CREDENTIALS`: JSON object with Azure service principal details
   - `REGISTRY_USERNAME`: Username for your Docker registry
   - `REGISTRY_PASSWORD`: Password for your Docker registry

4. Push to the main branch to trigger the CI/CD pipeline:
   ```
   git push origin main
   ```

5. Monitor the GitHub Actions workflow for deployment status and outputs.

## Environment Variables

The following environment variables are required:

- `DATABASE_URL`: URL for the PostgreSQL database
- `REDIS_URL`: URL for the Redis cache
- `API_PORT`: Port for the Data Retriever API
- `RABBITMQ_URL`: URL for RabbitMQ (used by Data Simulator)

These should be set in the `.env` file and added as GitHub Secrets for use in the CI/CD pipeline.

## Local Development

To set up the project for local development:

1. Install dependencies:
   - Python 3.9+
   - Docker and Docker Compose
   - kubectl
   - Helm
   - Terraform

2. Set up virtual environments for both microservices: (This is optional)
   ```bash
   cd data_simulator
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cd ../data_retriever
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Set up local environment variables:
   Copy the `.env.example` file to `.env` and fill in the necessary values for local development.

4. Start the services using Docker Compose:
   ```bash
   docker-compose up -d
   ```

5. Access the Data Retriever API at `http://localhost:8000`

6. To run tests:
   ```bash
   cd data_simulator
   pytest
   cd ../data_retriever
   pytest
   ```

7. For local Kubernetes development, you can use Minikube:
   ```bash
   minikube start
   helm install data-simulator ./infrastructure/helm/data-simulator
   helm install data-retriever ./infrastructure/helm/data-retriever
   ```

## Troubleshooting Guide

Common issues and their solutions:

1. **Docker build fails**
   - Ensure Docker is running and you have sufficient permissions.
   - Check if all required files are present in the build context.
   - Verify that the base image specified in the Dockerfile is accessible.

2. **Kubernetes pods are not running**
   - Check pod status: `kubectl get pods`
   - View pod logs: `kubectl logs <pod-name>`
   - Describe the pod for events: `kubectl describe pod <pod-name>`

3. **Database connection issues**
   - Verify the `DATABASE_URL` environment variable is correctly set.
   - Ensure the database is running and accessible from the cluster/container.
   - Check for any firewall or network policy restrictions.

4. **API returns 500 error**
   - Check the Data Retriever logs for detailed error messages.
   - Verify all required environment variables are set correctly.
   - Ensure the Redis cache is running and accessible.

5. **Terraform apply fails**
   - Verify Azure credentials are correctly set.
   - Check for any resource constraints or quota limits in your Azure subscription.
   - Ensure there are no conflicting resources or name collisions.

## API Documentation

The Data Retriever service exposes the following endpoints:

1. **Get Ranking**
   - Endpoint: `GET /ranking/{metric}`
   - Description: Retrieves the ranking of LLMs for a specific metric.
   - Parameters:
     - `metric` (path): The metric to rank by (e.g., "TTFT", "TPS", "e2e_latency", "RPS")
   - Response:
     ```json
     [
       {
         "llm_model": "GPT-4",
         "avg_value": 95.5,
         "std_dev": 2.3
       },
       {
         "llm_model": "Claude-2",
         "avg_value": 92.1,
         "std_dev": 3.1
       }
     ]
     ```

2. **Get Available Metrics**
   - Endpoint: `GET /metrics`
   - Description: Retrieves a list of available metrics.
   - Response:
     ```json
     ["TTFT", "TPS", "e2e_latency", "RPS"]
     ```

3. **Get Available Models**
   - Endpoint: `GET /models`
   - Description: Retrieves a list of available LLM models.
   - Response:
     ```json
     ["GPT-4", "Claude-2", "BLOOM", "LLaMA"]
     ```

All endpoints require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

## Performance Considerations

To ensure optimal performance of the LLM Benchmark System:

1. **Database Indexing**: Ensure proper indexing on frequently queried fields in the PostgreSQL database, especially on the `metric` and `llm_model` columns.

2. **Caching**: The Data Retriever service uses Redis for caching. Adjust the cache expiration time based on how frequently your benchmark data changes.

3. **Kubernetes Resources**: Monitor the resource usage of your pods and adjust the resource requests and limits in the Helm charts accordingly.

4. **Scaling**: Configure Horizontal Pod Autoscaling (HPA) for the Data Retriever service to handle varying loads.

5. **Database Connection Pooling**: Implement connection pooling in the Data Retriever service to efficiently manage database connections.

6. **Asynchronous Processing**: For the Data Simulator, consider using asynchronous processing with RabbitMQ to handle large volumes of data generation without blocking.

## Security Considerations

To enhance the security of your LLM Benchmark System:

1. **Secrets Management**: Use Azure Key Vault to store and manage sensitive information like database credentials and API keys.

2. **Network Policies**: Implement Kubernetes Network Policies to control traffic flow between pods.

3. **TLS Encryption**: Use cert-manager to automatically provision and manage TLS certificates for your services.

4. **API Authentication**: Implement OAuth2 or OpenID Connect for robust API authentication and authorization.

5. **Regular Updates**: Keep all dependencies, Docker images, and Kubernetes components up-to-date with the latest security patches.

6. **Pod Security Policies**: Enforce Pod Security Policies to control the security context in which pods run.

7. **Audit Logging**: Enable Kubernetes audit logging to track all API server requests for security analysis and compliance.

8. **Image Scanning**: Implement container image scanning in your CI/CD pipeline to detect vulnerabilities before deployment.

Remember to regularly review and update your security measures as your project evolves and new security best practices emerge.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.