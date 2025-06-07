# Domain Site: Embedded Systems

## How to run
1. install [Docker Desktop](https://www.docker.com/products/docker-desktop/)

2. Clone the repository into a folder:

    ```powershell
    git clone https://github.com/Asiandayboy/Domain.git
    cd <path to folder to cloned it into>
    ```

3. Create an .env file in the root directory with the following keys
    ```env
    GG_API_KEY=<api key for google gemini>
    SF_API_KEY=<api key for SketchFab>
    ```

4. Start the services with Docker Compose
    ```docker
    docker compose up
    ```

5. Access the app
- Flask app: http://localhost:5000
- Prometheus: http://localhost:9090

