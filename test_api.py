#!/usr/bin/env python3
"""
Quick script to test all API endpoints locally.
Run this after starting the Django server.
"""

import requests
import json

BASE_URL = "http://localhost:8000/dadjokes"

def test_endpoint(url, method="GET", data=None):
    """Test an API endpoint and print the result."""
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        
        print(f"\n{'='*60}")
        print(f"Testing: {method} {url}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200 or response.status_code == 201:
            try:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
                return True
            except:
                print(f"Response: {response.text[:200]}")
                return True
        else:
            print(f"Error: {response.text[:200]}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"\n{'='*60}")
        print(f"ERROR: Could not connect to {url}")
        print("Make sure Django server is running on port 8000")
        return False
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"ERROR: {str(e)}")
        return False

def main():
    print("Testing Dad Jokes API Endpoints")
    print("="*60)
    
    results = []
    
    # Test GET endpoints
    results.append(("GET /api/", test_endpoint(f"{BASE_URL}/api/")))
    results.append(("GET /api/random", test_endpoint(f"{BASE_URL}/api/random")))
    results.append(("GET /api/random_picture", test_endpoint(f"{BASE_URL}/api/random_picture")))
    results.append(("GET /api/jokes", test_endpoint(f"{BASE_URL}/api/jokes")))
    results.append(("GET /api/pictures", test_endpoint(f"{BASE_URL}/api/pictures")))
    
    # Test detail endpoints (assuming ID 1 exists)
    results.append(("GET /api/joke/1", test_endpoint(f"{BASE_URL}/api/joke/1")))
    results.append(("GET /api/picture/1", test_endpoint(f"{BASE_URL}/api/picture/1")))
    
    # Test POST endpoint
    test_joke = {
        "text": "Why did the test script cross the road? To test the API!",
        "contributor": "Test Script"
    }
    results.append(("POST /api/jokes", test_endpoint(f"{BASE_URL}/api/jokes", method="POST", data=test_joke)))
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print("="*60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("ERROR: requests library not installed.")
        print("Install it with: pip install requests")
        exit(1)
    
    success = main()
    exit(0 if success else 1)

