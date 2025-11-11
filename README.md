## Structure of the repository:

The application is composed of one Flask (v3.1.2) backend and one Angular (v20.3.8) frontend with the following structure:

```
.
├── README.md
├── backend
├── docker-compose.yaml
├── frontend
├── pyproject.toml
└── tests
```

## Pre-requisites 
### To build the project:
```
Python 3.12
Angular 20.3.9
docker
docker-compose
```

### Pre-requisites to run the project:
```
docker
docker-compose
```

## How to build the project:

### How to compile Python dependencies
`uv pip compile requirements.in -o requirements.txt`

### How to install Python dependencies 
`uv pip install -r requirements.txt`

### How to run with flask
In backend folder:
`flask run`

### How to run with gunicorn
`gunicorn --bind 0.0.0.0:5000 --chdir ./backend wsgi:application`

### How to run with Docker

#### Docker build
To run in the root folder:
`docker build -f backend/Dockerfile.backend -t backend:0.0.1 ./backend`
`docker build -f frontend/Dockerfile.frontend -t frontend:0.0.1 ./frontend`

`docker run -p 5000:5000 backend:0.0.1`
`docker run -p 8080:80 frontend:0.0.1`


### Run in production
The recommended way to run the project in production is with docker-compose.

It is going to start smoothly the two containers (backend first then frontend).

#### How to run the app with docker-compose
`docker-compose up -d`

#### How to run the CLI on the docker container
Once the backend container is running, it exposes the CLI.
```sh
docker exec -it flask_backend_app give-me-odds backend/examples/example1/millennium-falcon.json backend/examples/example1/empire.js
```
In the example, flask_backend_app is the container name given by docker-compose.

> **⚠️ Warning: CLI can only access the files already inside the container !**
>
> The container as defined in the current state  
> of the repo only contain `backend/examples` files.  
> See [Limitations and Future evolutions](#limitations-and-future-evolutions)
>  

## Project inputs

### millennium-falcon data

**millennium-falcon.json**
```json
{
  "autonomy": 6,
  "departure": "Tatooine",
  "arrival": "Endor",
  "routes_db": "universe.db"
}
```
   - autonomy (integer): autonomy of the Millennium Falcon in days.
   - departure (string): Planet where the Millennium Falcon is on day 0.
   - arrival (string): Planet where the Millennium Falcon must be at or before countdown.
   - routes_db (string): Path toward a SQLite database file containing the routes. The path can be either absolute or relative to the location of the `millennium-falcon.json` file itself.

The SQLite database will contain a table named ROUTES. Each row in the table represents a space route. Routes can be travelled **in any direction** (from origin to destination or vice-versa).

   - ORIGIN (TEXT): Name of the origin planet. Cannot be null or empty.
   - DESTINATION (TEXT): Name of the destination planet. Cannot be null or empty.
   - TRAVEL_TIME (INTEGER): Number days needed to travel from one planet to the other. Must be strictly positive.

| ORIGIN   | DESTINATION | TRAVEL_TIME |
|----------|-------------|-------------|
| Tatooine | Dagobah     | 4           |
| Dagobah  | Endor       | 1           |

### empire data

a JSON file containing the data intercepted by the rebels about the plans of the Empire and displaying the odds (as a percentage) that the Millennium Falcon reaches Endor in time and saves the galaxy.

**empire.json**
```json
{
  "countdown": 6, 
  "bounty_hunters": [
    {"planet": "Tatooine", "day": 4 },
    {"planet": "Dagobah", "day": 5 }
  ]
}
```

   - countdown (integer): number of days before the Death Star annihilates Endor
   - bounty_hunters (list): list of all locations where Bounty Hunter are scheduled to be present.
      - planet (string): Name of the planet. It cannot be null or empty.
      - day (integer): Day the bounty hunters are on the planet. 0 represents the first day of the mission, i.e. today.



# Limitations and Future evolutions

### Security
Here are the following security measures:
- user in backend is appuser and not root
- user in frontend container is nginx and not root
- backend allows requests only from `FRONTEND_URL` defined in the docker-compose

> TODO: before shipping to production, we should thoroughly review the measures.

### CLI
One limitation with CLI in production mode (meaning run with Docker/docker-compose) is that it can only access data files that are initially present in the container at build time.

Currently the files are the examples files from the repos in `./backend/examples`.

For example:
```sh
docker exec -it flask_backend_app give-me-odds backend/examples/example1/millennium-falcon.json backend/examples/example1/empire.json
>>>0
```

In order to allow to run the CLI on any file, we could bind a local volume to a container volume. In that case, we can point any file in that binded volume.

Here the new backend section of the docker-compose.yaml. Check the volume section to bind the local `./backend/examples` to a folder in the container in `/tmp/examples`.

```yaml
services:
  backend:
      build: 
        context: ./backend
        dockerfile: ./Dockerfile.backend
      environment:
        - ENV=production
      ports:
        - "5000:5000"
      restart: always
      container_name: flask_backend_app
      volumes:
        - ./backend/examples:/tmp/examples:ro
...
```
