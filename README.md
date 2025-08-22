# 🧪 Playwright Pytest Automation

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)  
![Playwright](https://img.shields.io/badge/Playwright-Testing-brightgreen.svg)  
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

Automation test framework using **Python, Playwright, and Pytest**.  
This project follows the **Page Object Model (POM)** pattern for maintainability and scalability.
Please see final section for ⚠️ Notes and Limitations
---

## 📂 Project Structure

```
.
├── pages/                  # Page Objects (BasePage + sections)
│   ├── base_page.py
│   ├── repo_page.py
│   ├── shop_page.py
│   └── sections/
│       ├── product_section.py
│       └── cart_section.py
│       └── work_abroad_section.py
├── tests/                  # Test cases
│   ├── sample_test.py
│   └── conftest.py
├── config/                 # Config & logging
│   ├── logging.ini
│   └── pytest.ini
├── fixtures/               # network logger and browser setup/teardown fixtures
│   ├── browser.py
│   └── network.py
├── utils/                  #centralized logging and wait time configurations/utilities
│   ├── logger.py
│   └── wait.py
├── requirements.txt        # Dependencies
├── README.md               # This file
└── venv/                   # Virtual environment (excluded from git)
```

---

## 🚀 Getting Started

  ### 1. Clone the Repository

  ```bash
  git clone https://github.com/gideongl/nuclera_exercise.git
  cd your-repo
  ```

### 2. Install Python and Create and Activate a Virtual Environment
  
  Install Python (Windows):
  ```bash
    sudo apt update
    sudo apt install python3 python3-pip -y
  ```
  Install Python (macOS / Linux):  
  ```bash
      brew update
      brew install python
      python3 --version
      pip3 --version
  ```
  Otherwise, it’s recommended to download Python from python.org
  and check Add Python to PATH during installation
  
  Create venv:
  ```bash
  python -m venv venv
  ```

  Activate it:

  - **Windows (PowerShell)**  
    ```bash
    venv\Scripts\Activate.ps1
    ```
  - **Windows (Command Prompt)**  
    ```bash
    venv\Scripts\Activate
    ```
  - **macOS / Linux**  
    ```bash
    source venv/bin/activate
    ```

### 3. Install Dependencies
  Navigate to Project Root Directory
  ```bash
  python -m pip install --upgrade pip
  python -m pip install pytest-playwright
  python -m pip install -r requirements.txt
  python -m playwright install
  ```

### 4. Run Tests

  Run all tests and generate an HTML report:

  ```bash

	pytest --html=reports/test_report.html --self-contained-html
  ```

  Run in headed mode:

  ```bash
  pytest --html=reports/test_report.html --self-contained-html --headed
  ```

  Run a specific test:

  ```bash
  pytest tests/sample_test.py::test_cart_section --html=reports/test_report.html --self-contained-html
  ```

  ---


## 🏗️ Framework Features

  - ✅ **Playwright** for fast, reliable browser automation  
  - ✅ **Pytest** for flexible test execution & reporting  
  - ✅ **Page Object Model (POM)** for maintainability  
  - ✅ Configurable logging (`logging.ini`)  
  - ✅ Works on Windows, macOS, Linux  

  ---

## 📖 Example Test

  ```python
  @pytest.mark.ui
  def test_product_list_section(page):
      shopping_page = ShoppingPage(page)
      shopping_page.go_to_page("https://automated-test-evaluation.web.app/")

      section = shopping_page.product_list_section
      expect(section.section_root).to_be_visible()
      expect(section.add_to_cart_button(0)).to_be_visible()
  ```

  ---

## ⚙️ Configuration

  - `pytest.ini` → Pytest config (markers, options, test paths)  
  - `logging.ini` → Logging setup  
  - `requirements.txt` → Python dependencies  

  ---

## 🤝 Contributing

  Pull requests are welcome!  
  For major changes, please open an issue first to discuss what you’d like to change.

  ---

## 📜 License

This project is licensed under the MIT License.  
See [LICENSE](LICENSE) for details.


## ⚠️ Notes & Limitations

- **Browser Context**
  - Tests are designed to run in Chromium by default.
  - Running in Firefox or WebKit may require minor adjustments.
  - The test suite currently assumes a desktop viewport; responsive/mobile layouts are not covered.


- **Test Environment**
  - Tests assume a stable network connection.
  - Intermittent network issues may cause timeouts or failures.

- **Data Handling**
  - Tests currently work with the pre-populated test environment.
  - Dynamic content or frequently updated product lists may require updating selectors.

- **Selectors**
  - Many locators are based on CSS classes generated dynamically.
  - Changes in the front-end styling or DOM structure can break tests.

- **Headless vs Headed**
  - Some visual tests (e.g., hover actions) are more reliable in headed mode.
  - Headless mode may not render certain UI elements exactly as in a real browser.

- **Authentication & Access**
  - The repository assumes public pages; private content or authentication flows are not tested.
  - GitHub repo tests assume the repository is public and accessible without login.

- **Reporting**
  - Test artifacts (screenshots, videos, network logs) are saved in the `artifacts/` directory.
  - Screenshots, networklogs and Video are only generated for failing tests
  - Video feature is currently broken while I prioritise test coverage
  - Ensure sufficient disk space when running multiple tests.
