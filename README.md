# Aikopilot
## A Post-processor for Aiko (or any other whisper based dictation tool)

This script can be used to processes input text with some static filters and uses LLMs to correct typos, 
remove common whisper hallucinations, and apply specific flags for text manipulation.

## Features

- Removes common hallucinations from the input text
- Clears newlines from short transcripts
- Extracts and applies flags for additional processing
- Uses OpenAI API to correct typos and apply grammar fixes

## Requirements

- Python 3.x
- OpenAI Python library

## Setup

1. Install the required library:
   ```
   pip install openai
   ```

2. Set up the OpenAI client in the script:
   - Ensure you have access to a local OpenAI-compatible API endpoint
   - Update the `base_url` and `api_key` in the script if necessary

## Usage

Run the script and provide input text via stdin:

```
python processor.py < input.txt
```

Or pipe input directly:

```
echo "Your input text here fix grammar" | python processor.py
```

## Flags

You can include flags in the input text to apply specific processing:

- `fix grammar`: Applies grammar fixes to the input text

## Customization

- Modify the `replacements` dictionary to add or remove common hallucinations
- Add new flags in the `flags` and `flag_prompt` dictionaries to extend functionality

## Note

This script uses a local OpenAI-compatible API endpoint. Ensure the endpoint is running and accessible before using the script.
```
