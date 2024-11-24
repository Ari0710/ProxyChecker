# Proxy Checker GUI Tool

A simple and user-friendly GUI-based tool to test the validity of proxy servers. Paste your proxies, check which ones are working, and easily copy the results for further use.

---

## Features
- **Paste Proxies**: Input a list of proxies directly into the tool.
- **Check Proxies**: Tests the provided proxies against a reliable server (`1.1.1.1`) to determine their availability.
- **Results Display**: Displays working proxies side by side with the original list.
- **Real-Time Updates**: Shows the progress percentage and counts of working vs. total proxies.
- **Copy to Clipboard**: One-click button to copy all working proxies.
- **Standalone Executable**: Can be run as an `.exe` file without requiring Python.

---

## Requirements
If you're running the script version, you'll need:
- Python 3.7 or higher
- The following Python libraries:
  ```bash
  pip install tkinter requests
  ```

---

## How to Use
### For the Python Script
1. Run the script:
   ```bash
   python proxycheck.py
   ```
2. Paste proxies into the **Pasted Proxies** section.
3. Click the **Check Proxies** button.
4. View the results in the **Working Proxies** section.
5. Use the **Copy Working Proxies** button to copy the working proxies to your clipboard.

### For the Executable File
1. Double-click the `proxy_checker.exe` file.
2. Follow the same steps as above.

---

## Creating an Executable File
If you need to generate an `.exe` from the Python script, follow these steps:
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Generate the executable:
   ```bash
   pyinstaller --onefile --noconsole proxy_checker.py
   ```
3. Locate the executable in the `dist` folder.

---

## Example Input
```text
44.218.183.55:80
204.236.137.68:80
13.56.192.187:80
91.92.155.207:3128
```

---

## Output
The **Working Proxies** section will display something like:
```text
44.218.183.55:80
13.56.192.187:80
```

---

## Contributing
Feel free to open an issue or create a pull request if you have suggestions for improving the tool.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---
