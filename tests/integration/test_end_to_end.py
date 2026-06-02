import os
import subprocess
import time

import httpx
import pytest


@pytest.mark.integration
def test_end_to_end_via_nginx():
    if os.getenv("RUN_INTEGRATION_TESTS", "false").lower() not in {"1", "true", "yes"}:
        pytest.skip("Integration tests are enabled with RUN_INTEGRATION_TESTS=true")

    subprocess.run(
        ["docker", "compose", "up", "-d", "--build", "db", "redis", "web", "nginx"],
        check=True,
    )
    try:
        url = "http://127.0.0.1"
        for _attempt in range(15):
            try:
                response = httpx.get(url, timeout=5.0)
                if response.status_code == 200:
                    break
            except Exception:
                pass
            time.sleep(2)
        else:
            pytest.fail("Service did not become available within expected time")

        response = httpx.get(url, timeout=5.0)
        assert response.status_code == 200
        assert response.json()["status"] == "Senior DevOps App is Running"
    finally:
        subprocess.run(["docker", "compose", "down"], check=True)
