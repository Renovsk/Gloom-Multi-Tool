import random, string, requests
import Gloom

code = "".join(random.choices(string.digits+string.ascii_letters, k=16))
r = requests.get(f"https://discord.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true",timeout=10)
if r.status_code in list(range(200,300)):
    print(f"discord.gift/{code} is valid fr")
    Gloom.main()