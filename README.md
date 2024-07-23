# Trading Platform Simulator

This repository contains the Trading Platform Simulator, a FastAPI application that supports WebSockets connections and related tests.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Windows](#windows)
  - [Linux](#linux)
- [Running the Server and Tests](#running-the-server-and-tests)
  - [Windows](#windows-1)
  - [Linux](#linux-1)
- [Swagger Documentation](#swagger-documentation)
- [Test Report](#test-report)

## Prerequisites

Before running the application and tests, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)
- [Python](https://www.python.org/downloads/)

## Setup

### Windows

1. Clone the repository:
    ```sh
    git clone https://github.com/dancost/trading_platform_sim.git
    cd trading_platform_sim
    ```

### Linux

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

### Linux

Tested on:

- Docker version 24.0.7
- docker-compose version 1.29.2
- Ubuntu 22.04.1

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

## Swagger Documentation

Once the server is running, you can access the Swagger documentation at the following URL:

- [http://localhost:8000/docs](http://localhost:8000/docs)

This documentation provides an interactive interface to explore the API endpoints and test them.

- an offline version of the openapi.yaml can also be found [here](https://github.com/dancost/trading_platform_sim/blob/main/openapi_trading_platform.yaml)

## Test Report

The test report will be generated and can be found at:

- `tests/test_results/report.html`
- sample test report can be found in gitHub actions artifacts: https://github.com/dancost/trading_platform_sim/actions/runs/10057725081/artifacts/1730009804 (includes failing test case for demonstration purpose)

