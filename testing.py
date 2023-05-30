def load():
    global proxies
    with open("./proxies.txt", 'r') as file:
            proxies = file.readlines()
    if not proxies:
        proxies = None
    proxies = [proxy.strip() for proxy in proxies]
    
    

def proxy():
    global proxies
    if proxies is None:
        return None

    proxy_iter = iter(proxies)
    while True:
        try:
            t = next(proxy_iter)
            yield {'http': f'http://{t}', 'https': f'https://{t}'}
        except StopIteration:
            proxy_iter = iter(proxies)
            
            
load()

for _ in range(10):
    print(next(proxy()))