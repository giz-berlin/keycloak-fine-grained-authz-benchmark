import requests
import time

USERNAME = "admin"
PASSWORD = "admin"
CLIENT_ID = "demo"
CLIENT_SECRET = "demo_secret"

AUTHZ_REALM = "authz"
NO_AUTHZ_REALM = "no-authz"

BASE_URL = "http://localhost:8080"

ITERATIONS = 10
SEED_USERS = 100

def millis(duration):
    return int(round(duration * 1000))

def prepare(realm):
    print("Preparing realm")
    with requests.Session() as s:
        auth_session_user(s, realm)

        r = s.get(f"{BASE_URL}/admin/realms/{realm}/users")
        r.raise_for_status()
        users = r.json()
        
        if len(users) >= SEED_USERS:
            print("Not seeding realm")
            return

        for i in range(SEED_USERS):
            name = f"user{i}"

            r = s.post(
                f"{BASE_URL}/admin/realms/{realm}/users",
                json={
                    "enabled": True,
                    "username": name,
                    "firstName": name,
                    "lastName": name,
                    "email": f"{name}@test.keycloak.org",
                    "emailVerified": True,
                },
            )
            r.raise_for_status()

def get_users(s, realm):
    now = time.time()
    
    r = s.get(f"{BASE_URL}/admin/realms/{realm}/users")
    r.raise_for_status()
    
    duration = time.time() - now
    
    return duration

def auth_session_user(s, realm):
    r = s.post(
        f"{BASE_URL}/realms/{realm}/protocol/openid-connect/token",
        data={
            "username": USERNAME,
            "password": PASSWORD,
            "grant_type": "password",
            "client_id": "admin-cli",
        },
    )
    r.raise_for_status()
    access_token = r.json()["access_token"]
    s.headers.update({"Authorization": f"Bearer {access_token}"})

def auth_session_client(s, realm):
    r = s.post(
        f"{BASE_URL}/realms/{realm}/protocol/openid-connect/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials",
        },
    )
    r.raise_for_status()
    access_token = r.json()["access_token"]
    s.headers.update({"Authorization": f"Bearer {access_token}"})

def test_user(realm):
    with requests.Session() as s:
        auth_session_user(s, realm)

        print(f"User on realm {realm}")
        for i in range(ITERATIONS):
            duration = get_users(s, realm)
            print(millis(duration))

def test_client(realm):
    with requests.Session() as s:
        auth_session_client(s, realm)

        print(f"Service account on realm {realm}")
        for i in range(ITERATIONS):
            duration = get_users(s, realm)
            print(millis(duration))

def main():
    for realm in [AUTHZ_REALM, NO_AUTHZ_REALM]:
        prepare(realm)

        test_user(realm)
        test_client(realm)

if __name__ == "__main__":
    main()
