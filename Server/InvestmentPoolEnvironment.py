from Pool import Pool
from datas import frequency_time_unit, price_coefficient, investment_coefficient
import datetime

class InvestmentPoolEnvironment:
    def __init__(self, pool: Pool):
        self.pool = pool
        self.current_state = None
        self.current_action = None

    def step(self, action):
        # Apply the action (change the frequency of minting)
        self.pool.current_frequency = action
        self.pool.update_withdrawals_amounts()

        # Calculate the reward
        reward = self.calculate_reward()

        # Update the current state
        self.current_state = self.get_state()

        return self.current_state, reward

    def calculate_reward(self):
        # Calculate the reward based on the change in price and investment frequency
        price_reward = self.calculate_price_reward()
        investment_reward = self.calculate_investment_reward()

        return price_coefficient * price_reward + investment_coefficient * investment_reward

    def calculate_price_reward(self):
        # Calculate the reward based on the change in price
        if len(self.pool.prices) < 2:
            return 0

        return self.pool.prices[-1] - self.pool.prices[-2]

    def calculate_investment_reward(self):
        # Calculate the reward based on the change in investment frequency
        if len(self.pool.investments) < 2:
            return 0

        if self.pool.investments[-1][0] - self.pool.investments[-2][0] < frequency_time_unit:
            return self.pool.investments[-1][1] - self.pool.investments[-2][1]
        else:
            return 0

    def get_state(self):
        # The state is the current price and the current frequency of investment
        current_price = self.pool.get_current_price()
        current_frequency_of_investment = self.pool.calculate_current_frequency()
        return current_price, current_frequency_of_investment

    def get_investment_frequency(self):
        if len(self.pool.investments) == 0:
            return 0
        sum = 0
        for investment in self.pool.investments:
            if datetime.datetime.now() - investment[0] < datetime.timedelta(seconds=frequency_time_unit):
                break
            sum += investment[1].carbon_value
        return sum / frequency_time_unit

    def reset(self):
        # Reset the environment to the initial state
        self.pool = Pool(self.pool.standard, self.pool.carbon_type, self.pool.issuance_year)
        self.current_state = self.get_state()
        self.current_action = None
