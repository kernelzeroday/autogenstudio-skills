import os
import pytest
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from tool_kit.plot_diagram import draw_geometric_structure
from tool_kit.webscrape import save_webpage_as_text

class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><p>Test Content</p></body></html>")

def run_mock_server(server_class=HTTPServer, handler_class=MockServerRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def test_draw_geometric_structure():
    file_name = 'test_structure'
    image_path = draw_geometric_structure(file_name, base_circles=5, base_circle_color='red', top_circle_color='green', line_color='black', line_width=3)
    
    # Check if the file was created
    assert os.path.exists(image_path)
    
    # Clean up the created file
    os.remove(image_path)
    os.rmdir('diagrams')

def test_save_webpage_as_text_mock(monkeypatch):
    class MockResponse:
        def __init__(self, text):
            self.text = text

    def mock_get(*args, **kwargs):
        return MockResponse("<html><body><p>Test Content</p></body></html>")

    monkeypatch.setattr("requests.get", mock_get)
    
    url = 'http://example.com'
    output_filename = 'test_webpage_content.txt'
    file_path = save_webpage_as_text(url, output_filename)
    
    # Check if the file was created
    assert os.path.exists(file_path)
    
    # Check the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        assert "Test Content" in content
    
    # Clean up the created file
    os.remove(file_path)

def test_save_webpage_as_text_real():
    server_thread = threading.Thread(target=run_mock_server)
    server_thread.daemon = True
    server_thread.start()

    url = 'http://localhost:8000'
    output_filename = 'test_webpage_content.txt'
    file_path = save_webpage_as_text(url, output_filename)
    
    # Check if the file was created
    assert os.path.exists(file_path)
    
    # Check the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        assert "Test Content" in content
    
    # Clean up the created file
    os.remove(file_path)

if __name__ == "__main__":
    pytest.main(["-v", __file__])
