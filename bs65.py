import base64

with open("logo.png", "rb") as f:
    base64_data = base64.b64encode(f.read()).decode()

with open("logo_base64.txt", "w", encoding="utf-8") as f:
    f.write(base64_data)

print("Base64 saved to logo_base64.txt")