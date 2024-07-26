# 🛒 Ecommerce Scraping Project

Welcome to the **Ecommerce Scraping Project**! This project is a powerful Django-based web application designed to scrape product data from various e-commerce websites and present it in an intuitive and user-friendly interface.

## 🌟 Features

- **Multi-site Scraping:** Collect product data from Amazon, eBay, and Best Buy.
- **Database Storage:** Efficiently store scraped data in a PostgreSQL database.
- **Detailed Product Display:** Show comprehensive product information including image, name, price, reviews, sentiment score, and sentiment label.
- **Smart Product Selection:** Automatically identify and highlight the best product based on sentiment score and price.

## 🛠 Requirements

- Python 3.10
- Django 4.2
- Django REST framework 3.14.0
- psycopg2-binary 2.9.6
- requests 2.31.0
- beautifulsoup4 4.12.2
- lxml 4.9.3
- vaderSentiment==3.3.2

## ⚙️ Installation

Follow these steps to set up the project:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/ecommerce_scraping.git
    cd ecommerce_scraping
    ```

2. **Create a Virtual Environment and Activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply the Migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```

## 🐳 Docker Setup

To run the project using Docker, follow these steps:

1. **Build the Docker Image:**

    ```bash
    docker build -t ecommerce_scraping .
    ```

2. **Run the Docker Container:**

    ```bash
    docker run -p 8000:8000 ecommerce_scraping
    ```

## 🚀 Usage

1. Open your web browser and navigate to `http://127.0.0.1:8000`.
2. Enter a product name in the search bar and click **"Search"**.
3. If the product data is already in the database, it will be displayed immediately.
4. If the product data is not in the database, the application will scrape the data and display it once the scraping is complete.

## 🛠 Configuration

Ensure to set environment variables for API keys, database credentials, etc., as needed. This can be done by creating a `.env` file in the root directory and adding the required variables.

## 🧩 Contributing

We welcome contributions to enhance the project! Please follow these steps:

1. **Fork the repository**.
2. **Create a new branch** for your feature or bug fix.
3. **Submit a Pull Request** with a clear description of your changes.

## ❓ Troubleshooting

If you encounter any issues, please refer to the [FAQ](#) section or open an issue on GitHub.

## 💼 Credits

We appreciate the use of external libraries and tools that made this project possible. Special thanks to the developers of BeautifulSoup, Scrapy, Django, and others.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📧 Contact

For any questions, suggestions, or feedback, please feel free to contact:

**Name:** Bitsol Technologies
**Email:** [ismail@bitsol.tech](mailto:ismail@bitsol.tech)

---
Happy Scraping! 🚀
