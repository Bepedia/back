

def get_user(headers):
    return headers.get("X-Goog-Authenticated-User-Email", "test@test.com")
