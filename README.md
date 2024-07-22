# Trading Platform Simulator

This repository contains the Trading Platform Simulator, a FastAPI application that supports WebSockets connections. It includes a comprehensive test suite to validate the API and WebSocket functionality.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Windows](#windows)
  - [Linux/Unix](#linuxunix)
- [Running the Server and Tests](#running-the-server-and-tests)
  - [Windows](#windows-1)
  - [Linux/Unix](#linuxunix-1)
- [Swagger Documentation](#swagger-documentation)

## Prerequisites

Before running the application and tests, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)

## Setup

### Windows

1. Clone the repository:
    ```sh
    git clone https://github.com/dancost/trading_platform_sim.git
    cd trading_platform_sim
    ```

### Linux/Unix

1. Clone the repository:
    ```sh
    git clone https://github.com/dancost/trading_platform_sim.git
    cd trading_platform_sim
    ```

## Running the Server and Tests

### Windows

1. Ensure Docker is running.
2. Open a terminal (PowerShell) and navigate to the project directory:
    ```sh
    cd trading_platform_sim
    ```

3. Define the environment variable for the desired test plan:

    - Smoke test plan:
        ```sh
        $env:PYTEST_ARGS="-s -v -m smoke --html=test_results/report.html --self-contained-html --capture=sys"
        ```

    - Negative test plan:
        ```sh
        $env:PYTEST_ARGS="-s -v -m negative --html=test_results/report.html --self-contained-html --capture=sys"
        ```

    - Websockets test plan:
        ```sh
        $env:PYTEST_ARGS="-s -v -m ws --html=test_results/report.html --self-contained-html --capture=sys"
        ```

    - Performance test plan:
        ```sh
        $env:PYTEST_ARGS="-s -v -m performance --html=test_results/report.html --self-contained-html --capture=sys"
        ```

    - Run all tests:
        ```sh
        $env:PYTEST_ARGS="-s -v --html=test_results/report.html --self-contained-html --capture=sys"
        ```

4. Build and run the Docker containers:
    ```sh
    docker-compose up --build
    ```

### Linux/Unix

1. Ensure Docker is running.
2. Open a terminal and navigate to the project directory:
    ```sh
    cd trading_platform_sim
    ```

3. Define the environment variable for the desired test plan:

    - Smoke test plan:
        ```sh
        export PYTEST_ARGS="-s -v -m smoke --html=test_results/report.html --self-contained-html --capture=sys"
        ```

    - Negative test plan:
        ```sh
        export PYTEST_ARGS="-s -v -m negative --html=test_results/report.html --self-contained-html --capture=sys"
        ```

    - Websockets test plan:
        ```sh
        export PYTEST_ARGS="-s -v -m ws --html=test_results/report.html --self-contained-html --capture=sys"
        ```

    - Performance test plan:
        ```sh
        export PYTEST_ARGS="-s -v -m performance --html=test_results/report.html --self-contained-html --capture=sys"
        ```

    - Run all tests:
        ```sh
        export PYTEST_ARGS="-s -v --html=test_results/report.html --self-contained-html --capture=sys"
        ```

4. Build and run the Docker containers:
    ```sh
    docker-compose up --build
    ```

### Test Report

The test report will be generated and can be found at:

- `tests/test_results/report.html`

## Swagger Documentation

Once the server is running, you can access the Swagger documentation at the following URL:

- [http://localhost:8000/docs](http://localhost:8000/docs)

This documentation provides an interactive interface to explore the API endpoints and test them.

## Additional Notes

- Ensure that the necessary ports are open and not being used by other applications.
- Modify the `docker-compose.yml` file if needed to suit your environment or setup requirements.
