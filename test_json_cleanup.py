#!/usr/bin/env python3
"""
Quick test to verify JSON cleanup logic works correctly
"""

import json

def clean_json_response(response_text):
    """Clean up response text - remove markdown code blocks if present"""
    response_text = response_text.strip()
    if response_text.startswith('```'):
        # Remove opening code block (```json or ```)
        lines = response_text.split('\n')
        if lines[0].startswith('```'):
            lines = lines[1:]
        # Remove closing code block (```)
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]
        response_text = '\n'.join(lines).strip()
    return response_text


# Test cases
test_cases = [
    # Case 1: JSON with markdown code blocks (the error case)
    (
        '''```json
{
  "category": "HAZARDOUS",
  "confidence": "high",
  "reasoning": "Electronic waste",
  "items_detected": ["smartphone"]
}
```''',
        "JSON with markdown code blocks"
    ),
    # Case 2: Plain JSON (ideal case)
    (
        '''{
  "category": "ORGANIC",
  "confidence": "medium",
  "reasoning": "Food waste",
  "items_detected": ["apple"]
}''',
        "Plain JSON without code blocks"
    ),
    # Case 3: Code block without json tag
    (
        '''```
{
  "category": "INORGANIC",
  "confidence": "low",
  "reasoning": "Plastic",
  "items_detected": ["bottle"]
}
```''',
        "Code block without json tag"
    ),
]

print("Testing JSON cleanup logic...\n")
print("=" * 60)

all_passed = True
for i, (test_input, description) in enumerate(test_cases, 1):
    print(f"\nTest {i}: {description}")
    print("-" * 60)

    try:
        cleaned = clean_json_response(test_input)
        parsed = json.loads(cleaned)

        print(f"✓ Successfully cleaned and parsed")
        print(f"  Category: {parsed['category']}")
        print(f"  Confidence: {parsed['confidence']}")

    except json.JSONDecodeError as e:
        print(f"✗ FAILED: JSON parsing error")
        print(f"  Error: {e}")
        print(f"  Cleaned text: {repr(cleaned)}")
        all_passed = False
    except Exception as e:
        print(f"✗ FAILED: {e}")
        all_passed = False

print("\n" + "=" * 60)
if all_passed:
    print("✓ All tests passed!")
else:
    print("✗ Some tests failed")
