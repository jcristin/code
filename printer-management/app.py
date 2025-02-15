from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Printer, Seller, Client, Assignment, Issue
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///printer_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db.init_app(app)

# Criar as tabelas
with app.app_context():
    db.create_all()

# Rotas principais
@app.route('/')
def index():
    return render_template('index.html')

# Rotas para Impressoras
@app.route('/printers')
def list_printers():
    printers = Printer.query.all()
    return render_template('printers/list.html', printers=printers)

@app.route('/printers/new', methods=['GET', 'POST'])
def add_printer():
    if request.method == 'POST':
        printer = Printer(
            serial_number=request.form['serial_number'],
            model=request.form['model']
        )
        db.session.add(printer)
        try:
            db.session.commit()
            flash('Impressora registrada com sucesso!', 'success')
            return redirect(url_for('list_printers'))
        except:
            db.session.rollback()
            flash('Erro ao registrar impressora.', 'error')
    return render_template('printers/new.html')

# Rotas para Vendedores
@app.route('/sellers')
def list_sellers():
    sellers = Seller.query.all()
    return render_template('sellers/list.html', sellers=sellers)

@app.route('/sellers/new', methods=['GET', 'POST'])
def add_seller():
    if request.method == 'POST':
        seller = Seller(
            name=request.form['name'],
            email=request.form['email']
        )
        db.session.add(seller)
        try:
            db.session.commit()
            flash('Vendedor registrado com sucesso!', 'success')
            return redirect(url_for('list_sellers'))
        except:
            db.session.rollback()
            flash('Erro ao registrar vendedor.', 'error')
    return render_template('sellers/new.html')

# Rotas para Clientes
@app.route('/clients')
def list_clients():
    clients = Client.query.all()
    return render_template('clients/list.html', clients=clients)

@app.route('/clients/new', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        client = Client(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone'],
            address=request.form['address']
        )
        db.session.add(client)
        try:
            db.session.commit()
            flash('Cliente registrado com sucesso!', 'success')
            return redirect(url_for('list_clients'))
        except:
            db.session.rollback()
            flash('Erro ao registrar cliente.', 'error')
    return render_template('clients/new.html')

# Rotas para Atribuições
@app.route('/assignments')
def list_assignments():
    assignments = Assignment.query.all()
    return render_template('assignments/list.html', assignments=assignments)

@app.route('/assignments/new', methods=['GET', 'POST'])
def new_assignment():
    if request.method == 'POST':
        assignment = Assignment(
            printer_id=request.form['printer_id'],
            seller_id=request.form['seller_id'],
            client_id=request.form['client_id']
        )
        printer = Printer.query.get(request.form['printer_id'])
        printer.status = 'assigned'
        db.session.add(assignment)
        try:
            db.session.commit()
            flash('Impressora atribuída com sucesso!', 'success')
            return redirect(url_for('list_assignments'))
        except:
            db.session.rollback()
            flash('Erro ao atribuir impressora.', 'error')
    printers = Printer.query.filter_by(status='available').all()
    sellers = Seller.query.all()
    clients = Client.query.all()
    return render_template('assignments/new.html', printers=printers, sellers=sellers, clients=clients)

# Rotas para Devoluções
@app.route('/assignments/return/<int:id>', methods=['POST'])
def return_printer(id):
    assignment = Assignment.query.get_or_404(id)
    assignment.return_date = datetime.utcnow()
    assignment.status = 'returned'
    assignment.printer.status = 'available'
    try:
        db.session.commit()
        flash('Impressora devolvida com sucesso!', 'success')
    except:
        db.session.rollback()
        flash('Erro ao processar devolução.', 'error')
    return redirect(url_for('list_assignments'))

# Rotas para Problemas/Avarias
@app.route('/issues')
def list_issues():
    issues = Issue.query.all()
    return render_template('issues/list.html', issues=issues)

@app.route('/issues/new', methods=['GET', 'POST'])
def report_issue():
    if request.method == 'POST':
        issue = Issue(
            printer_id=request.form['printer_id'],
            description=request.form['description']
        )
        printer = Printer.query.get(request.form['printer_id'])
        printer.status = 'maintenance'
        db.session.add(issue)
        try:
            db.session.commit()
            flash('Problema registrado com sucesso!', 'success')
            return redirect(url_for('list_issues'))
        except:
            db.session.rollback()
            flash('Erro ao registrar problema.', 'error')
    printers = Printer.query.all()
    return render_template('issues/new.html', printers=printers)

@app.route('/issues/resolve/<int:id>', methods=['POST'])
def resolve_issue(id):
    issue = Issue.query.get_or_404(id)
    issue.resolved_date = datetime.utcnow()
    issue.status = 'resolved'
    issue.printer.status = 'available'
    try:
        db.session.commit()
        flash('Problema resolvido com sucesso!', 'success')
    except:
        db.session.rollback()
        flash('Erro ao resolver problema.', 'error')
    return redirect(url_for('list_issues'))

if __name__ == '__main__':
    app.run(debug=True)
