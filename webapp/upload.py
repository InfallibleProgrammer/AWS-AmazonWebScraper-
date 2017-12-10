from flask import Flask, request, render_template
from amazonHC import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def my_form_post():
    if request.method == 'POST':
        textsearch = request.form['textsearch']
        sort = request.form['sort']
        num = request.form['num']
        product_list = SearchList(textsearch, int(num))
        if sort == 'ascending':
             product_list = mergeSort(ascending_original, product_list)
             Product.all_data = mergeSort(ascending_original, Product.all_data)
        else:
            product_list = mergeSort(descending_original, product_list)
            Product.all_data = mergeSort(descending_original, Product.all_data)
        return render_template('results.html',
                                product_list = product_list,
                                all_data = Product.all_data,
                                )
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
