import threading
import requests
import uuid
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor

# Configuration
BASE_URL = "https://ainewsworld.ai/api/subscribe"
NUM_THREADS = 500
ORIGINAL_TOKEN = "0f090f9a-629a-4401-aa36-65465a3efa64"
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Common email domains
EMAIL_DOMAINS = [
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "outlook.com",
    "icloud.com",
    "protonmail.com",
    "aol.com",
    "mail.com",
    "zoho.com",
    "gmx.com"
]

# Headers from the curl command
HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://ainewsworld.ai",
    "priority": "u=1, i",
    "referer": "https://ainewsworld.ai/",
    "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
}

COOKIES = {
    "_ga": "GA1.1.1576102486.1779255515",
    "_ga_HX1QYDFKDM": "GS2.1.s1779255514$o1$g1$t1779255527$j47$l0$h0"
}


def generate_random_email():
    """Generate a random realistic email address."""
    # Generate random username (6-12 characters)
    username_length = random.randint(6, 12)
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
    
    # Add random numbers to make it look more realistic
    username += str(random.randint(100, 999))
    
    # Select random domain
    domain = random.choice(EMAIL_DOMAINS)
    
    return f"{username}@{domain}"


def generate_unique_token():
    """Generate a unique UUID token in the same format as the original."""
    return str(uuid.uuid4())


def perform_get_request(thread_id):
    """Perform GET request with unique token with retry logic."""
    unique_token = generate_unique_token()
    url = f"{BASE_URL}?token={unique_token}"
    
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=HEADERS, cookies=COOKIES, timeout=10)
            
            if response.status_code == 503:
                if attempt < MAX_RETRIES:
                    wait_time = RETRY_DELAY * (2 ** attempt)
                    print(f"Thread {thread_id} - GET - Token: {unique_token} - Status: 503 - Retrying in {wait_time}s (attempt {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"Thread {thread_id} - GET - Token: {unique_token} - Status: 503 - Max retries exceeded")
                    return 503
            
            print(f"Thread {thread_id} - GET - Token: {unique_token} - Status: {response.status_code}")
            return response.status_code
        except Exception as e:
            if attempt < MAX_RETRIES:
                wait_time = RETRY_DELAY * (2 ** attempt)
                print(f"Thread {thread_id} - GET Error: {str(e)} - Retrying in {wait_time}s (attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(wait_time)
                continue
            else:
                print(f"Thread {thread_id} - GET Error: {str(e)} - Max retries exceeded")
                return None


def perform_post_request(thread_id):
    """Perform POST request with random email with retry logic."""
    email = generate_random_email()
    payload = {"email": email}
    
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = requests.post(
                BASE_URL,
                headers=HEADERS,
                cookies=COOKIES,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 503:
                if attempt < MAX_RETRIES:
                    wait_time = RETRY_DELAY * (2 ** attempt)
                    print(f"Thread {thread_id} - POST - Email: {email} - Status: 503 - Retrying in {wait_time}s (attempt {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"Thread {thread_id} - POST - Email: {email} - Status: 503 - Max retries exceeded")
                    return 503
            
            print(f"Thread {thread_id} - POST - Email: {email} - Status: {response.status_code}")
            return response.status_code
        except Exception as e:
            if attempt < MAX_RETRIES:
                wait_time = RETRY_DELAY * (2 ** attempt)
                print(f"Thread {thread_id} - POST Error: {str(e)} - Retrying in {wait_time}s (attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(wait_time)
                continue
            else:
                print(f"Thread {thread_id} - POST Error: {str(e)} - Max retries exceeded")
                return None


def perform_combined_request(thread_id):
    """Perform both GET and POST requests in a single thread with retry logic."""
    # GET request with unique token
    unique_token = generate_unique_token()
    get_url = f"{BASE_URL}?token={unique_token}"
    get_status = None
    
    for attempt in range(MAX_RETRIES + 1):
        try:
            get_response = requests.get(get_url, headers=HEADERS, cookies=COOKIES, timeout=10)
            
            if get_response.status_code == 503:
                if attempt < MAX_RETRIES:
                    wait_time = RETRY_DELAY * (2 ** attempt)
                    print(f"Thread {thread_id} - GET - Token: {unique_token} - Status: 503 - Retrying in {wait_time}s (attempt {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"Thread {thread_id} - GET - Token: {unique_token} - Status: 503 - Max retries exceeded")
                    get_status = 503
                    break
            
            print(f"Thread {thread_id} - GET - Token: {unique_token} - Status: {get_response.status_code}")
            get_status = get_response.status_code
            break
        except Exception as e:
            if attempt < MAX_RETRIES:
                wait_time = RETRY_DELAY * (2 ** attempt)
                print(f"Thread {thread_id} - GET Error: {str(e)} - Retrying in {wait_time}s (attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(wait_time)
                continue
            else:
                print(f"Thread {thread_id} - GET Error: {str(e)} - Max retries exceeded")
                get_status = None
                break
    
    # Small delay between requests
    time.sleep(random.uniform(0.1, 0.5))
    
    # POST request with random email
    email = generate_random_email()
    payload = {"email": email}
    post_status = None
    
    for attempt in range(MAX_RETRIES + 1):
        try:
            post_response = requests.post(
                BASE_URL,
                headers=HEADERS,
                cookies=COOKIES,
                json=payload,
                timeout=10
            )
            
            if post_response.status_code == 503:
                if attempt < MAX_RETRIES:
                    wait_time = RETRY_DELAY * (2 ** attempt)
                    print(f"Thread {thread_id} - POST - Email: {email} - Status: 503 - Retrying in {wait_time}s (attempt {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"Thread {thread_id} - POST - Email: {email} - Status: 503 - Max retries exceeded")
                    post_status = 503
                    break
            
            print(f"Thread {thread_id} - POST - Email: {email} - Status: {post_response.status_code}")
            post_status = post_response.status_code
            break
        except Exception as e:
            if attempt < MAX_RETRIES:
                wait_time = RETRY_DELAY * (2 ** attempt)
                print(f"Thread {thread_id} - POST Error: {str(e)} - Retrying in {wait_time}s (attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(wait_time)
                continue
            else:
                print(f"Thread {thread_id} - POST Error: {str(e)} - Max retries exceeded")
                post_status = None
                break
    
    return {
        "get_status": get_status,
        "post_status": post_status
    }


def run_load_test(mode="combined"):
    """Run load test with 500 threads."""
    print(f"Starting load test with {NUM_THREADS} threads...")
    print(f"Mode: {mode}")
    print("-" * 80)
    
    start_time = time.time()
    
    if mode == "get":
        # Run only GET requests
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            futures = [executor.submit(perform_get_request, i) for i in range(NUM_THREADS)]
            results = [future.result() for future in futures]
    
    elif mode == "post":
        # Run only POST requests
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            futures = [executor.submit(perform_post_request, i) for i in range(NUM_THREADS)]
            results = [future.result() for future in futures]
    
    else:  # combined mode (default)
        # Run both GET and POST requests
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            futures = [executor.submit(perform_combined_request, i) for i in range(NUM_THREADS)]
            results = [future.result() for future in futures]
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("-" * 80)
    print(f"Load test completed in {duration:.2f} seconds")
    print(f"Total threads: {NUM_THREADS}")
    print(f"Requests per second: {NUM_THREADS / duration:.2f}")


if __name__ == "__main__":
    # You can change the mode to "get", "post", or "combined"
    # combined: runs both GET and POST requests in each thread
    # get: runs only GET requests
    # post: runs only POST requests
    
    mode = "combined"  # Change this to "get" or "post" as needed
    
    run_load_test(mode=mode)
