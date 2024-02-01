# Reinforcement Learning for carbon token investment

In this project, we explore the use of Reinforcement Learning in cryptocurrency investment for green energy credits. We delve into the significance of the carbon credit market globally, post-Paris Agreement, and propose a method to transform carbon credits into tradable cryptocurrencies using Reinforcement Learning powered investment pools. We tackles the challenges of carbon credit value variabilities and the integration of deep Q learning learning networks into smart contracts. We aim to adapt our model for real-world application by testing it in simulated environments.

---
## Installation

Before using the API, you need to set up the Python environment and install the required dependencies.

1. Install Flask using pip (if not already installed):
   ```
   pip install flask
   ```

2. Save the provided Python code in a file, e.g., `app.py`.

3. Run the Flask application:
   ```
   python app.py
   ```

The application will start and be accessible at `http://localhost:3000`.

---
## Flask API for Carbon Credit Tokenization and Investment Pools

This Flask application provides an API for managing carbon credit tokens and investment pools related to these tokens. The application includes several endpoints for token creation, investment, and withdrawal.

### Setup and Dependencies

- Install Flask and other necessary libraries using `pip`.
- Import the required modules: Flask, random, string, time, datetime, json, threading.
- Import custom modules: `ERC1155Token`, `DQNAgent`, `Pool`, `InvestmentPoolEnvironment`, `datas`.

### Running the Application

- Run the application using: `python <script_name>.py`.
- The application will start on `localhost` at port `3000`.

### API Endpoints

#### 1. `/credittotoken/<token_id>` (GET)

Converts a carbon credit to a token.

- **Path Parameter**: `token_id` - The unique identifier of the token.
- **Returns**: JSON object with `token` key containing the token data.

Curl command:

```
curl -X GET http://localhost:3000/credittotoken/<token_id>
```

#### 2. `/certToPool/<token_id>/<address>` (GET)

Invests a token into a pool.

- **Path Parameters**:
  - `token_id` - The unique identifier of the token.
  - `address` - The address to which the token is linked.
- **Returns**: JSON object with `approve` key indicating success (`'1'`) or failure (`'0'`).

Curl command:

```
curl -X GET http://localhost:3000/certToPool/<token_id>/<address>
```

#### 3. `/withdraw/<token_id>` (GET)

Withdraws an investment from a pool.

- **Path Parameter**: `token_id` - The unique identifier of the token.
- **Query Parameter**: `address` - The address associated with the token.
- **Returns**: JSON object with `amount` key indicating the withdrawal amount.

Curl command:

```
curl -X GET "http://localhost:3000/withdraw/<token_id>?address=<address>"
```

#### 4. `/triggerPool/<standard>/<carbon_type>/<year>` (GET)

Triggers a learning algorithm for a specific pool.

- **Path Parameters**:
  - `standard` - The standard of the pool.
  - `carbon_type` - The type of carbon credit.
  - `year` - The year of the pool.
- **Returns**: JSON object with `success` key indicating success (`'1'`).

Curl command:

```
curl -X GET http://localhost:3000/triggerPool/<standard>/<carbon_type>/<year>
```

---

## Notes

- The application uses random values and hardcoded data for demonstration purposes.
- It is designed to handle carbon credit tokens with various attributes like standard, type, and value.
- The `DQNAgent` and `Pool` classes are used to manage the investments and learning algorithm for the investment pools.
- Ensure that all custom modules (`ERC1155Token`, `DQNAgent`, `Pool`, `InvestmentPoolEnvironment`, `datas`) are correctly set up and imported.


