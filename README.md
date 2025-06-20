# 🛒 Automated Purchase Simulator with Selenium

This project is an **automated purchase simulation tool** built with [Selenium](https://www.selenium.dev/) and Python. Its purpose is to simulate and test the checkout flow of an e-commerce website using randomly generated fake user data (via the [Faker](https://faker.readthedocs.io/en/master/) library). No real transaction is completed — this is strictly for educational and testing purposes.

> ⚠️ **Disclaimer**: This script is intended for educational and ethical automation testing only. Do not use it on websites without permission.

---

## 🚀 Features

- Accesses a specific product page.
- Accepts cookies automatically (multiple fallback selectors).
- Adds the product to cart using multiple selector strategies.
- Fills in user info (name, email, address, CPF, phone, etc.).
- Selects credit card payment method.
- Fills out fake credit card details (Visa, Mastercard, Amex).
- Does **not** finalize the transaction.
- Simulates multiple purchases with randomized delays.
- Logs all steps using Python’s `logging`.

---

## 🧰 Technologies Used

- Python 3.8+
- [Selenium](https://pypi.org/project/selenium/)
- [Faker (pt_BR)](https://faker.readthedocs.io/en/master/locales.html#faker-providers-person-pt-br)
- Google Chrome + ChromeDriver

---

## 📦 Installation

1. **Clone the repository**

```requiriments
selenium>=4.0.0
faker>=19.6.1
```
