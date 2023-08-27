# FedEx Tracking API Python Client

This is a Python client for the [FedEx Tracking API](https://developer.fedex.com/api/en-at/catalog/track/v1/docs.html).

It is not fully featured yet, but it is a good starting point. It requires you to have a FedEx developer account and an API key.

## Installation

```bash
pip install fedextrack
```

## Usage

```python
from fedextrack import FedEx

api = FedEx("YOUR_API_KEY", "YOUR_API_SECRET")

# Realtime tracking

tracking = api.tracking("YOUR_SHIPMENT_NUMBER")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.