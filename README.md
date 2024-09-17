# API-Commandes

# Creation of the shared network
docker network create shared-network

# Build app
docker-compose build

# Run app
docker-compose up

# Stop app
docker-compose down

# Application

The application will be available at [http://127.0.0.1:8002](http://127.0.0.1:8002).

## Postman collection

### JSON File

```json 
{
    "info": {
        "name": "FastAPI Orders API",
        "_postman_id": "your_postman_id",
        "description": "Collection for testing API Orders",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": [
        {
            "name": "Create Order",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json",
                        "type": "text"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\"clientId\": 1, \"produits\": [{\"produitId\": 1}, {\"produitId\": 2}]}"
                },
                "url": {
                    "raw": "http://127.0.0.1:8002/customers/orders",
                    "protocol": "http",
                    "host": [
                        "127",
                        "0",
                        "0",
                        "1"
                    ],
                    "port": "8002",
                    "path": [
                        "customers",
                        "orders"
                    ]
                }
            },
            "response": []
        },
        {
            "name": "Get Orders by Customer ID",
            "request": {
                "method": "GET",
                "header": [],
                "url": {
                    "raw": "http://127.0.0.1:8002/customers/:customer_id/orders",
                    "protocol": "http",
                    "host": [
                        "127",
                        "0",
                        "0",
                        "1"
                    ],
                    "port": "8002",
                    "path": [
                        "customers",
                        ":customer_id",
                        "orders"
                    ],
                    "variable": [
                        {
                            "key": "customer_id",
                            "value": "1"
                        }
                    ]
                }
            },
            "response": []
        }
    ]
}

```