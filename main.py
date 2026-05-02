import requests
import re
import json
import random
import time
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import os

# Initialize colorama for Windows
init(autoreset=True)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Apple) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 14; Mobile; rv:124.0) Gecko/124.0 Firefox/124.0"
]

def get_random_headers():
    ua = random.choice(USER_AGENTS)
    return {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://docs.google.com/forms/",
        "DNT": "1", # Do Not Track
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_form_data(url):
    """Fetches form metadata including entry IDs and question types."""
    try:
        # Using a fresh session with no cookies for the initial fetch
        response = requests.get(url, headers=get_random_headers(), timeout=10, cookies={})
        if response.status_code == 404:
            return None, "Error: Form not found (404)."
        if "Sign in to your Google Account" in response.text or "restricted" in response.text.lower():
            return None, "Error: Could not access (account restricted)."
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Google Forms stores metadata in FB_PUBLIC_LOAD_DATA_
        script_tag = soup.find('script', string=re.compile('FB_PUBLIC_LOAD_DATA_'))
        
        if not script_tag:
            return None, "Error: Could not parse form data. Is this a valid Google Form URL?"

        # Extract the JSON data from the script tag
        json_str = re.search(r'FB_PUBLIC_LOAD_DATA_\s*=\s*(.*?);', script_tag.string, re.DOTALL).group(1)
        data = json.loads(json_str)
        
        # data[1][1] contains the list of questions
        questions_raw = data[1][1]
        
        parsed_questions = []
        for q in questions_raw:
            try:
                q_text = q[1]
                q_id = q[4][0][0]
                q_type = q[3] # 0: short text, 1: long text, 2: multiple choice, 3: dropdown, 4: checkboxes, 5: linear scale
                
                options = []
                if q_type in [2, 3, 4]: # MC, Dropdown, Checkbox
                    options = [opt[0] for opt in q[4][0][1]]
                elif q_type == 5: # Linear scale
                    options = list(range(int(q[4][0][3][0]), int(q[4][0][3][1]) + 1))
                
                parsed_questions.append({
                    'text': q_text,
                    'id': f'entry.{q_id}',
                    'type': q_type,
                    'options': options
                })
            except (IndexError, TypeError):
                continue
                
        # Submission URL
        form_id = re.search(r'/forms/d/e/(.*?)/', url).group(1)
        submit_url = f"https://docs.google.com/forms/d/e/{form_id}/formResponse"
        
        return {
            'questions': parsed_questions,
            'submit_url': submit_url
        }, None

    except Exception as e:
        return None, f"Error: {str(e)}"

def load_texts():
    if not os.path.exists("texts.txt"):
        return ["Educational Test"]
    with open("texts.txt", "r", encoding="utf-8") as f:
        content = f.read()
        # Support both comma and newline separation
        parts = [p.strip() for p in content.replace('\n', ',').split(',') if p.strip()]
        return parts

def main():
    clear_screen()
    print(f"{Fore.CYAN}=== Google Form Automation Tool (Educational) ==={Style.RESET_ALL}")
    
    url = input(f"{Fore.YELLOW}Enter the Google Form URL: {Style.RESET_ALL}").strip()
    if not url.startswith("http"):
        print(f"{Fore.RED}Invalid URL. Must start with http/https.{Style.RESET_ALL}")
        return

    print(f"{Fore.BLUE}Fetching form details...{Style.RESET_ALL}")
    form_info, error = get_form_data(url)
    
    if error:
        print(f"{Fore.RED}{error}{Style.RESET_ALL}")
        return

    questions = form_info['questions']
    submit_url = form_info['submit_url']
    
    print(f"{Fore.GREEN}Found {len(questions)} questions.{Style.RESET_ALL}\n")
    
    user_configs = []
    text_pool = load_texts()

    for q in questions:
        print(f"{Fore.WHITE}Q: {q['text']}{Style.RESET_ALL}")
        
        if q['type'] in [0, 1]: # Text
            print("1. Random from texts.txt")
            print("2. Manual static text")
            choice = input("Select option (1/2): ")
            if choice == "2":
                val = input("Enter text: ")
                user_configs.append(('static', val))
            else:
                user_configs.append(('random_text', None))
                
        elif q['type'] in [2, 3, 5]: # MC, Dropdown, Scale
            print("1. Random choice")
            print("2. Manual choice")
            choice = input("Select option (1/2): ")
            if choice == "2":
                for i, opt in enumerate(q['options']):
                    print(f"  {i+1}. {opt}")
                idx = int(input("Select index: ")) - 1
                user_configs.append(('static', q['options'][idx]))
            else:
                user_configs.append(('random_choice', q['options']))
                
        elif q['type'] == 4: # Checkboxes
            print("1. Random (select 1)")
            print("2. Manual selection (comma separated indices)")
            choice = input("Select option (1/2): ")
            if choice == "2":
                for i, opt in enumerate(q['options']):
                    print(f"  {i+1}. {opt}")
                indices = [int(x.strip()) - 1 for x in input("Indices: ").split(',')]
                user_configs.append(('static_list', [q['options'][i] for i in indices]))
            else:
                user_configs.append(('random_choice_list', q['options']))
        else:
            user_configs.append(('skip', None))
        print("-" * 20)

    try:
        count = int(input(f"\n{Fore.YELLOW}How many times to submit? {Style.RESET_ALL}"))
        power = int(input(f"{Fore.YELLOW}Power (1-10, 10 is fastest): {Style.RESET_ALL}"))
    except ValueError:
        print(f"{Fore.RED}Invalid number input.{Style.RESET_ALL}")
        return

    # Calculate delay based on power
    # Power 1: 5s delay, Power 10: 0.1s delay
    delay = max(0.1, 5.0 - (power * 0.49))

    print(f"\n{Fore.CYAN}Starting submissions... Press Ctrl+C to stop.{Style.RESET_ALL}")
    
    success_count = 0
    fail_count = 0

    for i in range(count):
        payload = {}
        for idx, (config_type, config_val) in enumerate(user_configs):
            q_id = questions[idx]['id']
            
            if config_type == 'static':
                payload[q_id] = config_val
            elif config_type == 'static_list':
                payload[q_id] = config_val
            elif config_type == 'random_text':
                payload[q_id] = random.choice(text_pool)
            elif config_type == 'random_choice':
                payload[q_id] = random.choice(config_val)
            elif config_type == 'random_choice_list':
                payload[q_id] = [random.choice(config_val)]

        try:
            # Explicitly clear cookies for every request to ensure zero session linkage
            res = requests.post(submit_url, data=payload, headers=get_random_headers(), timeout=5, cookies={})
            if res.status_code == 200:
                success_count += 1
                print(f"{Fore.GREEN}[{i+1}/{count}] Success{Style.RESET_ALL}")
            else:
                fail_count += 1
                print(f"{Fore.RED}[{i+1}/{count}] Failed (Status: {res.status_code}){Style.RESET_ALL}")
        except Exception as e:
            fail_count += 1
            print(f"{Fore.RED}[{i+1}/{count}] Error: {str(e)}{Style.RESET_ALL}")

        if i < count - 1:
            # Add random jitter to the delay (±20%) to break mathematical patterns
            jitter = delay * random.uniform(0.1, 0.2)
            actual_delay = delay + random.uniform(-jitter, jitter)
            time.sleep(max(0.05, actual_delay))

    print(f"\n{Fore.CYAN}Done! Total: {count} | Success: {success_count} | Failed: {fail_count}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
