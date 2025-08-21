import pytest
import json

@pytest.fixture
def network_logger(page):
    requests = []

    def log_request(request):
        requests.append({"url": request.url, "method": request.method})

    page.on("request", log_request)
    yield requests

    with open("artifacts/network_logs/network_logs.json", "w") as f:
        json.dump(requests, f, indent=2)
