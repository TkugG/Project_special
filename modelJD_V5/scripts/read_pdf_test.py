import sys
print("Python version:", sys.version)

try:
    import pypdf
    print("pypdf available")
except ImportError:
    print("pypdf NOT available")

try:
    import fitz # PyMuPDF
    print("fitz available")
except ImportError:
    print("fitz NOT available")

try:
    import pdfplumber
    print("pdfplumber available")
except ImportError:
    print("pdfplumber NOT available")
