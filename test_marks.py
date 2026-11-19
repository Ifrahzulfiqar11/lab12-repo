import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By

# (input, expected result)
TESTS = [
    ("-1", "Rejected"),
    ("0", "Accepted"),
    ("5", "Accepted"),
    ("10", "Accepted"),
    ("11", "Rejected"),
]

page = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "index.html"
url = page.resolve().as_uri()

driver = webdriver.Chrome()
results = []

try:
    for value, expected in TESTS:
        driver.get(url)

        box = driver.find_element(By.ID, "mark")
        box.clear()
        box.send_keys(value)

        driver.find_element(By.TAG_NAME, "button").click()

        actual_text = driver.find_element(By.ID, "result").text

        actual = "Accepted" if actual_text.startswith("Accepted") else (
            "Rejected" if actual_text.startswith("Rejected") else actual_text
        )

        status = "PASS" if actual == expected else "FAIL"
        results.append((value, expected, actual_text, status))

finally:
    driver.quit()

print(f"\n{'Input':<8}{'Expected':<12}{'Actual':<40}{'Result'}")
print("-" * 68)

for value, expected, actual_text, status in results:
    print(f"{value:<8}{expected:<12}{actual_text:<40}{status}")

print(f"\n{sum(r[3] == 'PASS' for r in results)}/{len(results)} tests passed")
