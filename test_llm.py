import requests
import time
import sys

def test_rfp_processing():
    print("Waiting for server to start...")
    time.sleep(5) # Give the server a moment to start
    
    url = "http://localhost:8000/process-rfp"
    payload = {"rfp_id": "RFP-2024-001"}
    
    try:
        print(f"Sending request to {url}...")
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("\nSUCCESS! Bid generated.")
                print(f"Confidence: {data['bid']['confidence']}%")
                print(f"Reasoning: {data['bid'].get('reasoning', 'No reasoning found')}")
                return True
            else:
                print("\nFAILED. Application returned success=False.")
                return False
        else:
            print(f"\nFAILED. Status Code: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"\nEXCEPTION: {e}")
        return False

if __name__ == "__main__":
    success = test_rfp_processing()
    sys.exit(0 if success else 1)
