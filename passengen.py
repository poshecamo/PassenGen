#!/usr/bin/env python3
"""
PassenGen - Secure Password Generator

A command-line based tool designed to generate cryptographically secure passwords
locally, without relying on any external services.
"""

import secrets
import string
import argparse
import sys
import datetime

from cryptography.fernet import Fernet

try:
    from colorama import init, Fore, Style
    COLORAMA_AVAILABLE = True
    init()  # Initialize colorama
except ImportError:
    COLORAMA_AVAILABLE = False


def get_logo():
    return r"""
  _____                           _____            
 |  __ \                        / ____|           
 | |__) |_ _ ___ ___  ___ _ __ | |  __  ___ _ __  
 |  ___/ _` / __/ __|/ _ \ '_ \| | |_ |/ _ \ '_ \ 
 | |  | (_| \__ \__ \  __/ | | | |__| |  __/ | | |
 |_|   \__,_|___/___/\___|_| |_|\_____|\___|_| |_|
                                                  
       .--.
      |o_o |    Secure Password Generator
      |:_/ |    
     //   \ \   
    (|     | )  
   /'\_   _/`\  
   \___) (___/  
       """

def get_small_logo():
    return "PassenGen - Secure Passwords"

def print_logo(small=False):
    logo = get_small_logo() if small else get_logo()
    print_colored(logo, "cyan", bold=True)

def interactive_options():
    """Ask the user for password generation options interactively."""
    try:
        length = int(input("Enter password length (minimum 12): "))
        if length < MIN_PASSWORD_LENGTH:
            print_colored(f"Password length must be at least {MIN_PASSWORD_LENGTH}.", "red", bold=True)
            sys.exit(1)
    except ValueError:
        print_colored("Invalid length input. Must be an integer.", "red", bold=True)
        sys.exit(1)

    specials = input("Include special characters? (y/n): ").lower() == 'y'
    digits = input("Include digits? (y/n): ").lower() == 'y'
    uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
    lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'

    force_word = input("Do you want to force a word inside your password? (Leave blank if no): ")

    if not any([specials, digits, uppercase, lowercase]):
        print_colored("At least one character set must be enabled.", "red", bold=True)
        sys.exit(1)

    return {
        'length': length,
        'use_specials': specials,
        'use_digits': digits,
        'use_uppercase': uppercase,
        'use_lowercase': lowercase,
        'force_word': force_word.strip()
    }

# Constants
MIN_PASSWORD_LENGTH = 12
DEFAULT_PASSWORD_LENGTH = 16


def generate_password(length=DEFAULT_PASSWORD_LENGTH, use_specials=True, 
                      use_digits=True, use_uppercase=True, use_lowercase=True,
                      force_word=""):
    """
    Generate a cryptographically secure password using the secrets module.
    
    Args:
        length (int): Length of the password (minimum 12)
        use_specials (bool): Include special characters
        use_digits (bool): Include digits
        use_uppercase (bool): Include uppercase letters
        use_lowercase (bool): Include lowercase letters
        force_word (str): A word to forcefully include inside the password
        
    Returns:
        str: Generated password
    """
    # Validate that at least one character set is selected
    if not any([use_specials, use_digits, use_uppercase, use_lowercase]):
        raise ValueError("At least one character set must be enabled")
    
    # Build the alphabet based on selected options
    alphabet = ""
    if use_lowercase:
        alphabet += string.ascii_lowercase
    if use_uppercase:
        alphabet += string.ascii_uppercase
    if use_digits:
        alphabet += string.digits
    if use_specials:
        alphabet += string.punctuation
    
    # Generate the password
    if force_word:
        if len(force_word) > length:
            raise ValueError("Forced word cannot be longer than password length.")
        base_length = length - len(force_word)
        password = ''.join(secrets.choice(alphabet) for _ in range(base_length))
        insert_pos = secrets.randbelow(len(password) + 1)
        password = password[:insert_pos] + force_word + password[insert_pos:]
    else:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
    
    return password

def get_rotation_recommendation():
    created_at = datetime.datetime.now()
    rotate_after_days = 90
    next_rotation = created_at + datetime.timedelta(days=rotate_after_days)
    return created_at.strftime("%Y-%m-%d"), next_rotation.strftime("%Y-%m-%d")

def print_colored(text, color=None, bold=False):
    """Print colored text if colorama is available."""
    if COLORAMA_AVAILABLE and color:
        color_code = getattr(Fore, color.upper(), "")
        style_code = Style.BRIGHT if bold else ""
        print(f"{style_code}{color_code}{text}{Style.RESET_ALL}")
    else:
        print(text)

