"""
Browser Controller for MARK 12
Automates browser actions, searches, and web navigation.
"""
import webbrowser
import urllib.parse
from typing import Dict, Any
from database.repository import Repository

class BrowserController:
    def open_url(self, url: str) -> Dict[str, Any]:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        try:
            webbrowser.open(url)
            Repository.log_automation("open_url", url, "SUCCESS")
            return {"success": True, "message": f"Opened {url} in default browser."}
        except Exception as e:
            Repository.log_automation("open_url", url, "FAILED", str(e))
            return {"success": False, "message": f"Failed to open {url}: {str(e)}"}

    def search_web(self, query: str, engine: str = "google") -> Dict[str, Any]:
        encoded = urllib.parse.quote(query)
        if engine.lower() == "youtube":
            url = f"https://www.youtube.com/results?search_query={encoded}"
        elif engine.lower() == "github":
            url = f"https://github.com/search?q={encoded}"
        else:
            url = f"https://www.google.com/search?q={encoded}"

        return self.open_url(url)

global_browser_controller = BrowserController()
