# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import termcolor
import time
import os
import sys
import json
import base64
from pathlib import Path
from datetime import datetime
from ..computer import (
    Computer,
    EnvState,
)
from ..data_extraction_prompt import EXTRACTION_PROMPT_V3
import playwright.sync_api
from playwright.sync_api import sync_playwright
from typing import Literal, Dict, Any

# Define a mapping from the user-friendly key names to Playwright's expected key names.
# Playwright is generally good with case-insensitivity for these, but it's best to be canonical.
# See: https://playwright.dev/docs/api/class-keyboard#keyboard-press
# Keys like 'a', 'b', '1', '$' are passed directly.
PLAYWRIGHT_KEY_MAP = {
    "backspace": "Backspace",
    "tab": "Tab",
    "return": "Enter",  # Playwright uses 'Enter'
    "enter": "Enter",
    "shift": "Shift",
    "control": "ControlOrMeta",
    "alt": "Alt",
    "escape": "Escape",
    "space": "Space",  # Can also just be " "
    "pageup": "PageUp",
    "pagedown": "PageDown",
    "end": "End",
    "home": "Home",
    "left": "ArrowLeft",
    "up": "ArrowUp",
    "right": "ArrowRight",
    "down": "ArrowDown",
    "insert": "Insert",
    "delete": "Delete",
    "semicolon": ";",  # For actual character ';'
    "equals": "=",  # For actual character '='
    "multiply": "Multiply",  # NumpadMultiply
    "add": "Add",  # NumpadAdd
    "separator": "Separator",  # Numpad specific
    "subtract": "Subtract",  # NumpadSubtract, or just '-' for character
    "decimal": "Decimal",  # NumpadDecimal, or just '.' for character
    "divide": "Divide",  # NumpadDivide, or just '/' for character
    "f1": "F1",
    "f2": "F2",
    "f3": "F3",
    "f4": "F4",
    "f5": "F5",
    "f6": "F6",
    "f7": "F7",
    "f8": "F8",
    "f9": "F9",
    "f10": "F10",
    "f11": "F11",
    "f12": "F12",
    "command": "Meta",  # 'Meta' is Command on macOS, Windows key on Windows
}


