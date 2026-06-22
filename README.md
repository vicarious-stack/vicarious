# Vicarious

A premium, immersive literary‑fiction web reader blending neuroscience, psychology, systems thinking, and narrative storytelling.

- **Read Online (Live)**: [https://vicarious-stack.github.io/vicarious/](https://vicarious-stack.github.io/vicarious/)
- **Repository**: Contains the full manuscript (`chapter_01.md` ... `chapter_12.md`, 6 scientific interludes, prologue, epilogue, and appendices), supporting build/validation scripts, and the web reader implementation.
- **Premium Reader Features**: Midnight Void, Warm Alabaster, and Amber Night color themes; dynamic font scaling; collapsible Table of Contents; scroll progress tracking; estimated reading time; and persistent user preferences via LocalStorage.

## Getting Started (Local Host)

Since the reader fetches the book content asynchronously, you should run a local HTTP server instead of double-clicking the `index.html` file (which may fail due to browser CORS policies).

### 1. Clone the repository
```bash
git clone https://github.com/vicarious-stack/vicarious.git
cd vicarious
```

### 2. Run a local web server
Using Python:
```bash
python -m http.server 8787
```

Using Node.js (`http-server`):
```bash
npx http-server -p 8787
```

### 3. Open the reader
Open your browser and navigate to:
[http://localhost:8787/index.html](http://localhost:8787/index.html)

---
Feel free to explore, remix, or contribute!
