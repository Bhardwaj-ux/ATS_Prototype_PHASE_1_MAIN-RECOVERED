class ConversionError(Exception):
    pass


def convert_pdf_to_markdown(file_obj) -> str:
    """
    Extracts plain text from a PDF using PyMuPDF only (no pymupdf4llm,
    no onnxruntime). Output isn't literal Markdown, but it preserves
    paragraph/page breaks well enough for the LLM extraction step,
    which only needs readable structured text, not real markdown.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError as exc:
        raise ConversionError(f"Missing PDF conversion dependency: {exc}") from exc

    try:
        file_obj.seek(0)
        data = file_obj.read()
        doc = fitz.open(stream=data, filetype="pdf")

        page_texts = []
        for page in doc:
            text = page.get_text("text")
            if text and text.strip():
                page_texts.append(text.strip())
        doc.close()

        markdown_text = "\n\n".join(page_texts)
    except Exception as exc:
        raise ConversionError(f"Could not read this PDF file: {exc}") from exc

    return markdown_text


def convert_docx_to_markdown(file_obj) -> str:
    try:
        import mammoth
        from markdownify import markdownify
    except ImportError as exc:
        raise ConversionError(f"Missing DOCX conversion dependency: {exc}") from exc

    try:
        file_obj.seek(0)
        result = mammoth.convert_to_html(file_obj)
        markdown_text = markdownify(result.value, heading_style="ATX")
    except Exception as exc:
        raise ConversionError(f"Could not read this DOCX file: {exc}") from exc

    return markdown_text