def evaluate_password_strength(password):
    length = len(password)
    categories = sum([
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in string.punctuation for c in password)
    ])
    if length >= 16 and categories == 4:
        return "Very Strong 💪"
    elif length >= 12 and categories >= 3:
        return "Strong 🔥"
    elif length >= 8 and categories >= 2:
        return "Moderate ⚡"
    else:
        return "Weak ⚠️"

def save_password_encrypted(password, filepath="saved_passwords.enc"):
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted = cipher.encrypt(password.encode())
    with open(filepath, "wb") as file:
        file.write(encrypted)
    with open(filepath + ".key", "wb") as keyfile:
        keyfile.write(key)
    print_colored(f"Password encrypted and saved to {filepath}", "cyan")
    print_colored(f"Encryption key saved to {filepath}.key (Keep it safe!)", "cyan")


def main():
    """Main function to handle CLI arguments and generate passwords."""
    print_logo()
    parser = argparse.ArgumentParser(
        description="PassenGen - Secure Password Generator",
        epilog="Generates cryptographically secure passwords locally."
    )
    
    parser.add_argument(
        '-l', '--length', 
        type=int, 
        default=DEFAULT_PASSWORD_LENGTH,
        help=f'Length of the password (minimum {MIN_PASSWORD_LENGTH}, default {DEFAULT_PASSWORD_LENGTH})'
    )
    
    parser.add_argument(
        '-ns', '--no-specials', 
        action='store_true', 
        help='Exclude special characters'
    )
    
    parser.add_argument(
        '-nd', '--no-digits', 
        action='store_true', 
        help='Exclude digits'
    )
    
    parser.add_argument(
        '-nl', '--no-lowercase', 
        action='store_true', 
        help='Exclude lowercase letters'
    )
    
    parser.add_argument(
        '-nu', '--no-uppercase', 
        action='store_true', 
        help='Exclude uppercase letters'
    )
    
    parser.add_argument(
        '-c', '--count', 
        type=int, 
        default=1,
        help='Number of passwords to generate (default: 1)'
    )
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        options = interactive_options()

        password = generate_password(
            length=options['length'],
            use_specials=options['use_specials'],
            use_digits=options['use_digits'],
            use_uppercase=options['use_uppercase'],
            use_lowercase=options['use_lowercase'],
            force_word=options['force_word']
        )

        print_colored("\nGenerated Password:", "yellow")
        print_colored(password, "green", bold=True)
        print_colored("\nPassword Strength: " + evaluate_password_strength(password), "magenta")

        created_at, next_rotation = get_rotation_recommendation()
        print_colored(f"\nPassword Created On: {created_at}", "blue")
        print_colored(f"Recommended Rotation By: {next_rotation}", "blue")

        save_choice = input("\nDo you want to save this password encrypted locally? (y/n): ").lower()
        if save_choice == 'y':
            save_password_encrypted(password)

        print("\nPassword generated using cryptographically secure methods.")
        print("This tool operates completely offline for your security.")
        sys.exit(0)
    
    # Validate password length
    if args.length < MIN_PASSWORD_LENGTH:
        print_colored(
            f"Error: Password length must be at least {MIN_PASSWORD_LENGTH} characters.", 
            "red", 
            bold=True
        )
        sys.exit(1)
    
    # Validate that at least one character set is enabled
    if args.no_specials and args.no_digits and args.no_lowercase and args.no_uppercase:
        print_colored(
            "Error: At least one character set must be enabled.", 
            "red", 
            bold=True
        )
        sys.exit(1)
    
    try:
        print_colored("PassenGen - Secure Password Generator", "cyan", bold=True)
        print_colored("=" * 40, "cyan")
        
        for i in range(args.count):
            password = generate_password(
                length=args.length,
                use_specials=not args.no_specials,
                use_digits=not args.no_digits,
                use_uppercase=not args.no_uppercase,
                use_lowercase=not args.no_lowercase
            )
            
            if args.count > 1:
                print_colored(f"\nPassword #{i+1}:", "yellow")
            else:
                print_colored("\nGenerated Password:", "yellow")
                
            print_colored(password, "green", bold=True)
            print_colored("Password Strength: " + evaluate_password_strength(password), "magenta")

            created_at, next_rotation = get_rotation_recommendation()
            print_colored(f"\nPassword Created On: {created_at}", "blue")
            print_colored(f"Recommended Rotation By: {next_rotation}", "blue")

            save_choice = input("\nDo you want to save this password encrypted locally? (y/n): ").lower()
            if save_choice == 'y':
                save_password_encrypted(password)
        
        print("\nPassword generated using cryptographically secure methods.")
        print("This tool operates completely offline for your security.")
        
    except Exception as e:
        print_colored(f"\nError: {str(e)}", "red", bold=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
