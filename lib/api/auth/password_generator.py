from string import ascii_letters, digits, punctuation
import secrets

def generate_password():
    # Combine all character sets
    all_characters = ascii_letters + digits + punctuation
    
    # Generate password
    password = ''.join(secrets.choice(all_characters) for _ in range(8))
    
    # Ensure at least one character from each category
    password_list = list(password)
    if not any(c.isalpha() for c in password_list):
        password_list.append(secrets.choice(ascii_letters))
    if not any(c.isdigit() for c in password_list):
        password_list.append(secrets.choice(digits))
    if not any(c in punctuation for c in password_list):
        password_list.append(secrets.choice(punctuation))
    
    # Shuffle list to ensure randomness
    secrets.SystemRandom().shuffle(password_list)
    
    # Join back into string
    password = ''.join(password_list)
    
    return password
