# PassenGen - Secure Password Generator

PassenGen is a command-line based tool written in Python designed to generate cryptographically secure passwords locally, without relying on any external services. It is lightweight, secure by design, customizable, and now supports both CLI arguments and interactive mode.

## Features

- **Cryptographically secure** randomness using Python's `secrets` module
- **Configurable password length**, character sets, and optional forced inclusion of specific words
- **Interactive mode** if no CLI arguments are provided
- **Minimum enforced password length** of 12 characters
- **Passphrase generation** mode (random words)
- **Encrypted password saving** locally using symmetric encryption
- **Password strength scoring** after generation
- **Zero network connections**: fully offline and local operation
- **Colorful output** (optional, requires colorama)
- **Docker support** for easy cross-platform execution
- **Auto Password Expiration/Rotation Reminder**: After generating a password, the tool displays the creation date and a recommended date for password rotation (default 90 days), promoting good cybersecurity hygiene.
- **Breached Password Check**: After generating a password, the tool automatically checks against the Have I Been Pwned database to warn if the password has been found in known breaches.

## Security Precautions

- **Randomness Source**: All password generation uses the `secrets` module which is based on operating system entropy, ensuring cryptographic strength.
- **Minimum Length Enforcement**: No passwords shorter than 12 characters are allowed, aligning with NIST and cybersecurity best practices.
- **No Logging**: Generated passwords are not logged, printed unnecessarily, or saved unless explicitly managed by the user.
- **Input Validation**: User inputs (e.g., length) are strictly validated before generation.
- **No Networking**: The tool does not connect to the internet, ensuring zero risk of password leaks.

## Installation

### Clone the Repository

```bash
git clone https://github.com/poshecamo/PassenGen.git
cd passengen
```

### Setup Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Make the Script Executable (Linux/macOS)

```bash
chmod +x passengen.py
```

## Running with Docker

If you prefer not to install Python and dependencies manually, you can run PassenGen using Docker:

1. Build the Docker image:

```bash
docker build -t passengen .
```

2. Run PassenGen inside Docker:

```bash
docker run -it passengen
```

PassenGen will launch inside the container, and you can generate passwords interactively.

## Usage

### Interactive Mode (Recommended)

Simply run:

```bash
python passengen.py
```

You will be prompted interactively for:
- Password length
- Whether to include special characters, digits, uppercase, lowercase
- Optional: Force a specific word to be inserted into the password
- Option to generate a passphrase instead of a random password
- Option to copy the password to clipboard
- Option to save the password encrypted locally
- See password strength score
- View password creation date and recommended rotation date
- Automatic check if the generated password is found in known data breaches (powered by Have I Been Pwned).

### CLI Mode with Arguments

#### Basic Command

```bash
python passengen.py --length 16
```

Generates a secure password with specific settings.

#### Exclude Special Characters

```bash
python passengen.py --no-specials
```

Generates a password without special characters.

#### Generate Multiple Passwords

```bash
python passengen.py --count 5
```

Generates 5 different passwords.

#### Full Example with Multiple Options

```bash
python passengen.py --length 20 --no-specials --no-digits
```

## CLI Options

| Option | Short | Description |
|--------|-------|-------------|
| `--length` | `-l` | Specify password length (minimum enforced to 12) |
| `--no-specials` | `-ns` | Exclude special characters |
| `--no-digits` | `-nd` | Exclude digits |
| `--no-lowercase` | `-nl` | Exclude lowercase letters |
| `--no-uppercase` | `-nu` | Exclude uppercase letters |
| `--count` | `-c` | Number of passwords to generate (default: 1) |
| `--force-word` | (N/A) | Force a specific word to be included in the password |
| `--help` | `-h` | Show help message and exit |

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
