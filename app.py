from flask import Flask, redirect, request, render_template, url_for


transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

app = Flask(__name__)


# Read
@app.route('/')
def get_transactions():
    '''List all transactions.'''

    return render_template('transactions.html', transactions=transactions)


# Create
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    '''Add a transaction.'''

    # POST
    if request.method == 'POST':

        # create new transaction object and add it to transactions list
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(transaction)

        # redirect to the transactions list page
        return redirect(url_for('get_transactions'))

    # GET
    return render_template('form.html')


# Update
@app.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id: int):
    '''Edit a transaction.'''

    # POST
    if request.method == 'POST':

        date = request.form['date']
        amount = float(request.form['amount'])

        # update the matching ID transaction values
        index = {t['id']: t for t in transactions}
        if transaction_id in index:
            index[transaction_id]['date'] = date
            index[transaction_id]['amount'] = amount

        # redirect to the transactions list page
        return redirect(url_for('get_transactions'))

    # GET: find the matching ID transaction and render the edit form
    for t in transactions:
        if t['id'] == transaction_id:
            return render_template('edit.html', transaction=t)


# Delete
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id: int):
    '''Delete a transaction.'''

    # DELETE: find the matching ID transaction and remove it
    for t in transactions:
        if t['id'] == transaction_id:
            transactions.remove(t)
            break

    # redirect to the transactions list page
    return redirect(url_for('get_transactions'))


if __name__ == '__main__':
    app.run(debug=True)
