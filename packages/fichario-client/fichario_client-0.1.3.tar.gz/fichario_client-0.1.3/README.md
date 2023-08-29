<p align="center">
  <a href="http://nestjs.com/" target="blank"><img src="https://fichar.io/documentation/03-IV_Horiz_Invertido.svg" width="400" alt="Nest Logo" /></a>
</p>

# Fichar.io API Client


The `Fichario Client` Python library serves as a client for interacting with the API provided by Fichar.io. This API client simplifies the process of authenticating users and making various requests to the API's endpoints. The client uses JSON Web Tokens (JWT) for authentication and supports retrieving user credentials, company information, device details, payload data, etc.

## Installation
You can install the package using pip:

```bash
pip install fichario-client
```

## Usage

1. Import the `FicharioClient` class:

```python
from fichario_client.client import FicharioClient
```

2. Create an instance of the `FicharioClient` class with your user credentials:

```python
client = FicharioClient(email="your_email@example.com", password="your_password")
```

3. Access API functionalities using the client's methods:

- Retrieve user credentials:
```python
user_credentials = client.get_user_credentials()
print(user_credentials)
```

- Retrieve your company's information:
```python
company_info = client.get_my_company()
print(company_info)
```

- List your devices:
```python
devices = client.list_my_devices()
print(devices)
```

- Get information about a specific device:
```python
device_id = "your_device_id"
device_info = client.get_device(deviceId=device_id)
print(device_info)
```

- Retrieve payload data from a device:
```python
payload_data = client.get_payload(deviceId=device_id, get_all=True)
print(payload_data)
```

- Retrieve raw payload data from a device:
```python
raw_payload_data = client.get_raw_payload(deviceId=device_id)
print(raw_payload_data)
```

- Get device information:
```python
device_info = client.get_device_info(deviceId=device_id)
print(device_info)
```
Retrieve alarms associated with a device:
```python
alarms = client.get_device_alarms(deviceId=device_id)
print(alarms)
```

Retrieve alarm history associated with a device:
```python
alarm_history = client.get_device_alarms_history(deviceId=device_id)
print(alarm_history)
```

**Note:** Ensure you have all the requirements for the library installed before using the library `FicharioClient`.

**Contributing**

Contributions to this API client are welcome. If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the project's GitHub repository.

**License**

This project is licensed under the MIT License. You can find the license details in the `LICENSE` file in the project repository.

**Disclaimer**

This API client is designed to interact with the "https://api.fichar.io/" API based on the available information. Be sure to refer to the API documentation for detailed information about endpoints, authentication, and usage limits.




## Stay in touch

- Author - [Ronald Lopes](https://github.com/RonaldLopes)
- Website - [https://fichar.io](https://fichar.io/)