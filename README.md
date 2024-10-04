
### Network Automation ZTP Script

```markdown

This script automates the **Zero-Touch Provisioning (ZTP)** of network devices (switches and routers), allowing them to fetch, download, and apply their configurations automatically via **TFTP** and a remote **API**. It ensures that new network devices can join the network with minimal intervention from network administrators.

## Part 1: Environment Setup and Configuration Fetching

### 1. Secure Decryption of Environment Variables

Before the network devices can fetch their configuration data from the API, the script securely decrypts environment variables such as **API tokens** and the **TFTP server IP**. The variables are stored in an encrypted format using **Fernet encryption**, and the script decrypts these variables at runtime.

#### Key Files:
- `secret.key`: Stores the encryption key for decrypting the environment variables.
- `encrypted_env.bin`: Contains the encrypted environment variables such as the API token and TFTP server IP.

#### Decrypting Environment Variables:

The script starts by loading the encryption key from `secret.key` and decrypting the contents of `encrypted_env.bin`. This step ensures that the sensitive environment variables are securely stored and only decrypted when needed.

```python
def load_key():
    """
    Load the encryption key from a file.

    Returns:
        bytes: The encryption key used for decryption.
    """
    try:
        key = open("secret.key", "rb").read()
        logging.info("Successfully loaded the encryption key.")
        return key
    except FileNotFoundError:
        logging.error("Encryption key file not found. Ensure 'secret.key' exists.")
        raise
    except Exception as e:
        logging.error(f"Error loading encryption key: {e}")
        raise
```

Once the encryption key is loaded, the script reads and decrypts the environment variables from `encrypted_env.bin`.

```python
def decrypt_env():
    """
    Decrypt the environment file and load the values into environment variables.

    This function reads the encrypted environment file (`encrypted_env.bin`), decrypts it using 
    the encryption key, and sets each decrypted key-value pair as an environment variable.
    """
    try:
        key = load_key()
        fernet = Fernet(key)
        with open("encrypted_env.bin", "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()
        decrypted_data = fernet.decrypt(encrypted_data).decode()

        # Load the decrypted data into environment variables
        for line in decrypted_data.splitlines():
            if line.strip():
                key, value = line.split('=')
                os.environ[key] = value
        logging.info("Environment variables successfully decrypted and loaded.")
    except FileNotFoundError:
        logging.error("Encrypted environment file not found. Ensure 'encrypted_env.bin' exists.")
        raise
    except Exception as e:
        logging.error(f"Error decrypting environment variables: {e}")
        raise
```

### 2. Fetching Configuration Data from the API

Once the environment variables are successfully decrypted and available, the script makes an HTTP GET request to the API to fetch the network configuration data. The API token, which is one of the decrypted environment variables, is used for authentication.

The script sends a **GET request** to the API endpoint and receives a **JSON response** containing the configuration data for the network devices.

```python
def fetch_configuration(api_url):
    """
    Fetch the network configuration from the API using the decrypted environment variables.

    This function makes an HTTP GET request to the given API URL and retrieves the 
    configuration data in JSON format. It uses an API token stored in environment variables 
    for authentication.

    Args:
        api_url (str): The URL of the API to fetch configuration from.

    Returns
        dict: The parsed JSON configuration data if the request is successful, else None.

    Raises:
        Exception: If there is an error during the API request or data retrieval.
    """
    api_token = os.getenv('API_TOKEN')
    if not api_token:
        logging.error("API token not found in environment variables.")
        return None
    try:
        headers = {'Authorization': f'Bearer {api_token}'}
        logging.info(f"Fetching configuration from {api_url}...")
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an error if the request failed
        logging.info("Configuration fetched successfully.")
        return response.json()  # Return the parsed JSON response as a dictionary
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching configuration: {e}")
        return None
```

In this part of the script, the following steps occur:
- The script reads the decrypted **API token** from the environment.
- It sends an authenticated request to the API server using the token.
- The server responds with a **JSON configuration** that contains the settings for the device (VLANs, interfaces, firewall rules, etc.).

---
