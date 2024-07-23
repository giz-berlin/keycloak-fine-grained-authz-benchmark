# Keycloak Fine Grained Authz User versus Service Account Benchmark

This repository contains a benchmark to test the performance of API requests using a normal user account token versus a service account token.

## Running the Benchmark

1. Make sure that you have `docker`, `docker-compose`, `python` and the Python `requests` module installed.
1. Start the Keycloak container using `docker compose up`. There will be two realms imported from [import](./import/).
    - **authz**: A realm with fine-grained authorization enabled for users and an `admin group` policy.
    - **no-authz**: A realm without fine-grained authorization enabled.
    - Both realms have an `admin` user (`view-users` and `manage-users`), a `viewer` user (only `view-users`) and a `demo` client with service account (`view-users`).
1. Run the benchmark via `python bench.py`. This will do the following per realm:
    1. If not already present, create 100 users.
    1. Query the users GET API several times with a **user** token obtained via `direct_grant` for both users.
    1. Query the users GET API several times with a **service account** token obtained via `client_credentials` grant.

Note: The first run of the benchmark will take a bit longer, subsequent runs will be faster. I don't know why exactly, but it might have something to do with caching the data from the database.

## Results

- Without fine-grained authorization, all requests are equally fast around `10ms`.
- With fine-grained authorization, request duration depends on the roles and type of user:
  - **service account** and `view-users`: takes quite long, around `200ms`
  - **user** and `view-users`: significantly faster than service account, around `15ms`
  - **user** and `manage-users`: even faster, around `10ms`.
