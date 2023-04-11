from flask import Flask, jsonify, request

from prayertimes import *

app = Flask(__name__)

# This is just a skeleton for the API


@app.route('/graph', methods=['GET'])
def get_graph():
    # get parameters from query string
    start_month = request.args.get('start_month')
    start_year = request.args.get('start_year')
    end_month = request.args.get('end_month')
    end_year = request.args.get('end_year')

    address = request.args.get('address')

    # call function to retrieve image
    # image = generate_graph(start_date, end_date, address)
    graph = generate_prayer_times_graph(
        start_month, start_year, end_month, end_year, address)

    # return image as response
    response = jsonify({'graph': graph})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(debug=True)
