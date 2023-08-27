from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization

from pathlib import Path

def generate_ssh_key(username, comment="", new_priv_key=True):
    base_dir = Path.home() / ".gator"
    base_dir.mkdir(exist_ok=True) 

    priv_key_file = base_dir / "private_key.pem"
    pub_key_file = base_dir / "public_key.pub"

    if new_priv_key or not priv_key_file.exists():
        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=2048
        )

        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption()
        ).decode('utf-8')

        with priv_key_file.open('w') as file:
            file.write(private_key)
    else:
        with priv_key_file.open('r') as file:
            private_key = file.read()
        
        key = serialization.load_pem_private_key(
            private_key.encode(),
            password=None,
            backend=crypto_default_backend()
        )

    public_key_data = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    ).decode('utf-8')

    formatted_public_key = f"{public_key_data} {comment}"

    # formatted_public_key = f"{username}:{public_key_data} {comment}"
    save_public_key = f"{public_key_data} {comment}"
    # Save the public key
    with pub_key_file.open('w') as file:
        file.write(save_public_key)

    return private_key, formatted_public_key, str(priv_key_file)
