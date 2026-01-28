#!/usr/bin/env python3
"""Clean up generated HTML documentation files.

Removes:
- Broken links to __main__ and __version__
- Unnecessary index links in headers
"""

import re
from pathlib import Path

DOCS_DIR = Path("docs/api")

def clean_html_files():
    """Clean HTML files from pydoc generation."""
    cleaned_count = 0
    
    for html_file in DOCS_DIR.glob("*.html"):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # Remove links to __main__ and __version__
            content = re.sub(r'<a href="[^"]*?__main__\.html">__main__</a><br>\s*', '', content)
            content = re.sub(r'<a href="[^"]*?__version__\.html">__version__</a><br>\s*', '', content)
            content = re.sub(r'<a href="[^"]*?__main__\.html">__main__</a>\s*', '', content)
            content = re.sub(r'<a href="[^"]*?__version__\.html">__version__</a>\s*', '', content)
            
            # Remove index link from header (keeping just the "index" text is useless)
            # But keep it simple - just remove the href link, leaving nothing
            content = re.sub(r'<a href="\.">\s*index\s*</a><br>\s*', '', content)
            content = re.sub(r'<br>\s*<a href="\.">\s*index\s*</a>', '', content)
            content = re.sub(r'<td class="extra"><a href="file:[^"]*?">[^<]*?</a></td></tr></table>', '', content)
            
            if content != original:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                cleaned_count += 1
                print(f"Cleaned {html_file.name}")
                
        except Exception as e:
            print(f"Error processing {html_file.name}: {e}")
    
    return cleaned_count

if __name__ == "__main__":
    count = clean_html_files()
    print(f"\nDone! Cleaned {count} file(s).")
