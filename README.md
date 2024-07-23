# Keycloak Fine Grained Authz User versus Service Account Benchmark

This repository contains a benchmark to test the performance of API requests using a normal user account token versus a service account token.

## Running the Benchmark

1. Make sure that you have `docker`, `docker-compose`, `python` and the Python `requests` module installed.
1. Start the Keycloak container using `docker compose up`. There will be two realms imported from [import](./import/).
    - **authz**: A realm with fine-grained authorization enabled for users and an `admin group` policy.
    - **no-authz**: A realm without fine-grained authorization enabled.
    - Both realms have an `admin` user account and a `demo` client with service account. Both have the `realm-admin` role from the `realm-management` client.
1. Run the benchmark via `python bench.py`. This will do the following per realm:
    1. If not already present, create 100 users.
    1. Query the users GET API several times with a **user** token obtained via `direct_grant`.
    1. Query the users GET API several times with a **service account** token obtained via `client_credentials` grant.

## Results

As a result of running the benchmark, you should see that without fine-grained authz or with a user token, the queries take around `7ms` to `10ms`.
With a service account and fine-grained authorization enabled, this takes **significantly** longer with delays in the `200ms` range.
