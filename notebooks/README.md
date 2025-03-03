# parse-records

### How to run
Run all notebooks in numerical order.
Scripts contain helpful functions or classes for data processing.

### Dependency management

Project's dependencies are managed by the [poetry](https://python-poetry.org/).
Moving to poetry has helped to have `pyproject.toml` as a single configuration file for the project as well.


#### [!] Poetry.lock file

To minimize the time of building images it is important to always have an up-to-date `poetry.lock` file in the repository.
In case a new dependency was added to `pyproject.toml` the command below should be run and the updated `poetry.lock` committed to the repo.

```shell
poetry lock --no-update
```

### Usage

#### To run service locally

0. Recommended step. Set virtualenvs inside project's repo and skip step 1.
```shell
poetry config virtualenvs.in-project true
```

1. Create a virtual env (optional)

```shell
python -m venv /pass/to/venv_name
source /tmp/test_env_name/bin/activate
```

2. Install dependencies from `pyproject.toml`

```shell
poetry install --no-root
```

3. Define env variables in `.env`

4. Run the script (this will run the process from beginning to end)

```shell
python src/run.py
```
