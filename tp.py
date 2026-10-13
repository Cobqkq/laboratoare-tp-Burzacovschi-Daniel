import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]

def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    url= (host + (path if path[0] == "/" else f"{path}"))
    return url
print(build_url("example.com","login"))
print(build_url("example.com","/login"))


def is_https(url,r):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    if "https" == url[:5]:
        r = True
    else:
        r = False
    return r
print(is_https("https://example.com"))
print(is_https("https://httpbin.org/html"))

def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    r = requests.get(url)
    return r.status_code
    return r.json.content
print(show_response("https://example.com"))

    


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""        
    response = requests.get(url, timeout=5)        
    status = response.status_code
        
    content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
    if not content_type:
        content_type = None
            
        
        length = len(response.content)
         
        server = response.headers.get("Server", "unknown")
        
        return {
            "status": status,
        "content_type": content_type,
            "length": length,
            "server": server
        }
        



def scan_sites(url,timeout=10,):
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    list = []
    r2 = requests.get(url,timeout)
    for site in SITES:
        if r2.ok == 200:
        list.append
    return list

        

def check_headers(url):
    present = []
    missing = []

    SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options"
]
    
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers
        
        for header in SECURITY_HEADERS:
            found = any(h.lower() == header.lower() for h in headers.keys())
            if found:
                present.append(header)
            else:
                missing.append(header)
                
    except requests.RequestException:
        missing = list(SECURITY_HEADERS)
    score = int((len(present) / len(SECURITY_HEADERS)) * 100)
    
    return {
        "present": present,
        "missing": missing,
        "score": score
    }

def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    last_status = None
    last_error = None
    made_attempts = 0
    
    for _ in range(attempts):
        made_attempts += 1
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code
            last_error = None             
            if last_status < 500:
                break
                
        except requests.RequestException as e:
            last_status = None
            last_error = str(e)
    result = {
        "status": last_status,
        "attempts": made_attempts
    }
    
    if last_error is not None:
        result["error"] = last_error
        
    return result