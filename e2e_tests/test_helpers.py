import re
import os
import sys
import html.parser
import subprocess
import http.server
import socketserver
import threading
import time

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class Element:
    def __init__(self, tag, attrs):
        self.tag = tag
        self.attrs = dict(attrs) if attrs else {}
        self.text = ""
        self.children = []
        self.parent = None
        
    def find_by_id(self, elem_id):
        if self.attrs.get("id") == elem_id:
            return self
        for child in self.children:
            found = child.find_by_id(elem_id)
            if found:
                return found
        return None
        
    def find_all(self, tag=None, class_name=None):
        results = []
        # Check tag match
        tag_match = (tag is None or self.tag == tag)
        # Check class match
        class_match = True
        if class_name is not None:
            classes = self.attrs.get("class", "").split()
            class_match = (class_name in classes)
        
        if tag_match and class_match:
            results.append(self)
            
        for child in self.children:
            results.extend(child.find_all(tag, class_name))
        return results

class DOMParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = Element("root", {})
        self.current = self.root
        self.style_content = []
        self.script_content = []
        self.in_style = False
        self.in_script = False
        
    def handle_starttag(self, tag, attrs):
        elem = Element(tag, attrs)
        elem.parent = self.current
        self.current.children.append(elem)
        self.current = elem
        if tag == 'style':
            self.in_style = True
        if tag == 'script':
            self.in_script = True
            
    def handle_endtag(self, tag):
        if tag == 'style':
            self.in_style = False
        if tag == 'script':
            self.in_script = False
        if self.current.parent:
            self.current = self.current.parent
            
    def handle_data(self, data):
        if self.in_style:
            self.style_content.append(data)
        elif self.in_script:
            self.script_content.append(data)
        if self.current:
            self.current.text += data

def load_index_html(path):
    """
    Loads index.html and parses it into a DOM tree.
    Returns (root_element, style_content_str, script_content_str)
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"index.html not found at path: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    parser = DOMParser()
    parser.feed(content)
    return parser.root, "".join(parser.style_content), "".join(parser.script_content)

def parse_markdown_structure(content):
    """
    Parses Markdown content and returns structured data:
    - headers: list of (level, title)
    - blockquotes: list of blockquote text
    - code_blocks: list of (language, code)
    - citations: list of citation strings
    - word_count: total word count
    """
    # Word count
    words = content.split()
    word_count = len(words)

    # Headers
    headers = []
    header_regex = re.compile(r'^(#{1,6})\s+(.*)$', re.MULTILINE)
    for match in header_regex.finditer(content):
        level = len(match.group(1))
        title = match.group(2).strip()
        headers.append((level, title))

    # Blockquotes
    blockquotes = []
    # Contiguous blockquote lines or individual blockquote content lines
    bq_regex = re.compile(r'^>\s?(.*)$', re.MULTILINE)
    for match in bq_regex.finditer(content):
        blockquotes.append(match.group(1).strip())

    # Code blocks
    code_blocks = []
    cb_regex = re.compile(r'^```(\w*)\n(.*?)```', re.DOTALL | re.MULTILINE)
    for match in cb_regex.finditer(content):
        language = match.group(1)
        code = match.group(2)
        code_blocks.append((language, code))

    # Citations: superscripts like [^1] or [1]
    citation_regex = re.compile(r'\[\^?(\w+)\]')
    citations = citation_regex.findall(content)

    return {
        "headers": headers,
        "blockquotes": blockquotes,
        "code_blocks": code_blocks,
        "citations": citations,
        "word_count": word_count
    }

def match_js_patterns(js_content, patterns):
    """
    Performs static regex pattern matching on JS block.
    patterns: list of compiled regexes or string patterns.
    Returns list of booleans indicating matches.
    """
    results = []
    for pattern in patterns:
        if isinstance(pattern, str):
            regex = re.compile(pattern)
        else:
            regex = pattern
        results.append(bool(regex.search(js_content)))
    return results

class SilentHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress logging
        pass

class BackgroundServer:
    def __init__(self, directory, port=8000):
        self.directory = directory
        self.port = port
        self.server = None
        self.thread = None

    def start(self):
        # Keep directory serving compatible with Python 3.7+
        class Handler(SilentHTTPRequestHandler):
            def __init__(self_handler, *args, **kwargs):
                super().__init_handler__(*args, directory=self.directory, **kwargs)

        for p in range(self.port, self.port + 100):
            try:
                self.server = socketserver.TCPServer(("", p), Handler)
                self.port = p
                break
            except OSError:
                continue
        else:
            raise OSError("Could not find an available port to start http.server")

        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        time.sleep(0.1)

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.thread.join()

def run_cli_tool(args, cwd=None, env=None):
    """
    Runs a CLI tool (e.g. ['python', 'validate.py'])
    Returns (returncode, stdout, stderr)
    """
    result = subprocess.run(
        args,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )
    return result.returncode, result.stdout, result.stderr
