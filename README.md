
---

### Key Sections of the README:

1. **Project Title and Description**: An introduction to the project and its purpose (ZTP automation for network devices).
2. **Features**: A bullet-point list of the key functionalities provided by the script.
3. **Project Structure**: An outline of the repository contents.
4. **Getting Started**: Step-by-step guide to clone, install dependencies, and run the project.
5. **Configuration**: Explains how to configure API settings and the TFTP server.
6. **Usage**: Details on how the script works and what configurations it generates.
7. **Debugging and Logs**: Information on how to monitor the script through logging.
8. **Contributing**: Guidelines for contributing to the project.
9. **License**: Licensing information.
10. **Contact**: Contact details for issues and support.

### Tips for Hosting:
- **Ensure that you push all necessary files** like `README.md`, `requirements.txt`, and any other dependencies.
- **Keep sensitive information like the API token out of the repository**. This should only be stored in encrypted files and never hardcoded or committed.

### Optional Files:
- **`requirements.txt`**: List of Python dependencies for the project.
- **`LICENSE`**: A file describing the license under which the project is distributed (e.g., MIT).

Let me know if you need further customization or additions!

Absolutely! Let’s take a closer look at the **README.md** file and make improvements by providing **in-depth details** about how the script works, what each component does, and how users can interact with it. We’ll explain every key part of the script so that users, even with minimal experience, can easily follow along and understand what’s happening.

### Improved and Detailed `README.md` for GitHub:

```markdown
# Network Automation ZTP Script

This project provides a Python-based solution for automating **Zero-Touch Provisioning (ZTP)** for network devices such as switches and routers. The script handles the process of **fetching configuration data** from a remote API, generating **Cisco CLI configurations**, and enabling network devices to **download and apply their startup configuration** via **TFTP**.

The goal is to streamline network deployment in environments where devices need to be configured automatically without manual intervention.

## Overview of How This Script Works

The script performs the following core tasks:

1. **Secure Decryption of Environment Variables**: The API token and other sensitive data are securely stored in an encrypted file, which is decrypted at runtime using a **Fernet encryption key**.
2. **Fetch Configuration Data from API**: The script contacts a remote API server (typically hosted on an EC2 instance or similar cloud service) and retrieves network configuration data for the devices.
3. **Generate Cisco CLI Configurations**: Based on the data returned from the API, the script generates a Cisco CLI configuration for switches and routers, containing critical configurations like VLANs, interfaces, and firewall rules.
4. **TFTP Download for Configuration**: The script adds a command to allow devices to download their configuration files via **TFTP** from a designated TFTP server.
5. **Logging and Debugging**: The script includes comprehensive logging to help monitor the progress and catch any errors during execution.

---

## Detailed Script Workflow

### 1. Secure Decryption of Environment Variables

Before any network configuration data can be fetched from the API, the script must first decrypt sensitive environment variables, such as the **API token**. This is achieved through **Fernet encryption**, ensuring that sensitive credentials are not exposed in plain text.

- The script expects two files:
  - `secret.key`: The encryption key used to decrypt the environment variables.
  - `encrypted_env.bin`: The encrypted environment variables (e.g., API token, TFTP server IP).
  
**How it works:**
- The script first loads the `secret.key` file.
- It then reads the encrypted data from `encrypted_env.bin`.
- Using the key, it decrypts the contents and loads the key-value pairs into environment variables (via `os.environ`), so they are accessible during the script execution.

```python
decrypt_env()
```

This ensures the API token and other configuration details are securely handled without hardcoding them into the script.

### 2. Fetch Configuration Data from API

Once the environment variables are decrypted and available, the script makes an **API request** to fetch the network configuration data. This data is returned in **JSON format**, typically containing information such as VLAN settings, firewall rules, static routes, and interface configurations.

**API Interaction:**
- The API token, loaded from the decrypted environment, is passed as a bearer token in the authorization header.
- The script uses the `requests` library to make an HTTP GET request to the API endpoint.
- The JSON response contains all the necessary configuration data that will be used to generate the CLI configurations.

Example API request:
```python
response = requests.get(api_url, headers={'Authorization': f'Bearer {api_token}'})
```

### 3. Generate Cisco CLI Configurations

After the configuration data is fetched from the API, the script processes this data and generates the corresponding **Cisco CLI configuration** for the devices. The generated CLI configurations include:

- **VLAN Configurations**: This section defines the VLANs that should be created on the switch.
- **Firewall Rules (ACLs)**: These rules control the traffic flow based on various criteria, such as source/destination, protocol, and ports.
- **Static Routes**: For routers, static routes are added based on the configuration data.
- **Interface Configurations**: Interfaces are configured with IP addresses, descriptions, and VLAN assignments.

Each of these configurations is generated as part of the Cisco CLI commands, ensuring that the network devices are set up according to the defined policies.

**Example of VLAN CLI generation:**
```python
for vlan in self.vlans:
    print(f"vlan {vlan['id']}")
    print(f" name {vlan['name']}")
