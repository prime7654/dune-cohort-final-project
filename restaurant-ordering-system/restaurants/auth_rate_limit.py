import hashlib

from django.core.cache import cache


AUTH_FAILURE_LIMIT = 5
AUTH_LOCKOUT_SECONDS = 300
AUTH_LOCKOUT_MESSAGE = "Too many failed sign-in attempts. Please try again in 5 minutes."


def _safe_cache_key(prefix, value):
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return f"auth-rate-limit:{prefix}:{digest}"


def _client_ip(request):
    if not request:
        return "unknown"

    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded_for:
        return forwarded_for.split(",", 1)[0].strip() or "unknown"

    return request.META.get("REMOTE_ADDR") or "unknown"


def _subjects(request, username):
    subjects = []
    if username:
        subjects.append(f"user:{username.strip().lower()}")
    subjects.append(f"ip:{_client_ip(request)}")
    return subjects


def is_auth_locked(request, username):
    return any(
        cache.get(_safe_cache_key("lock", subject))
        for subject in _subjects(request, username)
    )


def record_auth_failure(request, username):
    locked = False

    for subject in _subjects(request, username):
        attempts_key = _safe_cache_key("attempts", subject)
        attempts = int(cache.get(attempts_key, 0)) + 1
        cache.set(attempts_key, attempts, AUTH_LOCKOUT_SECONDS)

        if attempts >= AUTH_FAILURE_LIMIT:
            cache.set(
                _safe_cache_key("lock", subject),
                True,
                AUTH_LOCKOUT_SECONDS,
            )
            locked = True

    return locked


def clear_auth_failures(request, username):
    for subject in _subjects(request, username):
        cache.delete(_safe_cache_key("attempts", subject))
        cache.delete(_safe_cache_key("lock", subject))
