from flask import Flask, request, jsonify, make_response
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/update', methods=["POST"])
def update():
    payload = request.get_json(force=True)
    print(payload)
    humidity  = payload['humidity']
    temperature = payload['temperature']
    sql = 'INSERT INTO data(humidity, temperature) VALUES(%s, %s)'%(humidity, temperature)
    with psycopg2.connect(DATABASE_URL, sslmode='require')as db:
        c = db.cursor()
        c.execute(sql)
        db.commit()
    return make_response('OK', 200)

@app.route('/query', methods=['GET'])
def query():
    with psycopg2.connect(DATABASE_URL, sslmode='require') as db:
        c = db.cursor()
        c.execute('SELECT * FROM data')
        records = c.fetchall()
        results = []
        for r in records:
            results.append({'timestamp':r[1], 'humidity':r[2], 'temperature':r[3]})
        db.commit()
    return jsonify(results)

if __name__ == '__main__':
    with psycopg2.connect(DATABASE_URL, sslmode='require') as db:
        c = db.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS data
          (_id SERIAL PRIMARY KEY,
           timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
           humidity FLOAT NOT NULL,
           temperature FLOAT NOT NULL)''')
        db.commit()
    app.run(debug=True)