```

**Example of routing generation for routers:**
```python
for route in self.routing:
    print(f"ip route {route['destination']} {route['gateway']}")
```

### 4. TFTP Download for Configuration

To complete the ZTP process, the script also generates a command that instructs the device to download its configuration file from a **TFTP server**. This command is crucial in ZTP environments where devices need to fetch their configurations after obtaining an IP address via **DHCP**.

- The TFTP server IP is provided through the decrypted environment variables or directly in the script.
- The device uses the following command to download and apply its configuration:
  
```plaintext
copy tftp://<TFTP_SERVER_IP>/<config_filename> startup-config
```

For example, in the Cisco switch configuration, this would look like:
```python
print(f"copy tftp://{tftp_server_ip}/switch_config.txt startup-config")
```

### 5. Logging and Debugging

The script uses Python’s `logging` module for robust logging. This allows users to track the progress of the script, monitor API requests, and catch errors or warnings.

- **Info-level logs** track major events such as fetching configurations or applying changes.
- **Error-level logs** catch issues like failed API requests, missing files, or decryption failures.

You can adjust the verbosity of the logs by modifying the logging level in the script:
```python
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
```

---

## Installation and Setup

### Prerequisites

1. **Python 3.8+**: Ensure that Python is installed on your system. You can check this by running:
    ```bash
    python --version
    ```

2. **Python Packages**: The following Python packages are required and can be installed via `pip`:
    ```bash
    pip install -r requirements.txt
    ```

### Installation Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/network-automation-ztp.git
    cd network-automation-ztp
    ```

2. **Encrypt Your Environment Variables**:
   The environment variables such as API tokens and the TFTP server IP are stored in an encrypted file (`encrypted_env.bin`). Here's how to set them up:

   - First, generate the **encryption key** and save it to `secret.key`:
     ```python
     from cryptography.fernet import Fernet
     key = Fernet.generate_key()
     with open('secret.key', 'wb') as key_file:
         key_file.write(key)
     ```

   - Encrypt your environment variables and save them in `encrypted_env.bin`:
     ```python
     api_token = "your_api_token_here"
     tftp_server_ip = "192.168.1.100"
     env_data = f"API_TOKEN={api_token}\nTFTP_SERVER_IP={tftp_server_ip}"

     fernet = Fernet(key)
     encrypted_data = fernet.encrypt(env_data.encode())

     with open('encrypted_env.bin', 'wb') as encrypted_file:
         encrypted_file.write(encrypted_data)
     ```

3. **Run the Script**:
   Ensure both `secret.key` and `encrypted_env.bin` are in the working directory, then execute:
   ```bash
   python script.py
   ```

---

## Example Workflow

1. **Device Boots and Requests IP**: When the device boots up, it sends a DHCP request to obtain an IP address.
2. **DHCP Provides IP and TFTP Info**: The DHCP server responds with the IP address and the TFTP server information.
3. **Device Contacts API**: The device contacts the API to request its specific configuration.
4. **Device Downloads Config via TFTP**: The device uses the TFTP server IP to download its startup configuration file.
5. **Device Applies Config**: The startup configuration is applied, and the device becomes operational.

---

## Debugging and Logs

Logs provide insight into the execution flow and can help diagnose issues. Logs are written to the console by default and include timestamps, log levels, and messages.

- **Debug Level**: For development or deeper investigation, use the `DEBUG` level to see more granular details.
- **Error Logging**: Errors (e.g., issues with decryption, file not found, failed API requests) are logged under `ERROR` level.

Example of how to change the logging level:
```python
logging.basicConfig(level=logging.DEBUG)
```

---

## Contributing

We welcome contributions from the community! Here’s how you can contribute:

1. Fork the repository.
2. Create a new branch for your feature or fix (`git checkout -b feature/my-feature`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push your branch (`git push origin feature/my-feature`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Contact

For questions or support, please contact:

- **Name**: Your Name
- **Email**
