import sys
from openai import  OpenAI

## Configs
# Texts shorter than this will be returned as a single line
SINGLE_LINE_THRESHOLD = 250

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="your-api-key-here"
)

replacements = {
    "\nThank you!": "",
    "\nThanks.": "",
    "\nBye!": "",
    "\nBye": "",
    "\nI'm going to go to sleep.": "",
    "\nThanks for watching": "",
    "\nBye.": "",
    "\nEnjoy.": "",
    "\nThank you.": "",
    "\nThank you for watching": ""
}
flags = {
    "fix grammar": "fix_grammar",
    "do not fix, no AI processing": "no_ai_processing",
    "no post processing, raw text": "no_post_processing"
}

flag_prompt = {
    "fix_grammar": "Fix grammar errors in the input text."
}


def extract_flags(input_text):
    flags_found = []
    text = input_text.strip().lower().replace(",", "").replace(".", "").replace("?", "").replace("-", "")
    for flag_text, flag in flags.items():
        for flag_word in flag_text.split(","):
            if flag_word.strip() in text:
                flags_found.append(flag)
                input_text = input_text.replace(flag_word.strip(), "")
    return flags_found, input_text


def remove_common_hallucinations(text):
    for key in replacements:
        text = text.replace(key, replacements[key])
    return text


def clear_newlines_from_short_transcript(input_text):
    if input_text.count("\n") > SINGLE_LINE_THRESHOLD:
        return input_text
    return input_text.replace("\n", " ")


def process_with_ai(input_text, flags):
    if "no_ai_processing" in flags:
        return input_text
    # call openai api to fix possible typos
    prompt = ("Following text output of dictation, most likely in the context of programming."
              "Correct possible typos or out of context hallucinations that might be added to end of the text"
              "Do not output anything else. \nInput: ") + input_text
    for flag in flags:
        if flag in flag_prompt:
            prompt += f"\n{flag_prompt[flag]}"
    try:
        response = client.chat.completions.create(
            model="mistral-nemo-instruct-2407",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that corrects typos in dictation output."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for more deterministic outputs
            max_tokens=4000
        )

        corrected_text = response.choices[0].message.content.strip()
        return corrected_text
    except Exception as e:
        print(f"Error in AI processing: {str(e)}", file=sys.stderr)
        return input_text  # Return original text if there's an error


def process_text(input_text):
    flags, processed_text = extract_flags(input_text)
    if "no_post_processing" in flags:
        return processed_text
    processed_text = remove_common_hallucinations(input_text)
    processed_text = clear_newlines_from_short_transcript(processed_text)
    processed_text = process_with_ai(processed_text, flags)
    return processed_text


if __name__ == "__main__":
    # Read input from stdin
    input_text = sys.stdin.read().strip()

    # Process the text
    output_text = process_text(input_text)

    # Print the output
    print(output_text)
