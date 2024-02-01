from flask import Flask, jsonify, request
import random
import string
import time
import datetime
import json
import threading

from ERC1155Token import ERC1155EnergyToken
from RLAgent import DQNAgent
from Pool import Pool
from InvestmentPoolEnvironment import InvestmentPoolEnvironment
from datas import *

app = Flask(__name__)

# endpoint: /credittotoken/TokenID (GET)
@app.route('/credittotoken/<token_id>', methods=['GET'])
def credit_to_token(token_id):
    # the carbon credit values are just for sake of implementing a minimum viable product
    carbon_type = 0
    carbon_value = random.randint(10, 32_800)
    year = 2024 - 1985
    if token_id.startswith('GNE'):
        standard_value = standards_name_to_id['verra']
    else:
        standard_value = standards_name_to_id['satba']
    # make the hex string 4 bits for standard, 4 bits for carbon type, 16 bits for carbon value, 8 bits for year
    hex_string = f'{standard_value:04b}{carbon_type:04b}{carbon_value:016b}{year:08b}'
    # add the token to the tokens dictionary
    tokens[token_id] = {"token_data": hex_string}
    return jsonify({'token': hex_string})

# endpoint: /certToPool/TokenID (GET)
@app.route('/certToPool/<token_id>/<address>', methods=['GET'])
def cert_to_pool(token_id, address):
    # check if the token exists
    if token_id not in tokens:
        return jsonify({'error': 'Token not found'}), 404
    # get the token data
    hex_string = tokens[token_id]['token_data']
    standard_value = int(hex_string[:4], 2)
    carbon_type = int(hex_string[4:8], 2)
    carbon_value = int(hex_string[8:24], 2)
    year = int(hex_string[24:], 2) + 1985
    standard = standards_id_to_name[standard_value]
    carbon_type = carbon_id_to_type[carbon_type]
    # check if the pool exists
    if standard not in pools or carbon_type not in pools[standard] or year not in pools[standard][carbon_type]:
        return jsonify({'approve': '0'}), 404
    # get the pool
    pool = pools[standard][carbon_type][year]
    # invest in the pool
    pool.invest(ERC1155EnergyToken(token_id, standard, carbon_value, carbon_type, address, year))
    # add the token to the tokens dictionary
    tokens[token_id]['address'] = address
    # return the approve
    return jsonify({'approve': '1'})

@app.route('/withdraw/<token_id>', methods=['GET'])
def withdraw(token_id):
    # check if the token exists
    if token_id not in tokens:
        return jsonify({'error': 'Token not found'}), 404
    # get the token data
    hex_string = tokens[token_id]['token_data']
    standard_value = int(hex_string[:4], 2)
    carbon_type = int(hex_string[4:8], 2)
    carbon_value = int(hex_string[8:24], 2)
    year = int(hex_string[24:], 2) + 1985
    standard = standards_id_to_name[standard_value]
    carbon_type = carbon_id_to_type[carbon_type]
    # check if the pool exists
    if standard not in pools or carbon_type not in pools[standard] or year not in pools[standard][carbon_type]:
        return jsonify({'approve': '0'}), 404
    # get the pool
    pool = pools[standard][carbon_type][year]
    # check if the token is in the pool
    if token_id not in tokens or tokens[token_id]['address'] != request.args.get('address'):
        return jsonify({'error': 'Token not found'}), 404
    # get the address
    address = tokens[token_id]['address']
    # withdraw from the pool
    amount = pool.owners_withdrawals[address]
    # return the amount
    return jsonify({'amount': 'amount'})

@app.route('/triggerPool/<standard>/<carbon_type>/<year>', methods=['GET'])
def trigger_pool(standard, carbon_type, year):
    if standard not in pools or carbon_type not in pools[standard] or year not in pools[standard][carbon_type]:
        return jsonify({'error': 'Pool not found'}), 404
    pool = Pool(standard, carbon_type, year)
    ipe = InvestmentPoolEnvironment(pool)
    agent = DQNAgent(ipe)
    # create a new thread and run the pool
    def learn():
        state = ipe.get_state()
        action = agent.act(state)
        next_state, reward = ipe.step(action)
        agent.remember(state, action, reward, next_state)
        agent.replay()
        # sleep for 3 hours
        time.sleep(3 * 60 * 60)
    threading.Thread(target=learn).start()
    return jsonify({'success': '1'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
