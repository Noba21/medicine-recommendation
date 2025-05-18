from werkzeug.security import generate_password_hash, check_password_hash

pswed = "medical123"

hashed = generate_password_hash(pswed)

print(hashed)