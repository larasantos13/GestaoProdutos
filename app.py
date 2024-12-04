import csv
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Caminho para o arquivo CSV
CSV_FILE = 'fashion_products.csv'

# Função para ler o arquivo CSV
def ler_estoque():
    produtos = []
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            produtos.append(row)
    return produtos

# Função para escrever no arquivo CSV
def escrever_estoque(produtos):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['User ID', 'Product ID', 'Product Name', 'Brand', 'Category', 'Price', 'Rating', 'Color', 'Size']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for produto in produtos:
            writer.writerow(produto)

# Rota inicial
@app.route('/')
def index():
    produtos = ler_estoque()
    return render_template('index.html', produtos=produtos)

# Rota para adicionar produto
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        user_id = request.form['user_id']
        product_id = request.form['product_id']
        product_name = request.form['product_name']
        brand = request.form['brand']
        category = request.form['category']
        price = float(request.form['price'])
        rating = float(request.form['rating'])
        color = request.form['color']
        size = request.form['size']

        # Lê os produtos existentes
        produtos = ler_estoque()

        # Adiciona o novo produto
        novo_produto = {
            'User ID': user_id,
            'Product ID': product_id,
            'Product Name': product_name,
            'Brand': brand,
            'Category': category,
            'Price': price,
            'Rating': rating,
            'Color': color,
            'Size': size
        }

        # Adiciona o novo produto à lista
        produtos.append(novo_produto)

        # Escreve de volta no arquivo CSV
        escrever_estoque(produtos)

        return redirect(url_for('index'))
    return render_template('adicionar.html')

# Rota para editar produto
@app.route('/atualizar/<string:product_id>', methods=['GET', 'POST'])
def atualizar(product_id):
    produtos = ler_estoque()
    produto = next((p for p in produtos if p['Product ID'] == product_id), None)
    
    if produto is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        produto['Product Name'] = request.form['product_name']
        produto['Brand'] = request.form['brand']
        produto['Category'] = request.form['category']
        produto['Price'] = float(request.form['price'])
        produto['Rating'] = float(request.form['rating'])
        produto['Color'] = request.form['color']
        produto['Size'] = request.form['size']

        # Escreve as alterações no arquivo CSV
        escrever_estoque(produtos)

        return redirect(url_for('index'))

    return render_template('atualizar.html', produto=produto)

# Rota para excluir produto
@app.route('/excluir/<string:product_id>', methods=['POST'])
def excluir(product_id):
    produtos = ler_estoque()
    produtos = [p for p in produtos if p['Product ID'] != product_id]

    # Escreve a lista atualizada no arquivo CSV
    escrever_estoque(produtos)

    return redirect(url_for('index'))

# Rota para pesquisar produto por Product ID
@app.route('/pesquisar', methods=['GET', 'POST'])
def pesquisar():
    if request.method == 'POST':
        product_id = request.form['product_id']  # Obtém o ID do formulário
        produtos = ler_estoque()

        # Busca o produto pelo Product ID
        produto = next((p for p in produtos if p['Product ID'] == product_id), None)

        return render_template('pesquisar.html', produto=produto, product_id=product_id)

    # Renderiza a página de pesquisa vazia no caso de GET
    return render_template('pesquisar.html', produto=None)


if __name__ == '__main__':
    # Verifica se o arquivo CSV existe, caso contrário cria um arquivo com cabeçalhos
    try:
        open(CSV_FILE, 'r')
    except FileNotFoundError:
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['User ID', 'Product ID', 'Product Name', 'Brand', 'Category', 'Price', 'Rating', 'Color', 'Size'])
            writer.writeheader()

    app.run(debug=True)

