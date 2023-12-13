from playwright.sync_api import sync_playwright

def extract_website_content(domain):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"http://{domain}")
        content = page.content()
        browser.close()
        return content, domain
