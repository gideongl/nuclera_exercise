# conftest.py
import os
import json
import logging
import logging.config
import pytest
from pytest_html import extras
from fixtures.network import network_logger


# -----------------------------
# Load centralized logging.ini
# -----------------------------
logging_config_path = os.path.join(os.path.dirname(__file__), "config/logging.ini")
logging.config.fileConfig(logging_config_path, disable_existing_loggers=False)

# Create a module-level logger for hooks and fixtures
logger = logging.getLogger("pytest_playwright")

# -----------------------------
# Artifact directories
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
SCREENSHOT_DIR = os.path.join(ARTIFACTS_DIR, "screenshots")
VIDEO_DIR = os.path.join(ARTIFACTS_DIR, "videos")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)


# --- Helper to read last N lines from log ---
def _read_log_file_tail(lines: int = 50) -> str:
    log_file = os.path.join(ARTIFACTS_DIR, "test.log")
    if not os.path.exists(log_file):
        return ""
    with open(log_file, "r", encoding="utf-8") as f:
        return "".join(f.readlines()[-lines:])

# --- Pytest hook to attach logs/screenshots/videos/network ---
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call":
        # Attach log tail
        log_text = _read_log_file_tail()
        if log_text:
            extra.append(extras.text(log_text, name="Test Logs"))

        # Screenshot
        if report.failed and "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot_path = os.path.join(
                SCREENSHOT_DIR,
                f"{item.nodeid.replace('/', '_').replace(':', '_')}.png",
            )
            try:
                page.screenshot(path=screenshot_path, full_page=True)
                extra.append(extras.image(screenshot_path, name="Failure Screenshot"))
            except Exception as e:
                logger.warning(f"Could not capture screenshot: {e}")

        # Video
        if report.failed and "context" in item.funcargs:
            context = item.funcargs["context"]
            try:
                for p in context.pages:
                    if p.video:
                        video_path = p.video.path()
                        if os.path.exists(video_path):
                            new_path = os.path.join(
                                VIDEO_DIR,
                                f"{item.nodeid.replace('/', '_').replace(':', '_')}.webm",
                            )
                            os.rename(video_path, new_path)
                            extra.append(extras.video(new_path, name="Failure Video"))
                            break
            except Exception as e:
                logger.warning(f"Could not attach video: {e}")

        # Network logs
        if "network_logger" in item.funcargs:
            requests = item.funcargs["network_logger"]
            if requests:
                try:
                    network_dump = json.dumps(requests, indent=2)
                    extra.append(extras.text(network_dump, name="Network Logs"))
                except Exception as e:
                    logger.warning(f"Could not attach network logs: {e}")

    report.extra = extra