# DHL Tracking API Python Client

This is a Python client for the [DHL Shipment Tracking Unified API](https://developer.dhl.com/api-reference/shipment-tracking).

It is not fully featured yet, but it is a good starting point. It requires you to have a DHL developer account and an API key.

## Installation

```bash
pip install dhltrack
```

## Usage

```python
from dhltrack import DHL

api = DHL("YOUR_API_KEY", "YOUR_API_SECRET")

# Realtime tracking

tracking = api.track("YOUR_SHIPMENT_NUMBER")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.