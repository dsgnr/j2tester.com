<h1 align="center">j2tester.com</h1>

Inspired by [sivel/ansible-template-ui](https://github.com/sivel/ansible-template-ui), this repository creates a simple web UI and REST API for testing, parsing and rendering Ansible or Jinja2 templates.

Offers minimal requirements, without spinning up containers and executing Ansible.

Supports all [built-in Jinja2 filters](https://jinja.palletsprojects.com/en/stable/templates/#builtin-filters) as well as the aditional [Ansible built-in filters](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_filters.html).

## Table of contents:

- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Development](#development)
  - [Standalone](#standalone)
  - [Docker](#docker)
- [Production](#production)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)

## Getting Started

The project consists of two containers. The front-end is a static HTML file sat behind Nginx. The back-end is a simple API built using [Litestar](https://litestar.dev/).

The project aims to be super simple, with low overhead and also the least amount of dependencies as possible.

The project contains both production and development stacks. The production stack utilises `gunicorn` as the API's process manager with `uvicorn` workers. Development utilises `uvicorn` with the `--reload` parameter.

## Documentation

API routes and specification can be found at [j2tester.com/docs](https://j2tester.com/docs)

## Development

### Standalone

#### Web

> [!NOTE]
> Uses [Node](https://nodejs.org/) version 23 and newer. Requires [Yarn](https://classic.yarnpkg.com/en/)

Bringing up the UI outside of Docker;

```
$ cd frontend/web
$ yarn install
$ yarn dev
```

`j2tester.com` front-end will be running at [http://0.0.0.0:8080](http://0.0.0.0:8080).

#### API

> [!NOTE]
> Uses Python 3.12. The Python environment uses [Poetry](https://pypi.org/project/poetry/) for package management. This must be installed.

```
$ cd backend/api
$ poetry install
$ uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

`j2tester.com` API will be running at [http://0.0.0.0:8000](http://0.0.0.0:8000).

### Docker

```
$ docker-compose -f docker-compose-dev.yml up --build
```

j2tester.com front-end will be running at [http://0.0.0.0:8080](http://0.0.0.0:8080) and the API will be running at [http://0.0.0.0:8000](http://0.0.0.0:8000).

## Production

### Docker

> [!NOTE]
> Uses [ghcr.io/dsgnr/j2testerio-web:latest](https://github.com/dsgnr/j2tester.com/pkgs/container/j2testerio-web) and [ghcr.io/dsgnr/j2testerio-api:latest](https://github.com/dsgnr/j2tester.com/pkgs/container/j2testerio-api).

```
$ docker-compose up
```

`j2tester.com` front-end will be running at [http://0.0.0.0:8080](http://0.0.0.0:8080) and the API will be running at [http://0.0.0.0:8000](http://0.0.0.0:8000).

## Environment Variables

The following configuration options are available. These would be set within the Docker compose files, or in your environment if you're using j2tester standalone.

### Web

| Name             | Required? | Default         | Notes                                                                                    |
| ---------------- | --------- | --------------- | ---------------------------------------------------------------------------------------- |
| API_URL          | No        | http://api:8000 | The URL of the API service if changed from the default. The scheme and port is required. |

## Monitoring

A Prometheus `/metrics` endpoint is available for capturing metrics about the API endpoints, their response times and status codes. Since some endpoints have a hostname and variables provided via the path, these are grouped to anonymise them.

Add your instance to your Prometheus config using the following config (be sure to update the scrape target to suit your needs):
~~~ yaml
- job_name: 'j2tester'
  static_configs:
  - targets:
    - 'https://j2tester.com'
~~~

## Contributing

I'm thrilled that you’re interested in contributing to this project! Here’s how you can get involved:

### How to Contribute

1. **Submit Issues**:

   - If you encounter any bugs or have suggestions for improvements, please submit an issue on our [GitHub Issues](https://github.com/dsgnr/j2tester.com/issues) page.
   - Provide as much detail as possible, including steps to reproduce and screenshots if applicable.

2. **Propose Features**:

   - Have a great idea for a new feature? Open a feature request issue in the same [GitHub Issues](https://github.com/dsgnr/j2tester.com/issues) page.
   - Describe the feature in detail and explain how it will benefit the project.

3. **Submit Pull Requests**:
   - Fork the repository and create a new branch for your changes.
   - Make your modifications and test thoroughly.
   - Open a pull request against the `devel` branch of the original repository. Include a clear description of your changes and any relevant context.

## Author

- Website: https://danielhand.io
- Github: [@dsgnr](https://github.com/dsgnr)

## Show your support

Give a ⭐️ if this project helped you!

Running websites such as this comes with associated costs. Any donations to help the running of the site is hugely appreciated!

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/U7U3FUX17)

## License

See the [LICENSE](LICENSE) file for more details on terms and conditions.
