import subprocess

result = subprocess.run(
    ["git", "config", "user.name"],
    capture_output=True, text=True
)
name = result.stdout.strip()

result = subprocess.run(
    ["git", "config", "user.email"],
    capture_output=True, text=True
)
email = result.stdout.strip()

print(f"Active git account: {name} <{email}>")