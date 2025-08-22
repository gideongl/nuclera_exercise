# conftest.py
import json
import logging
import logging.config
from pathlib import Path
import os
import pytest
from pytest_html import extras
from fixtures.network import network_logger

# -----------------------------
# Determine repo root and config paths
# -----------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent  # tests/ -> repo root
LOGGING_CONFIG_PATH = REPO_ROOT / "config" / "logging.ini"

# -----------------------------
# Artifact directories
# -----------------------------
ARTIFACTS_DIR = REPO_ROOT / "artifacts"
SCREENSHOT_DIR = ARTIFACTS_DIR / "screenshots"
VIDEO_DIR = ARTIFACTS_DIR / "videos"
NETWORK_LOGGER_DIR = ARTIFACTS_DIR / "network_logs"

# Create directories if they do not exist
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)
NETWORK_LOGGER_DIR.mkdir(parents=True, exist_ok=True)

# Load centralized logging.ini
logging.config.fileConfig(LOGGING_CONFIG_PATH, disable_existing_loggers=False)

# Module-level logger for hooks and fixtures
logger = logging.getLogger("pytest_playwright")


# --- Helper to read last N lines from log ---
def _read_log_file_tail(lines: int = 50) -> str:
    log_file = ARTIFACTS_DIR / "test.log"
    if not log_file.exists():
        return ""
    with log_file.open("r", encoding="utf-8") as f:
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
            screenshot_path = SCREENSHOT_DIR / f"{item.nodeid.replace('/', '_').replace(':', '_')}.png"
            try:
                page.screenshot(path=str(screenshot_path), full_page=True)
                extra.append(extras.image(str(screenshot_path), name="Failure Screenshot"))
            except Exception as e:
                logger.warning(f"Could not capture screenshot: {e}")

        # Video
        if report.failed and "context" in item.funcargs:
            context = item.funcargs["context"]
            try:
                for p in context.pages:
                    if p.video:
                        video_path = Path(p.video.path())
                        if video_path.exists():
                            new_path = VIDEO_DIR / f"{item.nodeid.replace('/', '_').replace(':', '_')}.webm"
                            video_path.rename(new_path)
                            extra.append(extras.video(str(new_path), name="Failure Video"))
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
