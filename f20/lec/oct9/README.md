# Oct 9 Lecture

## 1. Requests vs. Selenium

### Watch: [18-minute video](https://youtu.be/o3Fp3OptT9s)

## 2. Selenium Example: Slow Table

### Watch: [24-minute video](https://youtu.be/9pRqLrbMl6M)

### Practice: Screenshot

In a notebook on your virtual machine, create a headless browser
instance:

```python
from IPython.core.display import Image

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

options = Options()
options.headless = True
b = webdriver.Chrome(options=options)
```

Navigate the browser to the URL of your favorite website, and save a screenshot:

```python
b.get("????")
b.save_screenshot("screenshot.png")
```

View the screenshot in the notebook:

```python
Image("screenshot.png")
```

## 3. Selenium Example: Load More

### Watch: [7-minute video](https://youtu.be/yzcQWjFjJhs)
