# FastAPI Scraping Project

This project is a FastAPI-based web application for scraping product data and caching the results using MongoDB and Redis. The goal is to avoid updating product data in the database if the scraped product price has not changed.

## Setup Instructions

### Prerequisites

- Python 3.8+
- MongoDB
- Redis

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/fastapi-scraping-caching.git
   cd fastapi-scraping-caching

### install the required dependencies:
- pip install -r requirements.txt

### make sure all redis-server is up and mongodb is also connected.

### start the fast api server
- fastapi dev main.py  

### Open your browser and navigate to http://127.0.0.1:8000/docs to view the interactive API documentation.

### To scrape product data, send a POST request to /scrape with the required parameters:

curl --location --request POST 'http://127.0.0.1:8000/scrape' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--header 'x-token: atlys_test' \
--data-raw '{
    "pages": "5",
    "url":"https://dentalstall.com/shop",
    "proxy": null
}'