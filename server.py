from mcp.server.fastmcp import FastMCP
import openpyxl
from PIL import Image
import pytesseract
import base64
import io
import os
mcp = FastMCP("Friends Technologies", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))


@mcp.tool()
def hello_world(name: str) -> str:
    """Simple test tool to verify server is working."""
    return f"Hello {name}, Friends Technologies MCP server is running!"


@mcp.tool()
def image_to_excel(image_base64: str, output_filename: str = "output.xlsx") -> str:
    """
    Convert a table image (base64 encoded) into an Excel (.xlsx) file.

    Args:
        image_base64: Base64 encoded image data (table/screenshot)
        output_filename: Name for the output Excel file
    """
    try:
        # Base64 -> Image
        img_data = base64.b64decode(image_base64)
        img = Image.open(io.BytesIO(img_data))

        # OCR text extract
        text = pytesseract.image_to_string(img)

        if not text.strip():
            return "Error: No text detected in the image."

        # Rows split (simple approach - whitespace based)
        rows = [line.split() for line in text.splitlines() if line.strip()]

        # Excel file create
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Extracted Data"

        for row in rows:
            ws.append(row)

        # Output folder
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_filename)
        wb.save(output_path)

        return f"Success! Excel file created at: {output_path} ({len(rows)} rows extracted)"

    except Exception as e:
        return f"Error processing image: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")