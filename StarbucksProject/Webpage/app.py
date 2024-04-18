from flask import Flask, render_template, request, jsonify
import psycopg2

#Establishing connection to PostgreSQL database
conn = psycopg2.connect(dbname="Starbucks",user="postgres",password="Zenith1234!",host="localhost",port="5432")
cursor = conn.cursor()


app = Flask(__name__)

#Home Route
@app.route('/')
def index():
    return render_template('index.html')

#About route
@app.route('/about')
def about():
    return render_template('about.html') 

# Dashboard Route with get request


def get_rev_data():
    try:
        cursor.execute("""SELECT x.name,
                           CAST(SUM(CAST(x.price AS DECIMAL)) AS DECIMAL) AS total_price
                        FROM (
                            SELECT ord.Datetime,
                                   st.location,
                                   st.name,
                                   dr.name AS drink_name,
                                   dr.price
                            FROM Orders ord
                            JOIN drink dr ON dr.drinkid = ord.drinkid
                            JOIN Store st ON st.storeid = ord.storeid
                        ) AS x
                        GROUP BY x.name
                        ORDER BY total_price DESC""")
        rev_data = cursor.fetchall()
        if rev_data:
            rev_labels = [row[0] for row in rev_data]
            rev_values = [float(row[1]) for row in rev_data]  # Convert to float if necessary
            print("rev_labels:", rev_labels)
            print("rev_values:", rev_values)
            return rev_labels, rev_values
        else:
            return [], []  # Return empty lists if no data is retrieved
    except Exception as e:
        print(str(e))
        return [], []

@app.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        # Execute a query to retrieve recent data from the database
        cursor.execute("""SELECT DATE(x.Datetime) AS date,
                           CAST(x.Datetime AS TIME) AS time,
                           EXTRACT(HOUR FROM x.Datetime) AS hour,
                           x.location, 
                           x.name, 
                           x.drink_name, 
                           x.price
                        FROM (
                            SELECT ord.Datetime, st.location, st.name, dr.name AS drink_name, dr.price
                            FROM Orders ord
                            JOIN drink dr ON dr.drinkid = ord.drinkid
                            JOIN Store st ON st.storeid = ord.storeid
                        ) AS x
                        ORDER BY x.Datetime DESC
                        LIMIT 10""")
        data = cursor.fetchall()
        # Convert the retrieved data to a list of dictionaries
        results = [{'Date': row[0], 'Time': str(row[1]), 'Hour': row[2], 'Location': row[3], 'Name': row[4], 'Drink Name': row[5], 'Price': row[6]} for row in data]
        
        # Get revenue data
        rev_labels, rev_values= get_rev_data()
        
        return render_template('dashboard.html', data=results, rev_labels=rev_labels, rev_values=rev_values)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Main Loop
if __name__ == '__main__':
    app.run(debug=True)

cursor.close()
conn.close() 
