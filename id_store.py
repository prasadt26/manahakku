"""Durable news-ID counter backed by a private GitHub Gist.

Streamlit Cloud containers have an ephemeral filesystem: the container is
rebuilt from a fresh `git clone` on every reboot (nightly maintenance, wake
from sleep, redeploy, any push), so a counter written to local disk is lost
and snaps back to whatever the repo happens to contain. The counter therefore
lives in a gist, which survives independently of the app.

Secrets required (Streamlit Cloud -> your app -> Settings -> Secrets):

    [github]
    token = "github_pat_..."          # PAT with gist read/write
    gist_id = "a1b2c3d4..."           # the id from the gist's URL
    filename = "poster_last_id.json"  # optional; this is the default

The gist file must already contain JSON of the form {"last_id": 931}. A
missing or malformed file is treated as an error rather than silently seeded,
so the app can never invent a counter and hand out an ID you already used.
"""

import json

import requests
import streamlit as st

API = "https://api.github.com"
DEFAULT_FILENAME = "poster_last_id.json"
TIMEOUT = 10


class IdStoreError(RuntimeError):
    """The durable counter could not be read or written."""


def _config():
    """Return (token, gist_id, filename) from Streamlit secrets."""
    try:
        cfg = st.secrets["github"]
    except Exception as exc:
        # Streamlit raises different types here depending on version and on
        # whether a secrets file exists at all, so catch broadly.
        raise IdStoreError(
            "No [github] section found in Streamlit secrets. Add `token` and "
            "`gist_id` under App -> Settings -> Secrets."
        ) from exc

    token = cfg.get("token")
    gist_id = cfg.get("gist_id")
    missing = [name for name, value in (("token", token), ("gist_id", gist_id)) if not value]
    if missing:
        raise IdStoreError(
            f"Missing {' and '.join(missing)} in the [github] secrets section."
        )
    return token, gist_id, cfg.get("filename", DEFAULT_FILENAME)


def _headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


@st.cache_data(ttl=30, show_spinner=False)
def _fetch_last_id():
    """Read the counter from the gist. Cached briefly to spare the API on reruns.

    Streamlit reruns the whole script on every widget interaction, so an
    uncached read would hit GitHub on each radio-button click. Exceptions are
    never cached, so a transient failure retries on the next rerun.
    """
    token, gist_id, filename = _config()
    try:
        response = requests.get(
            f"{API}/gists/{gist_id}", headers=_headers(token), timeout=TIMEOUT
        )
    except requests.RequestException as exc:
        raise IdStoreError(f"Could not reach the GitHub API: {exc}") from exc

    if response.status_code == 401:
        raise IdStoreError(
            "GitHub rejected the token (401). It may be expired, or it may lack "
            "the Gists permission."
        )
    if response.status_code == 404:
        raise IdStoreError(
            f"Gist {gist_id} was not found (404). Check `gist_id`, and that this "
            "token belongs to the account that owns the gist."
        )
    if not response.ok:
        raise IdStoreError(
            f"GitHub API returned {response.status_code}: {response.text[:200]}"
        )

    files = response.json().get("files") or {}
    if filename not in files:
        present = ", ".join(files) or "none"
        raise IdStoreError(
            f"The gist has no file named {filename!r}. Files present: {present}."
        )

    raw = files[filename].get("content") or ""
    try:
        value = json.loads(raw)["last_id"]
    except (ValueError, KeyError, TypeError) as exc:
        raise IdStoreError(
            f'{filename} must contain JSON like {{"last_id": 931}}. '
            f"Found: {raw[:100]!r}"
        ) from exc

    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise IdStoreError(f'"last_id" must be a non-negative integer, found {value!r}.')
    return value


def read_last_id():
    """Return the last locked news ID. Raises IdStoreError if unavailable."""
    return _fetch_last_id()


def write_last_id(value):
    """Overwrite the counter in the gist. Raises IdStoreError on failure."""
    token, gist_id, filename = _config()
    body = {"files": {filename: {"content": json.dumps({"last_id": value})}}}
    try:
        response = requests.patch(
            f"{API}/gists/{gist_id}",
            headers=_headers(token),
            json=body,
            timeout=TIMEOUT,
        )
    except requests.RequestException as exc:
        raise IdStoreError(f"Could not reach the GitHub API: {exc}") from exc

    if response.status_code in (401, 403):
        raise IdStoreError(
            f"GitHub refused the write ({response.status_code}). The token needs "
            "Gists set to Read and write."
        )
    if not response.ok:
        raise IdStoreError(
            f"GitHub API returned {response.status_code}: {response.text[:200]}"
        )

    _fetch_last_id.clear()


def claim_next_id():
    """Bump the counter by one and return the newly locked ID.

    Re-reads past the cache first, so a value bumped from another browser tab
    in the last 30 seconds is not handed out twice. This is not atomic -- the
    gist API offers no compare-and-swap -- so two simultaneous clicks could
    still collide. In practice, lock IDs from one tab at a time.
    """
    _fetch_last_id.clear()
    new_id = _fetch_last_id() + 1
    write_last_id(new_id)
    return new_id