class PlaywrightComputer(Computer):
    """Connects to a local Playwright instance."""

    def __init__(
        self,
        screen_size: tuple[int, int],
        initial_url: str = "https://www.google.com",
        search_engine_url: str = "https://www.google.com",
        highlight_mouse: bool = False,
        record_video: bool = True,
        parcel_number :str = None, 
        tax_year :str =None, 
        installment: str =None 
    ):
        self._initial_url = initial_url
        self._screen_size = screen_size
        self._search_engine_url = search_engine_url
        self._highlight_mouse = highlight_mouse
        self._record_video = record_video
        self._video_path = None
        self._parcel_number = parcel_number
        self._tax_year = tax_year
        self._installment = installment

    def _handle_new_page(self, new_page: playwright.sync_api.Page):
        """The Computer Use model only supports a single tab at the moment.

        Some websites, however, try to open links in a new tab.
        For those situations, we intercept the page-opening behavior, and instead overwrite the current page.
        """
        new_url = new_page.url
        new_page.close()
        # Increase timeout to 60 seconds (120000ms) for slow-loading pages
        self._page.goto(new_url, timeout=90000) 

    def __enter__(self):
        print("Creating session...")
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            args=[
                "--disable-extensions",
                "--disable-file-system",
                "--disable-plugins",
                "--disable-dev-shm-usage",
                "--disable-background-networking",
                "--disable-default-apps",
                "--disable-sync",
                # No '--no-sandbox' arg means the sandbox is on.
            ],
            headless=bool(os.environ.get("PLAYWRIGHT_HEADLESS", False)),
        )
        
        # Setup video recording if enabled
        context_options = {
            "viewport": {
                "width": self._screen_size[0],
                "height": self._screen_size[1],
            }
        }
        
        if self._record_video:
            # Create recording directory
            recording_dir = Path("./data/recording")
            recording_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate video filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self._video_path = recording_dir / f"session_{timestamp}"
            
            context_options["record_video_dir"] = str(recording_dir)
            context_options["record_video_size"] = {
                "width": self._screen_size[0],
                "height": self._screen_size[1],
            }
        
        self._context = self._browser.new_context(**context_options)
        self._page = self._context.new_page()
        # Increase timeout to 120 seconds (120000ms) for slow-loading pages
        self._page.goto(self._initial_url, timeout=120000)

        self._context.on("page", self._handle_new_page)

        termcolor.cprint(
            f"Started local playwright.",
            color="green",
            attrs=["bold"],
        )
        if self._record_video:
            termcolor.cprint(
                f"🎥 Recording video to: {recording_dir}/",
                color="cyan",
            )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Save video before closing
        if self._record_video and self._page:
            try:
                # Close page to ensure video is saved
                video = self._page.video
                if video:
                    # video_path = video.path() 
                    # video_path = video.path() 
                    recording_dir = Path("./data/recording") 
                    recording_dir.mkdir(parents=True, exist_ok=True) 
                    
                    # Generate video filename with timestamp 
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    video_path = recording_dir / f"{self._parcel_number}_{timestamp}"
                    termcolor.cprint(
                        f"✅ Video saved to: {video_path}",
                        color="green",
                        attrs=["bold"],
                    )
            except Exception as e:
                termcolor.cprint(
                    f"⚠️  Warning: Could not get video path: {e}",
                    color="yellow",
                )
        
        if self._context:
            self._context.close()
        try:
            self._browser.close()
        except Exception as e:
            # Browser was already shut down because of SIGINT or such.
            if "Browser.close: Connection closed while reading from the driver" in str(
                e
            ):
                pass
            else:
                raise

        self._playwright.stop()

    def open_web_browser(self) -> EnvState:
        return self.current_state()

    def click_at(self, x: int, y: int):
        self.highlight_mouse(x, y)
        self._page.mouse.click(x, y)
        self._page.wait_for_load_state()
        return self.current_state()

    def hover_at(self, x: int, y: int):
        self.highlight_mouse(x, y)
        self._page.mouse.move(x, y)
        self._page.wait_for_load_state()
        return self.current_state()

    def type_text_at(
        self,
        x: int,
        y: int,
        text: str,
        press_enter: bool = False,
        clear_before_typing: bool = True,
    ) -> EnvState:
        self.highlight_mouse(x, y)
        self._page.mouse.click(x, y)
        self._page.wait_for_load_state()

        if clear_before_typing:
            if sys.platform == "darwin":
                self.key_combination(["Command", "A"])
            else:
                self.key_combination(["Control", "A"])
            self.key_combination(["Delete"])

        self._page.keyboard.type(text)
        self._page.wait_for_load_state()

        if press_enter:
            self.key_combination(["Enter"])
        self._page.wait_for_load_state()
        return self.current_state()

    def _horizontal_document_scroll(
        self, direction: Literal["left", "right"]
    ) -> EnvState:
        # Scroll by 50% of the viewport size.
        horizontal_scroll_amount = self.screen_size()[0] // 2
        if direction == "left":
            sign = "-"
        else:
            sign = ""
        scroll_argument = f"{sign}{horizontal_scroll_amount}"
        # Scroll using JS.
        self._page.evaluate(f"window.scrollBy({scroll_argument}, 0); ")
        self._page.wait_for_load_state()
        return self.current_state()

    def scroll_document(
        self, direction: Literal["up", "down", "left", "right"]
    ) -> EnvState:
        if direction == "down":
            return self.key_combination(["PageDown"])
        elif direction == "up":
            return self.key_combination(["PageUp"])
        elif direction in ("left", "right"):
            return self._horizontal_document_scroll(direction)
        else:
            raise ValueError("Unsupported direction: ", direction)

    def scroll_at(
        self,
        x: int,
        y: int,
        direction: Literal["up", "down", "left", "right"],
        magnitude: int = 800,
    ) -> EnvState:
        self.highlight_mouse(x, y)

        self._page.mouse.move(x, y)
        self._page.wait_for_load_state()

        dx = 0
        dy = 0
        if direction == "up":
            dy = -magnitude
        elif direction == "down":
            dy = magnitude
        elif direction == "left":
            dx = -magnitude
        elif direction == "right":
            dx = magnitude
        else:
            raise ValueError("Unsupported direction: ", direction)

        self._page.mouse.wheel(dx, dy)
        self._page.wait_for_load_state()
        return self.current_state()

    def wait_5_seconds(self) -> EnvState:
        time.sleep(5)
        return self.current_state()

    def go_back(self) -> EnvState:
        self._page.go_back()
        self._page.wait_for_load_state()
        return self.current_state()

    def go_forward(self) -> EnvState:
        self._page.go_forward()
        self._page.wait_for_load_state()
        return self.current_state()

    def search(self) -> EnvState:
        return self.navigate(self._search_engine_url)

    def navigate(self, url: str) -> EnvState:
        normalized_url = url
        if not normalized_url.startswith(("http://", "https://")):
            normalized_url = "https://" + normalized_url
        # Increase timeout to 120 seconds (120000ms) for slow-loading pages
        self._page.goto(normalized_url, timeout=120000)
        self._page.wait_for_load_state()
        return self.current_state()

    def key_combination(self, keys: list[str]) -> EnvState:
        # Normalize all keys to the Playwright compatible version.
        keys = [PLAYWRIGHT_KEY_MAP.get(k.lower(), k) for k in keys]

        for key in keys[:-1]:
            self._page.keyboard.down(key)

        self._page.keyboard.press(keys[-1])

        for key in reversed(keys[:-1]):
            self._page.keyboard.up(key)

        return self.current_state()

    def drag_and_drop(
        self, x: int, y: int, destination_x: int, destination_y: int
    ) -> EnvState:
        self.highlight_mouse(x, y)
        self._page.mouse.move(x, y)
        self._page.wait_for_load_state()
        self._page.mouse.down()
        self._page.wait_for_load_state()

        self.highlight_mouse(destination_x, destination_y)
        self._page.mouse.move(destination_x, destination_y)
        self._page.wait_for_load_state()
        self._page.mouse.up()
        return self.current_state()

    def current_state(self) -> EnvState:
        self._page.wait_for_load_state()
        # Even if Playwright reports the page as loaded, it may not be so.
        # Add a manual sleep to make sure the page has finished rendering.
        time.sleep(8) 
        screenshot_bytes = self._page.screenshot(type="png", full_page=False) 
        print("\033[92m URL Navigated : ", self._page.url, "\033[0m")
        return EnvState(screenshot=screenshot_bytes, url=self._page.url)

    def screen_size(self) -> tuple[int, int]:
        viewport_size = self._page.viewport_size
        # If available, try to take the local playwright viewport size.
        if viewport_size:
            return viewport_size["width"], viewport_size["height"]
        # If unavailable, fall back to the original provided size.
        return self._screen_size

    def highlight_mouse(self, x: int, y: int):
        if not self._highlight_mouse:
            return
        self._page.evaluate(
            f"""
        () => {{
            const element_id = "playwright-feedback-circle";
            const div = document.createElement('div');
            div.id = element_id;
            div.style.pointerEvents = 'none';
            div.style.border = '4px solid red';
            div.style.borderRadius = '50%';
            div.style.width = '20px';
            div.style.height = '20px';
            div.style.position = 'fixed';
            div.style.zIndex = '9999';
            document.body.appendChild(div);

            div.hidden = false;
            div.style.left = {x} - 10 + 'px';
            div.style.top = {y} - 10 + 'px';

            setTimeout(() => {{
                div.hidden = true;
            }}, 2000);
        }}
    """
        )
        # Wait a bit for the user to see the cursor.
        time.sleep(1)

    def get_data_from_last_page(
        self,
        extraction_goal: str = "Extract all relevant information from the page",
        fields: Dict[str, str] = None,
    ) -> Dict[str, Any]:
        """
        Extract structured data from the current page using Gemini.

        Args:
            extraction_goal: What to extract from the page
            fields: List of field names to extract (e.g., ['parcel_number', 'owner_name'])

        Returns:
            Dictionary with extracted data in JSON format
        """
        try:
            # Wait for page to settle
            time.sleep(2)

            # Get page content as HTML
            html_content = self._page.content()

            # Convert HTML to Markdown (simplified extraction)
            # try:
            import markdownify

            content = markdownify.markdownify(html_content, strip=["a", "img"])
            for iframe in self._page.frames:
                if iframe.url != self._page.url and not iframe.url.startswith('data:'):
                    content += f'\n\nIFRAME {iframe.url}:\n'
                    content += markdownify.markdownify(iframe.content())

            # Save markdown content to a file 
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            md_file_path = f"./data/markdown/page_{timestamp}.md"
            md_file_path_obj = Path(md_file_path)
            md_file_path_obj.parent.mkdir(parents=True, exist_ok=True)
            with open(md_file_path_obj, "w", encoding="utf-8") as f:
                f.write(content)
        # except ImportError:
            # Fallback to HTML if markdownify not available
            # print("falling back to html")
            # content = html_content

            # If no fields specified, return markdown content
            if not fields:
                termcolor.cprint("📄 Extracted page content", color="green")
                return {"content": content, "url": self._page.url}

            # Use Gemini for structured extraction
            from google import genai

            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                termcolor.cprint(
                    "⚠️  GEMINI_API_KEY not set, returning raw content", color="yellow"
                )
                return {"content": content, "url": self._page.url}

            client = genai.Client(api_key=api_key)

            # Create prompt using EXTRACTION_PROMPT_V3 template
            # Save prompt to file
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            prompt_file_path = f"./data/prompts/extraction_prompt_{timestamp}.txt"
            prompt_file_path_obj = Path(prompt_file_path)
            prompt_file_path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Format the EXTRACTION_PROMPT_V3 with required variables
            prompt = EXTRACTION_PROMPT_V3.format(
                # parcelNumber=self._parcel_number or "",
                data=content
            )
            
            with open(prompt_file_path_obj, "w", encoding="utf-8") as f:
                f.write(prompt)

            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
            
            
            print("response : ", response)
            print("response : ", response.text) 

            # # Parse JSON from response
            # json_text = response.text.strip()
            
            # # Remove markdown code block markers
            # if json_text.startswith("```json"):
            #     json_text = json_text[7:]
            # elif json_text.startswith("```"):
            #     json_text = json_text[3:]
            
            # if json_text.endswith("```"):
            #     json_text = json_text[:-3]
            
            # Strip again to remove any whitespace after removing markers
            # json_text = json_text.strip()
            
            # Find the actual JSON object/array start
            # Handle cases where there might be text before the JSON
            # json_start = -1
            # for i, char in enumerate(json_text):
            #     if char in ['{', '[']:
            #         json_start = i
            #         break
            
            # if json_start > 0:
            #     json_text = json_text[json_start:]
            # elif json_start == -1:
            #     # No JSON found, raise an error
            #     raise ValueError(f"No JSON object found in response. Response text: {json_text[:200]}")

            # extracted_data = json.loads(json_text.strip())
            # extracted_data["url"] = self._page.url

            # print("*"*100) 
            # print("\033[92m extracted data : \n ", extracted_data, "\033[0m")
            # print("*"*100) 
            
            termcolor.cprint(
                # f"📊 Extracted structured data: {list(extracted_data.keys())}",
                f"📊 Extracted structured data: {response}",
                color="green",
            )
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            ex_data = f"./data/ext/extraction_data_{timestamp}.txt"
            ex_data_obj = Path(ex_data)
            ex_data_obj.parent.mkdir(parents=True, exist_ok=True)
            
            with open(ex_data_obj, "w", encoding="utf-8") as f:
                f.write(str(response))
        
            return response

        except json.JSONDecodeError as e:
            termcolor.cprint(f"⚠️  Failed to parse JSON: {e}", color="yellow")
            return {
                "content": content,
                "url": self._page.url,
                "error": "Failed to parse JSON",
            }
        except Exception as e:
            termcolor.cprint(f"❌ Error extracting data: {e}", color="red")
            return {"error": str(e), "url": self._page.url}

    def save_last_page_as_pdf(
        self, file_path: str = None, return_base64: bool = False
    ) -> Dict[str, Any]:
        """
        Save the current page as PDF.

        Args:
            file_path: Path to save PDF file. If None, generates filename from URL
            return_base64: If True, returns base64 encoded PDF data

        Returns:
            Dictionary with success status, file path, and optionally base64 data
        """
        try:
            # Generate default filename if not provided
            if not file_path:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                file_path = f"./data/pdfs/page_{timestamp}.pdf"

            # Ensure directory exists
            file_path_obj = Path(file_path)
            file_path_obj.parent.mkdir(parents=True, exist_ok=True)

            # Default PDF options
            pdf_options = {
                "format": "A4",
                "print_background": True,
                "margin": {
                    "top": "1cm",
                    "right": "1cm",
                    "bottom": "1cm",
                    "left": "1cm",
                },
            }

            # Generate PDF
            pdf_bytes = self._page.pdf(**pdf_options)

            # Save to file
            with open(file_path_obj, "wb") as f:
                f.write(pdf_bytes)

            result = {
                "success": True,
                "file_path": str(file_path_obj.absolute()),
                "url": self._page.url,
                "size_bytes": len(pdf_bytes),
            }

            # Add base64 if requested
            if return_base64:
                result["base64"] = base64.b64encode(pdf_bytes).decode("utf-8")

            termcolor.cprint(
                f"📄 Successfully saved PDF to: {file_path_obj}", color="green"
            )
            return result

        except Exception as e:
            error_msg = f"Failed to save PDF: {str(e)}"
            termcolor.cprint(f"❌ {error_msg}", color="red")
            return {"success": False, "error": error_msg, "url": self._page.url}

