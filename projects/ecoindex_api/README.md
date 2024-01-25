# Ecoindex-Api

This tool provides an easy way to analyze websites with [Ecoindex](https://www.ecoindex.fr) on a remote server. You have the ability to:

- Make a page analysis
- Define screen resolution
- Save results to a DB
- Retrieve results
- Limit the number of request per day for a given host
- Get screenshots of the analyzed page

This API is built on top of [ecoindex-scraper](https://pypi.org/project/ecoindex-scraper/) with [FastAPI](https://fastapi.tiangolo.com/) and [Celery](https://docs.celeryq.dev/)

## OpenAPI specification

The API specification can be found in the [documentation](projects/ecoindex_api/openapi.json). You can also access it with [Redoc](https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/cnumr/ecoindex_python_fullstack/main/projects/ecoindex_api/openapi.json).

## Requirements

- [Docker](https://www.docker.com/)
- [Docker-compose v2](https://docs.docker.com/compose/compose-v2/)

## Installation

With this docker setup you get 6 services running that are enough to make it all work:

- `db`: A MySQL instance
- `api`: The API instance running FastAPI application
- `worker`: The celery task worker that runs ecoindex analysis
- `redis` (optional): The [redis](https://redis.io/) instance that is used by the Celery worker
- `flower` (optional): The Celery [monitoring interface](https://flower.readthedocs.io/en/latest/)

### First start

```bash
cp docker-compose.yml.template docker-compose.yml && \
docker  compose up -d
```

Every services should start normaly, then you can go to:

- [http://localhost:8001/docs](http://localhost:8001/docs) to access to the swagger of the API
- [http://localhost:5555](http://localhost:5555) to access the flower interface (Celery task queue UI. Basic auth is `ecoindex:ecoindex`)

## Configuration

Here are the environment variables you can configure in your `.env` file:

| Service             | Variable Name              | Default value                      | Description                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------------- | -------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| API, Worker         | `DEBUG`                    | `False`                            | If you want to run the server in debug mode, you can set this variable to `True`                                                                                                                                                                                                                                                                                                                                           |
| API                 | `WAIT_BEFORE_SCROLL`       | 3                                  | You can configure the wait time of the scenario when a page is loaded before it scrolls down to the bottom of the page                                                                                                                                                                                                                                                                                                     |
| API                 | `WAIT_AFTER_SCROLL`        | 3                                  | You can configure the wait time of the scenario when a page is loaded after having scrolled down to the bottom of the page                                                                                                                                                                                                                                                                                                 |
| API                 | `CORS_ALLOWED_CREDENTIALS` | `True`                             | See [MDN web doc](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Credentials)                                                                                                                                                                                                                                                                                                              |
| API                 | `CORS_ALLOWED_HEADERS`     | `*`                                | See [MDN web doc](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Headers)                                                                                                                                                                                                                                                                                                                  |
| API                 | `CORS_ALLOWED_METHODS`     | `*`                                | See [MDN web doc](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Methods)                                                                                                                                                                                                                                                                                                                  |
| API                 | `CORS_ALLOWED_ORIGINS`     | `*`                                | See [MDN web doc](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin)                                                                                                                                                                                                                                                                                                                   |
| API                 | `EXCLUDED_HOSTS`           | `["localhost", "127.0.0.1"]`       | You can configure a list of hosts that will be excluded from the analysis.                                                                                                                                                                                                                                                                                                                                                 |
| API, Worker         | `DAILY_LIMIT_PER_HOST`     | 0                                  | When this variable is set, it won't be possible for a same host to make more request than defined in the same day to avoid overload. If the variable is set, you will get a header `x-remaining-daily-requests: 6` in your response. It is used for the POST methods. If you reach your authorized request quota for the day, the next requests will give you a 429 response. If the variable is set to 0, no limit is set |
| API, Worker         | `DATABASE_URL`             | `sqlite+aiosqlite:///./sql_app.db` | If you run your mysql instance on a dedicated server, you can configure it with your credentials. By default, it uses an sqlite database when running in local                                                                                                                                                                                                                                                             |  |
| API, Worker, Flower | `REDIS_CACHE_HOST`         | `localhost`                        | The hostname of the redis backend used by Celery but also API to cache results                                                                                                                                                                                                                                                                                                                                             |
| API, Worker         | `TZ`                       | `Europe/Paris`                     | The timezone used by the API and the worker.                                                                                                                                                                                                                                                                                                                                                                               |
| Worker              | `ENABLE_SCREENSHOT`        | `False`                            | If screenshots are enabled, when analyzing the page the image will be generated in the `./screenshot` directory with the image name corresponding to the analysis ID and will be available on the path `/{version}/ecoindexes/{id}/screenshot`                                                                                                                                                                             |
| Worker              | `SCREENSHOT_GID`           | None                               | The group used to create the screenshot. If not set, the group of the current user will be used.                                                                                                                                                                                                                                                                                                                           |
| Worker              | `SCREENSHOT_UID`           | None                               | The user used to create the screenshot. If not set, the current user will be used.                                                                                                                                                                                                                                                                                                                                         |
| Flower              | `FLOWER_BASIC_AUTH`        | `ecoindex:ecoindex`                | The basic auth used to access the flower interface                                                                                                                                                                                                                                                                                                                                                                         |

## Local development with [task](https://taskfile.dev)

Task is a task runner and build tool. You can install it with the following command:

```bash
curl -sL https://taskfile.dev/install.sh | sh
```

Then you can run the server in debug mode with the following command:

```bash
task start-dev
```

## Testing

We use Pytest to run unit tests for this project. The test suite are in the `tests` folder. Just execute :

```Bash
task tests

# or

task tests-coverage
```

> This runs pytest and also generate a [coverage report](https://pytest-cov.readthedocs.io/en/latest/) (terminal and html)
