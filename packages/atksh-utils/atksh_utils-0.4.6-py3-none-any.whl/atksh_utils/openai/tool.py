import json
import os
import subprocess
import tempfile
import time
from code import InteractiveConsole
from itertools import islice
from typing import Any

import requests
from bs4 import BeautifulSoup as bs4
from duckduckgo_search import DDGS

from .prompt import SEARCH_RESULT_SUMMARIZE_PROMPT, VISIT_PAGE_SUMMARIZE_PROMPT

# Create a temporary directory for storing files to $HOME/.cache/askgpt/
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "askgpt")
os.makedirs(CACHE_DIR, exist_ok=True)
SESSION_PATH = os.path.join(CACHE_DIR, "session.pkl")


def _clear_session():
    """Clears the session file."""
    if os.path.exists(SESSION_PATH):
        os.remove(SESSION_PATH)


MAX_ATTEMPTS = 3
MAX_SEARCH_RESULTS = 8


def get_browser_functions(ai: "OpenAI"):
    search_result_child = ai.make_child(model_name="gpt-3.5-turbo-16k", max_tokens=15000)
    search_result_child.set_system_prompt(SEARCH_RESULT_SUMMARIZE_PROMPT)
    visit_page_child = ai.make_child(model_name="gpt-3.5-turbo-16k", max_tokens=15000)
    visit_page_child.set_system_prompt(VISIT_PAGE_SUMMARIZE_PROMPT)

    def _search_summarize(query_text: str, results: str) -> str:
        """Summarizes the query text and results."""
        return search_result_child(f"Query: {query_text}\nResults: {results}\nSummary: ")[1]

    def _page_summarize(query_text: str, page: str) -> str:
        """Summarizes the query text and page."""
        return visit_page_child(f"Query: {query_text}\nPage: {page}\nSummary: ")[1]

    def web_search(query_text: str) -> str:
        """Searches the web for the query text.

        :param query_text: The keywords to query. For example, `The capital of Japan` or `首都 日本`.
        :type query_text: str
        :return: json dumped results (string)
        :rtype: str
        """
        attempts = 0
        search_results = []
        while attempts < MAX_ATTEMPTS:
            ddgs = DDGS()
            time.sleep(1)
            result = ddgs.text(query_text, region="ja-ja", safesearch="Off")
            search_results = list(islice(result, MAX_SEARCH_RESULTS))
            if search_results:
                break
            attempts += 1

        results = json.dumps(search_results, ensure_ascii=False, indent=2)
        ret = _search_summarize(query_text, results)
        return ret

    def visit_page(query_text: str, url: str) -> str:
        """Visits the page at the url and summarizes the text with respect to the query text. Recommended to use after web_search for each url.

        :param query_text: The text to query for summarization.
        :type query_text: str
        :param url: The url to visit (must be a valid url like `https://www.google.com`).
        :type url: str
        :return: The summarized text of the page.
        :rtype: str
        """
        try:
            response = requests.get(url)
            soup = bs4(response.text, "html.parser")
            body = soup.find("body").text.strip()
            ret = _page_summarize(query_text, body[:10000])
        except Exception as e:
            ret = f"Error: {e}.\nPlease try again or try another url."
        return ret

    return web_search, visit_page


def exec_python_code(code: str) -> str:
    """This is a function that executes Python code and returns the stdout. Don't forget to print the result.

    :param code: Python code of multiple lines. You must print the result. For example, `value = 2 + 3; print(value)`.
    :type code: str
    :return: The result of the execution of the Python code (stdout by print)
    :rtype: str
    """
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py") as f:
            f.write("import dill\n")
            f.write(f"try:\n    dill.load_session('{SESSION_PATH}')\nexcept:\n    pass\n")
            f.write(code)
            f.write(f"\ndill.dump_session('{SESSION_PATH}')\n")
            f.flush()
            result = subprocess.check_output(["python", f.name])
        result = result.decode("utf-8").strip()
        if not result:
            result = "NotPrintedError('The result is not printed.')"
    except Exception as e:
        result = f"Error: {e}.\nPlease try again or try another code."
    return result
