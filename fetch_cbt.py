import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_cbt():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'id,en-US;q=0.9,en;q=0.8',
    })

    # Step 1: Visit main book details page
    url_details = 'https://cbt.erlanggaonline.co.id/book/details/0054200490.0094'
    print(f"Fetching {url_details}...")
    r1 = session.get(url_details)
    print(f"Details page status: {r1.status_code}")

    # Step 2: Post login credentials to save_data
    save_url = 'https://cbt.erlanggaonline.co.id/book/save_data'
    payload = {
        'ci_csrf_token': '',
        'id_cbt': '0054200490.0094',
        'adminusers_level_id': '29',
        'username': 'Al Farel S',
        'email': 'rellnigenk999@gmail.com',
        'password': 'erlonline'
    }
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': url_details
    }
    print(f"Submitting credentials to {save_url}...")
    r2 = session.post(save_url, data=payload, headers=headers)
    print(f"Login response status: {r2.status_code}, response: {r2.text[:200]}")

    # Check redirect URL or response
    res_json = {}
    try:
        res_json = r2.json()
    except Exception:
        pass

    redirect_url = res_json.get('url') or res_json.get('redirect')
    print(f"Redirect URL: {redirect_url}")

    # If redirect url is provided, follow it; otherwise try standard start or pembahasan url
    target_url = redirect_url if redirect_url else 'https://cbt.erlanggaonline.co.id/book/details/0054200490.0094'
    r3 = session.get(target_url)
    print(f"Page content length: {len(r3.text)}")

    # Let's search for nav_data in script tags
    soup = BeautifulSoup(r3.text, 'html.parser')
    scripts = soup.find_all('script')
    nav_data_str = None
    for s in scripts:
        if s.string and 'nav_data' in s.string:
            m = re.search(r'var\s+nav_data\s*=\s*(\[.*?\]);', s.string, re.DOTALL)
            if m:
                nav_data_str = m.group(1)
                break

    if not nav_data_str:
        print("Looking for other pages or session test links...")
        # Check links on page
        for a in soup.find_all('a'):
            href = a.get('href', '')
            if 'pembahasan' in href or 'start' in href or 'cbt' in href:
                print(f"Found link: {href} ({a.text.strip()})")
                r_link = session.get(href)
                soup_sub = BeautifulSoup(r_link.text, 'html.parser')
                for s in soup_sub.find_all('script'):
                    if s.string and 'nav_data' in s.string:
                        m = re.search(r'var\s+nav_data\s*=\s*(\[.*?\]);', s.string, re.DOTALL)
                        if m:
                            nav_data_str = m.group(1)
                            print(f"Found nav_data in link {href}!")
                            break
                if nav_data_str:
                    break

    all_questions = []
    if nav_data_str:
        nav_data = json.loads(nav_data_str)
        print(f"Found {len(nav_data)} questions in nav_data!")
        
        get_q_url = 'https://cbt.erlanggaonline.co.id/book/get_question/'
        for idx, item in enumerate(nav_data):
            try:
                res_q = session.post(get_q_url, data={'data': item}, headers={'X-Requested-With': 'XMLHttpRequest'})
                q_data = res_q.json()
                all_questions.append(q_data)
                print(f"Fetched question {idx+1}/{len(nav_data)}")
            except Exception as e:
                print(f"Error fetching question {idx+1}: {e}")

        with open('cbt_raw_questions.json', 'w', encoding='utf-8') as f:
            json.dump(all_questions, f, ensure_ascii=False, indent=2)
        print("Successfully saved cbt_raw_questions.json!")
    else:
        print("Could not find nav_data automatically, writing debug HTML...")
        with open('debug_page.html', 'w', encoding='utf-8') as f:
            f.write(r3.text)

if __name__ == '__main__':
    scrape_cbt()
