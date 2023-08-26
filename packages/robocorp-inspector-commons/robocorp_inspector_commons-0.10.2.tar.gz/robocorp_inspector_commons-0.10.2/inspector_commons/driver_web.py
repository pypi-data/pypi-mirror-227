import base64
import logging
import os
import shutil
import time
import traceback
from pathlib import Path, WindowsPath
from typing import Any, Dict, Optional, Union
from urllib.parse import urlparse

from retry import retry
from RPA.core import webdriver  # type: ignore
from selenium import webdriver as selenium_webdriver
from selenium.common.exceptions import (  # type: ignore
    InvalidSessionIdException,
    JavascriptException,
    NoSuchWindowException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver import ActionChains, ChromeOptions, Remote  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore

from inspector_commons.utils import force_kill_process  # type: ignore

SERVICES = {
    "chrome": selenium_webdriver.chrome.service.Service,
    "firefox": selenium_webdriver.firefox.service.Service,
    "edge": selenium_webdriver.edge.service.Service,
    "chromiumedge": selenium_webdriver.edge.service.Service,
    "safari": selenium_webdriver.safari.service.Service,
    "ie": selenium_webdriver.ie.service.Service,
}


class WebDriverExceptions(Exception):
    def __init__(
        self,
        msg: Optional[str] = None,
        errors: Optional[Dict[str, WebDriverException]] = None,
    ):
        super().__init__()
        self.msg = msg or ""
        self.errors = errors or {}

    def __str__(self) -> str:
        return f"{self.msg}" + ", ".join(self.errors.keys())


def load_resource(filename):
    path = Path(__file__).parent / "static" / "resources" / str(filename)
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def chrome_options():
    opts = ChromeOptions()

    preferences = {
        "safebrowsing.enabled": True,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    }

    opts.add_argument("--no-sandbox")
    opts.add_argument("--allow-running-insecure-content")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-web-security")
    opts.add_experimental_option("prefs", preferences)
    opts.add_experimental_option(
        "excludeSwitches", ["enable-logging", "enable-automation"]
    )

    return opts


def friendly_name(element):
    tag = element.tag_name.lower()

    if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "a"):
        return element.text

    if tag == "img":
        alt = element.get_attribute("alt")
        if alt.strip():
            return alt

        url = element.get_attribute("src")
        name = os.path.basename(urlparse(url).path)
        if not url.startswith("data:image") and name.strip():
            return name

        return "Image"

    # TODO: Add div logic
    # TODO: Add input type and title logic

    # Human-friendly names for non-descriptive tags,
    # expand as necessary
    names = {
        # Navigation
        "nav": "Navigation",
        "input": "Input",
        # Text
        "b": "Bold",
        "i": "Italic",
        "br": "Line Break",
        "p": "Paragraph",
        "pre": "Preformatted Text",
        "samp": "Sample Text",
        # Lists
        "li": "List Item",
        "ol": "Ordered List",
        "ul": "Unordered List",
        # Tables
        "tbody": "Table Rows",
        "th": "Table Header",
        "thead": "Table Header",
        "tfoot": "Table Footer",
        "tr": "Table Row",
        "col": "Table Column",
        "td": "Table Cell",
        "hgroup": "Heading Group",
        "colgroup": "Column Group",
        # Misc
        "hr": "Horizontal Line",
    }

    if tag in names:
        return names[tag]

    return tag


class WebDriverError(Exception):
    """Common exception for all webdriver errors."""


