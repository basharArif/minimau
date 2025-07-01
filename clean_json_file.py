
import re
import json
from pathlib import Path

json_file_path = Path("/home/arif/leafloat/extracted_content.json")

try:
    # Read the content as a raw string, ignoring decoding errors
    content = json_file_path.read_text(encoding='utf-8', errors='ignore')

    # Remove all non-printable ASCII characters (0x00-0x1f, 0x7f)
    # This regex matches characters in the range U+0000-U+001F (control characters)
    # and also U+007F (DEL). It keeps printable ASCII characters.
    cleaned_content = re.sub(r'[\x00-\x1f\x7f]', '', content)

    # Attempt to load and dump to ensure proper JSON escaping and formatting
    parsed_json = json.loads(cleaned_content)
    final_json_content = json.dumps(parsed_json, indent=2, ensure_ascii=False) # ensure_ascii=False to keep non-ASCII chars as is

    json_file_path.write_text(final_json_content, encoding='utf-8')
    print("Successfully cleaned and re-formatted extracted_content.json")
except Exception as e:
    print(f"Error cleaning JSON file: {e}")
