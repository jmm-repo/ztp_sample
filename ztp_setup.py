import os
import requests
import logging
from cryptography.fernet import Fernet

# Configure logging for debugging and tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Decrypt the encrypted environment settings
def load_key():
    """
    Load the encryption key from a file.
    
    This key is used to decrypt the encrypted environment settings.

    Returns:
        bytes: The encryption key used for decryption.
    
    Raises:
        FileNotFoundError: If the key file is not found.
        Exception: For any other error that occurs during key loading.
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

def decrypt_env():
    """
    Decrypt the environment file and load the decrypted values into environment variables.

    This function reads the encrypted environment file (`encrypted_env.bin`), decrypts it using 
    the encryption key, and sets each decrypted key-value pair as an environment variable.

    Raises:
        FileNotFoundError: If the encrypted environment file is not found.
        Exception: For any other decryption-related errors.
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

# Step 2: External function to fetch configuration data from API
def fetch_configuration(api_url):
    """
    Fetch the network configuration from the API using the decrypted environment variables.

    This function makes an HTTP GET request to the given API URL and retrieves the 
    configuration data in JSON format. It uses an API token stored in environment variables 
    for authentication.

    Args:
        api_url (str): The URL of the API to fetch configuration from.

    Returns:
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

class NetworkConfig:
    """
    A class to manage and manipulate network configurations, including VLANs, DNS, firewall rules, 
    routing, and interfaces. It also provides methods to display, modify, and generate Cisco CLI 
    configurations for network devices like switches and routers.
    """
    def __init__(self, config_data):
        """
        Initialize the NetworkConfig object by parsing the configuration data.

        Args:
            config_data (dict): The network configuration data in dictionary format.
        
        Raises:
            Exception: If there is an error parsing the configuration data.
        """
        try:
            # Parse the provided configuration data into different network settings
            self.dns_settings = config_data.get("dns", {})
            self.vlans = config_data.get("vlans", [])
            self.firewall_rules = config_data.get("firewall", {}).get("rules", [])
            self.routing = config_data.get("routing", {}).get("static_routes", [])
            self.interfaces = config_data.get("sw_interfaces", [])
            logging.info("NetworkConfig initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing NetworkConfig: {e}")
            raise

    def display_dns_settings(self):
        """
        Display the DNS settings in the configuration.
        
        This method prints the primary and secondary DNS servers stored in the configuration.
        """
        try:
            print(f"DNS Settings:\nPrimary DNS: {self.dns_settings.get('primary')}, Secondary DNS: {self.dns_settings.get('secondary')}")
        except Exception as e:
            logging.error(f"Error displaying DNS settings: {e}")

    def display_vlans(self):
        """
        Display the VLAN configurations in the network configuration.

        This method prints the VLAN ID, name, and IP range for each VLAN in the configuration.
        """
        try:
            print("VLAN Configurations:")
            for vlan in self.vlans:
                print(f"VLAN ID: {vlan['id']}, Name: {vlan['name']}, IP Range: {vlan.get('ip_range', 'N/A')}")
        except Exception as e:
            logging.error(f"Error displaying VLANs: {e}")

    def display_firewall_rules(self):
        """
        Display the firewall (ACL) rules in the network configuration.

        This method prints each firewall rule, showing the rule ID, action (permit or deny), 
        protocol, source, destination, and port (if applicable).
        """
        try:
            print("Firewall/ACL Rules:")
            for rule in self.firewall_rules:
                action = "permit" if rule["action"] == "allow" else "deny"
                print(f"Rule ID: {rule['id']}, Action: {action}, Protocol: {rule['protocol']}, "
                      f"Source: {rule['source']}, Destination: {rule['destination']}, Port: {rule.get('port', 'N/A')}")
        except Exception as e:
            logging.error(f"Error displaying firewall rules: {e}")

    def display_routing(self):
        """
        Display the static routing configurations in the network configuration.

        This method prints each static route, showing the destination and the gateway for the route.
        """
        try:
            print("Routing Configurations:")
            for route in self.routing:
                print(f"Destination: {route['destination']}, Gateway: {route['gateway']}")
        except Exception as e:
            logging.error(f"Error displaying routing: {e}")

    def display_interfaces(self):
        """
        Display the interface configurations in the network configuration.

        This method prints each interface, showing the interface name, description (if present), 
        associated VLAN, and IP address configuration.
        """
        try:
            print("Interface Configurations:")
            for interface in self.interfaces:
                print(f"Interface: {interface['name']}, Description: {interface.get('description', 'N/A')}, "
                      f"VLAN: {interface.get('vlan', 'N/A')}, IP Address: {interface.get('ip_address', 'N/A')}")
        except Exception as e:
            logging.error(f"Error displaying interfaces: {e}")

    def generate_cisco_switch_config(self, tftp_server_ip):
        """
        Generate a Cisco CLI configuration for the switch, including TFTP download for startup config.

        This method prints the Cisco CLI commands required to configure the switch based on the 
        network configuration, including VLANs and interfaces. It also includes the TFTP command 
        to download the startup configuration from the TFTP server.

        Args:
            tftp_server_ip (str): The IP address of the TFTP server where the configuration will be fetched.
        """
        try:
            config_filename = "switch_config.txt"  # This can be dynamically generated per device
            print(f"! Downloading configuration from TFTP server {tftp_server_ip}")
            print(f"copy tftp://{tftp_server_ip}/{config_filename} startup-config")
            print(f"! Cisco Switch Configuration")
            
            print("!\n! VLAN Configuration")
            for vlan in self.vlans:
                print(f"vlan {vlan['id']}")
                print(f" name {vlan['name']}")
            
            print("!\n! Interface Configuration")
            for interface in self.interfaces:
                print(f"interface {interface['name']}")
                if "description" in interface:
                    print(f" description {interface['description']}")
                if "vlan" in interface:
                    print(f" switchport access vlan {interface['vlan']}")
                if "ip_address" in interface:
                    print(f" ip address {interface['ip_address']} {interface['subnet_mask']}")
            
            print("!\n")
            logging.info("Cisco switch configuration generated successfully.")
        except Exception as e:
            logging.error(f"Error generating Cisco switch
