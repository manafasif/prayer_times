from flask import Flask, jsonify, request

app = Flask(__name__)

# This is just a skeleton for the API


@app.route('/graph', methods=['GET'])
def get_graph():
    # get parameters from query string
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    address = request.args.get('address')

    # call function to retrieve image
    image = generate_graph(start_date, end_date, address)

    # return image as response
    response = jsonify({'image': image})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def generate_graph(start_date, end_date, address):
    # implement logic to retrieve image data based on date range and address
    # ...
    return graph


if __name__ == '__main__':
    app.run(debug=True)
