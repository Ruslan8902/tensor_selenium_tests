import os


def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")

    return driver.execute_script("""
        return document.querySelector('downloads-manager')
        .shadowRoot.querySelector('#downloadsList')
        .items.filter(e => e.state === 2)
        .map(e => e.filePath || e.file_path || e.fileUrl || e.file_url);
        """)


def convert_bytes_to_mb(bytes):
    return bytes / (1024 * 1024)


def get_file_size_in_mb(path):
    return convert_bytes_to_mb(os.path.getsize(path))
