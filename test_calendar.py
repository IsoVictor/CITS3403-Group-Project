from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_calendar():
    # Set up the web driver (e.g., Chrome)
    driver = webdriver.Chrome()

    try:
        # Navigate to the calendar page
        driver.get("http://localhost:5000/calendar")

        # Wait for the calendar to be visible
        calendar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "calendar"))
        )

        # Get all the events on the calendar
        events = driver.find_elements(By.CSS_SELECTOR, ".fc-event-title")

        # Check if the events are displayed
        assert len(events) > 0, "No events found on the calendar"

        # Hover over the first event
        first_event = events[0]
        webdriver.ActionChains(driver).move_to_element(first_event).perform()

        # Wait for the tooltip to be visible
        tooltip = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".tooltip"))
        )

        # Check if the tooltip contains the expected information
        tooltip_text = tooltip.text
        assert "Date" in tooltip_text, "Date not found in the tooltip"
        assert "Location" in tooltip_text, "Location not found in the tooltip"
        assert "Time" in tooltip_text, "Time not found in the tooltip"

        # Click on a date to redirect to the study groups page
        date_cell = driver.find_element(By.CSS_SELECTOR, ".fc-daygrid-day")
        date_cell.click()

        # Wait for the page to load and check if the URL contains "/study-groups"
        WebDriverWait(driver, 5).until(EC.url_contains("/study-groups"))
        assert "/study-groups" in driver.current_url, "Not redirected to the study groups page"

        print("Calendar test passed!")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    test_calendar()