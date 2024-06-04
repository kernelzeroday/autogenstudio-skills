import os
import pytest
from web_search.duck_duck_go import search_duckduckgo
from web_search.web_search import WebSearch, CONFIG

def test_search_duckduckgo_mock(monkeypatch):
    class MockDDGS:
        def text(self, keywords, region, safesearch, max_results):
            return [
                {"title": "Test Title 1", "href": "http://example.com/1", "body": "Test Snippet 1"},
                {"title": "Test Title 2", "href": "http://example.com/2", "body": "Test Snippet 2"}
            ]

    monkeypatch.setattr("web_search.duck_duck_go.DDGS", MockDDGS)
    results = search_duckduckgo("test query")
    assert len(results) == 2
    assert results[0]["title"] == "Test Title 1"
    assert results[0]["href"] == "http://example.com/1"
    assert results[0]["body"] == "Test Snippet 1"

def test_search_duckduckgo_real():
    results = search_duckduckgo("Python programming")
    assert len(results) > 0
    assert "title" in results[0]
    assert "href" in results[0]
    assert "body" in results[0]

def test_web_search_google_mock(monkeypatch):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    def mock_get(*args, **kwargs):
        return MockResponse({
            "items": [
                {"title": "Google Title 1", "link": "http://google.com/1", "snippet": "Google Snippet 1"},
                {"title": "Google Title 2", "link": "http://google.com/2", "snippet": "Google Snippet 2"}
            ]
        }, 200)

    monkeypatch.setattr("requests.get", mock_get)
    search = WebSearch(CONFIG)
    results = search.search_query("test query")
    assert len(results) == 2
    assert results[0] == ("Google Title 1", "http://google.com/1", "Google Snippet 1")

@pytest.mark.skipif(
    not os.getenv("GOOGLE_API_KEY") or not os.getenv("GOOGLE_SEARCH_ENGINE_ID"),
    reason="Google API key or search engine ID not set in environment variables"
)
def test_web_search_google_real():
    CONFIG["api_provider"] = "google"
    search = WebSearch(CONFIG)
    results = search.search_query("Python programming")
    assert len(results) > 0
    assert isinstance(results[0], tuple)
    assert len(results[0]) == 3

def test_web_search_bing_mock(monkeypatch):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    def mock_get(*args, **kwargs):
        return MockResponse({
            "webPages": {
                "value": [
                    {"name": "Bing Title 1", "url": "http://bing.com/1", "snippet": "Bing Snippet 1"},
                    {"name": "Bing Title 2", "url": "http://bing.com/2", "snippet": "Bing Snippet 2"}
                ]
            }
        }, 200)

    monkeypatch.setattr("requests.get", mock_get)
    CONFIG["api_provider"] = "bing"
    search = WebSearch(CONFIG)
    results = search.search_query("test query")
    assert len(results) == 2
    assert results[0] == ("Bing Title 1", "http://bing.com/1", "Bing Snippet 1")

@pytest.mark.skipif(
    not os.getenv("BING_API_KEY"),
    reason="Bing API key not set in environment variables"
)
def test_web_search_bing_real():
    CONFIG["api_provider"] = "bing"
    search = WebSearch(CONFIG)
    results = search.search_query("Python programming")
    assert len(results) > 0
    assert isinstance(results[0], tuple)
    assert len(results[0]) == 3

if __name__ == "__main__":
    pytest.main(["-v", __file__])
