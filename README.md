# Whisk Prompt Automation

An automated tool for submitting prompts to Google's Whisk image generation platform using Selenium WebDriver.

## Features

- Automated prompt submission to Google Whisk
- Handles browser automation using Microsoft Edge WebDriver
- Supports batch processing of prompts from a text file
- Includes error handling and screenshot capture
- Maintains browser session for manual login

## Prerequisites

- Python 3.x
- Selenium WebDriver
- Microsoft Edge browser
- Microsoft Edge WebDriver
- A text file containing prompts (one per line)

## Setup

1. Install required Python packages:
```bash
pip install selenium
```

2. Update the configuration section in the script with your paths:
```python
DRIVER_PATH = "path/to/msedgedriver.exe"
PROMPTS_FILE = "path/to/prompts.txt"
EDGE_PROFILE = "path/to/edge/profile"
PROFILE_DIR = "Default"
```

3. Ensure your prompts.txt file is properly formatted with one prompt per line

## Usage

Run the script using Python:
```bash
python whisk_script.py
```

The script will:
1. Open Microsoft Edge browser
2. Navigate to Google Whisk
3. Wait for manual login
4. Process prompts automatically
5. Save screenshots if errors occur

## Error Handling

- Screenshots are saved on errors or timeouts
- Continues processing remaining prompts if one fails
- Detailed console output for monitoring progress

## License

MIT License

## Author

AbuKhuzaima
