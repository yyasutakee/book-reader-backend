#!/usr/bin/env python3
"""
Simple test script for the spaCy API
"""

import requests
import json

# Test sentences
test_sentences = [
    "The cat sits on the mat",
    "I love reading books",
    "She is running quickly",
    "The beautiful flowers bloom in spring",
    "Dogs are barking loudly"
]

def test_api(base_url="http://localhost:8000"):
    print(f"Testing API at {base_url}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test root finding for each sentence
    for sentence in test_sentences:
        try:
            response = requests.post(
                f"{base_url}/find-root",
                json={"sentence": sentence}
            )
            result = response.json()
            print(f"📝 '{sentence}'")
            print(f"   Root: '{result['root_word']}' ({result['root_pos']})")
            print()
        except Exception as e:
            print(f"❌ Error with '{sentence}': {e}")

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    test_api(url)