class WebDriver:
    SCRIPT_TIMEOUT = 120.0  # seconds

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.selenium = None
        self.resources = {}
        self.is_remote = False
        self._load_resources()
        self._is_recording: bool = False

    @property
    def browser_pid(self):
        if not self.selenium:
            return None
        return self.selenium.service.process.pid

    @classmethod
    def from_remote(cls, executor_url, session_id, handle):
        # Override new session command to prevent spawning windows
        execute = Remote.execute

        def _execute_patched(self, driver_command, params=None):
            if driver_command == "newSession":
                return {"success": 0, "value": None, "sessionId": session_id}
            else:
                return execute(self, driver_command, params)

        try:
            Remote.execute = _execute_patched
            driver = Remote(command_executor=executor_url)
            driver.session_id = session_id
            driver.switch_to.window(handle)
        finally:
            Remote.execute = execute

        instance = cls()
        instance.selenium = driver
        instance.is_remote = True

        return instance

    @property
    def is_running(self):
        if not self.selenium:
            return False

        try:
            try:
                # Mock interaction to check if webdriver is still available
                _ = self.selenium.current_window_handle
            except NoSuchWindowException:
                # Handle tabs closed by user
                handles = self.selenium.window_handles
                self.selenium.switch_to_window(handles[-1])
            return True
        except Exception:  # pylint: disable=broad-except
            self.selenium = None
            return False

    @property
    def title(self):
        if not self.selenium:
            return None
        return self.selenium.title

    @property
    def url(self):
        if not self.selenium:
            return None
        return self.selenium.current_url

    def _load_resources(self):
        self.resources = {
            "style": load_resource("inspector.css"),
            "inspector": load_resource("inspector.js"),
            "inspect-guide": load_resource("guide.html"),
            "recording-guide": load_resource("browser-recording-guide.html"),
        }
        self.logger.debug("Resources loaded!")

    def _exec_resources(self):
        try:
            self.selenium.find_element(by=By.ID, value="inspector-style")
        except Exception as ex:  # pylint: disable=broad-except
            self.logger.debug("Inspector was not injected. Exception: %s", ex)
            self.logger.debug("Injecting resources to web page...")
            self.selenium.execute_script(self.resources["inspector"])
            self.logger.debug("Inspector code injected!")
            self.selenium.execute_script(
                'var style = document.getElementById("inspector-style");'
                f'var content = document.createTextNode(`{self.resources["style"]}`);'
                "style.appendChild(content);"
            )
            self.logger.debug("Inspector style injected!")
        else:
            self.logger.error(
                "Inspector already injected or did not manage to inject code!"
            )

    def _exec_driver(self, func, *args, **kwargs):
        def error(msg, *error_args):
            self.logger.warning(msg, error_args)
            raise WebDriverError(msg)

        if not self.selenium:
            error("No available webdriver")

        try:
            self._exec_resources()
            return func(*args, **kwargs)
        except TimeoutException:
            error("Timeout while running script")
        except JavascriptException as exc:
            error("Error while running script: %s", exc)
        except WebDriverError as exc:
            error("Webdriver error: %s", exc)
        except (InvalidSessionIdException, NoSuchWindowException) as exc:
            self.selenium = None
            error(exc)

    def _exec_script(self, script, *args, **kwargs):
        return self._exec_driver(self.selenium.execute_script, script, *args, **kwargs)

    def _exec_async_script(self, script, *args, **kwargs):
        return self._exec_driver(
            self.selenium.execute_async_script, script, *args, **kwargs
        )

    @retry(WebDriverExceptions, tries=3, delay=2)
    def _create_any_driver(self, preferred_browser: Optional[str] = None):  # noqa: C901
        """Create a webdriver instance with given options.

        If webdriver download is requested, a cached version will be used if exists.
        """
        browsers = (
            [preferred_browser]
            if preferred_browser is not None
            else webdriver.get_browser_order()
        )

        errors = {}
        for browser in browsers:
            if browser.lower() != "safari":
                # Download web driver (caching is tackled internally)
                path = webdriver.download(browser)
                if isinstance(path, WindowsPath):
                    path = str(path.resolve())
            else:
                # No download required for Safari
                path = None

            if browser.lower() == "chrome":
                options = {"options": chrome_options()}
            else:
                options = {}

            try:
                return self._create_driver(browser, path, **options)
            except WebDriverException as exc:
                self.logger.warning("Failed to start '%s': %s", browser, exc)
                errors[browser] = exc
            except Exception as exc:  # pylint: disable=broad-except
                self.logger.error("Unhandled exception:\n%s", traceback.format_exc())
                errors[browser] = WebDriverException(f"Unhandled exception: {exc}")

        exception_msg = (
            "Could not initiate webdriver's connection to Safari."
            "You must enable the 'Allow Remote Automation' option "
            "in Safari's Develop menu to control Safari via WebDriver: "
            if str(preferred_browser).lower() == "safari"
            else "No available webdriver found for: "
        )

        raise WebDriverExceptions(exception_msg, errors)

    def _create_driver(self, browser: str, path: Optional[str] = None, **options):
        service_args = None
        service_kwargs: Dict[str, Any] = {
            "service_args": None,
            "service_log_path": None,
            "port": 0,
        }

        for name, default in service_kwargs.items():
            service_kwargs[name] = options.pop(name, default)

        service_kwargs["log_path"] = service_kwargs.pop("service_log_path")
        if path:
            service_kwargs["executable_path"] = path

        service_class = SERVICES[browser.lower()]
        if service_class is selenium_webdriver.safari.service.Service:
            service_kwargs.pop("log_path")  # Not supported at all
        elif service_class is selenium_webdriver.ie.service.Service:
            service_kwargs["log_file"] = service_kwargs.pop("log_path")
            service_args = service_kwargs.pop("service_args")

        service_class = self._create_patched_service(service_class)
        service = service_class(**service_kwargs)
        if service_args:
            service.service_args.extend(service_args)

        # NOTE(cmin764): Starting with Selenium 4.9.1, we have to block their
        #  `SeleniumManager` from early stage, otherwise it will be activated when
        #  the WebDriver class itself is instantiated without throwing any error.
        if not shutil.which(service.path):
            raise OSError("Webdriver not available in PATH")

        # Capitalize browser name just to ensure it works if passed as lower case.
        # NOTE: But don't break a browser name like "ChromiumEdge".
        browser = browser[0].upper() + browser[1:]
        return webdriver.start(browser, service, **options)

    def _create_patched_service(self, klass):
        # pylint: disable=too-few-public-methods
        class PatchedService(klass):
            """Custom service class wrapping the picked browser's one."""

            # pylint: disable=no-self-argument
            def _start_process(this, *args, **kwargs):
                try:
                    return super()._start_process(*args, **kwargs)
                except WebDriverException as exc:
                    if "path" in str(exc).lower():
                        # Raises differently in order to not trigger the default
                        #  Selenium Manager webdriver download, while letting the error
                        #  bubble up. (so it's caught and handled by us instead, in
                        #  order to let our core's webdriver-manager to handle the
                        #  download)
                        raise OSError("Webdriver not available in PATH") from exc
                    raise

            # pylint: disable=no-self-argument
            def __del__(this) -> None:
                # With auto-close disabled, we shouldn't call the object's cleanup
                #  method, as this will automatically stop the webdriver service, which
                #  implies a browser shutdown command, which closes the browser.
                if getattr(this, "auto_close", True):
                    super().__del__()

        return PatchedService

    def _to_finder(self, strategy):
        strategy = str(strategy).lower()
        finder = {
            "class": By.CLASS_NAME,
            "css": By.CSS_SELECTOR,
            "id": By.ID,
            "link": By.LINK_TEXT,
            "name": By.NAME,
            "tag": By.TAG_NAME,
            "xpath": By.XPATH,
        }[strategy]

        if not finder:
            raise ValueError(f"Unknown search strategy: {strategy}")

        return lambda val: self.selenium.find_elements(by=finder, value=val)

    def start(self, preferred_browser: Optional[str] = None):
        if self.selenium:
            self.logger.warning("Webdriver already running")

        self.logger.debug("Starting browser")
        self.selenium = self._create_any_driver(preferred_browser)
        self.logger.debug("Selenium driver: %s", self.selenium)
        self.selenium.set_script_timeout(self.SCRIPT_TIMEOUT)

    def stop(self):
        self.logger.debug("Trying to stop driver...")
        if not self.selenium:
            self.logger.debug("Skipping close as no selenium present")
            return

        if self.is_remote:
            self.logger.debug("Skipping close for remote browser")
            return

        try:
            if self.selenium:
                force_kill_process(
                    logger=self.logger, pid=self.selenium.service.process.pid
                )
                self.logger.debug("Finished stopping browser child processes!")
            else:
                self.logger.debug("Skipped force stopping browser.")
        except Exception as ex:  # pylint: disable=W0703
            self.logger.error("There was an error while stopping driver: %s", ex)

        self.selenium = None

    def show_guide(self, guide_resources: str):
        guide = self.resources[guide_resources].encode("utf-8")
        payload = base64.b64encode(guide).decode("utf-8")
        self.selenium.get(f"data:text/html;base64,{payload}")

    def navigate(self, url):
        if url is None or url == self.selenium.current_url:
            self.logger.debug("Skipping navigating to url as it is the same.")
            return
        self.logger.debug("Navigating to: %s", url)
        self.selenium.get(url)

    def pick(self):
        def picker():
            locators = self.selenium.execute_async_script(
                "var callback = arguments[arguments.length - 1];"
                "Inspector.startPicker(callback);"
            )
            if not locators or len(locators) == 0:
                self.logger.debug("No locators were found")
                return {}

            self.logger.debug("Found locators: %s", locators)
            options = {}
            elements = set()
            for name, value in locators:
                self.logger.debug(
                    "Handling locator: name[%s] value[%s]", str(name), str(value)
                )
                strategy = name.split(":", 1)[0]
                self.logger.debug("Detected strategy: %s", str(strategy))
                finder = self._to_finder(str(strategy))
                matches = finder(value)
                self.logger.debug("Detected matches: %s", str(matches))

                if len(matches) == 1:
                    options[str(name)] = {
                        "strategy": str(strategy),
                        "value": str(value),
                    }
                    elements.add(matches[0])

            if len(elements) > 1:
                # TODO: Inform user somehow? How to test?
                self.logger.error("Picker options matching multiple elements")

            return options

        self.logger.debug("Starting interactive picker")
        return self._exec_driver(picker)

    def find(self, strategy, value):
        self.logger.debug("Finding elements: %s:%s", strategy, value)
        finder = self._to_finder(strategy)
        return self._exec_driver(finder, value)

    def get_matched_elements(self, elements):
        try:
            self.logger.debug("Matching %d element(s)", len(elements))
            script = """
var elements = arguments[0];
var tags = Inspector.describeElements(elements);
return tags
            """
            names = [friendly_name(element) for element in elements]
            values = self._exec_script(
                script,
                elements,
            )
            return list(zip(names, values))
        except StaleElementReferenceException as exc:
            self.logger.warning(exc)
            return []

    def highlight(self, elements):
        self.logger.debug("Highlighting %d element(s)", len(elements))
        try:
            self._exec_script(
                "var elements = arguments[0]; Inspector.highlightElements(elements);",
                elements,
            )
        except StaleElementReferenceException as exc:
            self.logger.warning(exc)

    def focus(self, element):
        self.logger.debug("Focusing on element: %s", friendly_name(element))
        try:
            self._exec_script(
                "var element = arguments[0]; Inspector.focusElement(element);",
                element,
            )
        except StaleElementReferenceException as exc:
            self.logger.warning(exc)

    def move_to_element(self, element):
        self.logger.debug("Moving to element: %s", friendly_name(element))
        self.logger.debug("Rect details: %s", element.rect)
        window_size = self.selenium.get_window_size()
        self.logger.debug("Selenium Window size: %s", window_size)
        delta = element.rect["y"] - window_size["height"] / 2

        # scroll with Selenium - making sure Selenium gets close to the element
        ActionChains(self.selenium).scroll_by_amount(0, int(delta)).perform()
        # make sure to wait a while for the scroll to finish
        time.sleep(0.2)
        # always place the element to the center for better clarity
        self._exec_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
            element,
        )
        # wait for scroll to happen
        time.sleep(0.2)

    def clear(self):
        self.logger.debug("Clearing highlights")
        return self._exec_script("Inspector.removeHighlights();")

    def cancel_pick(self):
        self.logger.debug("Canceling picking and clearing highlights")
        return self._exec_script("Inspector.cancelPick();")

    def record_event(self) -> Union[Dict, None]:
        try:
            self._is_recording = True
            self._exec_resources()

            result = self._exec_async_script(
                "var callback = arguments[arguments.length - 1];"
                "Inspector.recordEvent(callback);"
            )
            self.logger.debug(
                "Selenium execute async script finished, result: %s", result
            )
            self._is_recording = False
            return result
        except Exception as ex:  # pylint: disable=W0703
            self.logger.error("There was an exception while recording event: %s", ex)
            return None

    def stop_recording(self) -> None:
        try:
            if self._is_recording:
                self._exec_async_script("Inspector.stopRecording();")
        except Exception as ex:  # pylint: disable=W0703
            self.logger.error("There was an exception while recording event: %s", ex)
        self._is_recording = False
