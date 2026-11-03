import sys

try:
    import fitz

    d = fitz.open(sys.argv[1])
    print("paginas", len(d))
    for i, p in enumerate(d, 1):
        t = p.get_text()
        print(f"--- p{i} chars={len(t)} imgs={len(p.get_images())}")
        print(t)
except ImportError:
    from pypdf import PdfReader

    r = PdfReader(sys.argv[1])
    print("paginas", len(r.pages))
    for i, p in enumerate(r.pages, 1):
        t = p.extract_text()
        print(f"--- p{i} chars={len(t)}")
        print(t)
