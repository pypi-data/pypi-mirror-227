# chromedriver-autoinstaller-fix

This reposiory is created To fix "WARNING:root:Can not find chromedriver for currently installed chrome version." which has not been resolved in the orignal "python-chromedriver-autoinstaller-fix". 

Once, you use chromedriver-autoinstaller-fix you will not face error's if you are using versions > 115. 

## Installation

```bash
pip install chromedriver-autoinstaller-fix
```

## Usage
Just type `import chromedriver_autoinstaller_fix` in the module you want to use chromedriver.

## Example
```
from selenium import webdriver
import chromedriver_autoinstaller_fix


chromedriver_autoinstaller_fix.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
```

## Would appreciate a Star :)?