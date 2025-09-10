from flask import render_template, Blueprint, flash, redirect, url_for, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.forms import RegistrationForm, LoginForm, TransactionForm, BudgetForm, CSVUploadForm
from app.models import User, Transaction, Budget
from sqlalchemy import func
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import defaultdict
import io
import csv
from flask import Response

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', title='Home')

# ... (register, login, logout routes remain the same) ...

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# --- THIS IS THE FINAL, CORRECTED DASHBOARD ROUTE ---
@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # ... (Date Filter and Form submission logic remains the same) ...
    try:
        selected_month = int(request.args.get('month', datetime.utcnow().month))
        selected_year = int(request.args.get('year', datetime.utcnow().year))
    except (ValueError, TypeError):
        selected_month = datetime.utcnow().month
        selected_year = datetime.utcnow().year
        
    years = range(datetime.utcnow().year, datetime.utcnow().year - 5, -1)
    month_name = datetime(selected_year, selected_month, 1).strftime('%B')
    
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(amount=form.amount.data, type=form.type.data,
                                  category=form.category.data, date=form.date.data,
                                  description=form.description.data, owner=current_user)
        db.session.add(transaction)
        db.session.commit()
        flash('Your transaction has been added!', 'success')
        return redirect(url_for('main.dashboard', month=selected_month, year=selected_year))

    # ... (Pie Chart and Summary logic remains the same) ...
    total_income = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id, Transaction.type == 'income',
        func.extract('month', Transaction.date) == selected_month,
        func.extract('year', Transaction.date) == selected_year).scalar() or 0.0

    total_expenses = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id, Transaction.type == 'expense',
        func.extract('month', Transaction.date) == selected_month,
        func.extract('year', Transaction.date) == selected_year).scalar() or 0.0
    
    net_balance = total_income - total_expenses

    expense_data = db.session.query(
        Transaction.category, func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id, Transaction.type == 'expense',
        func.extract('month', Transaction.date) == selected_month,
        func.extract('year', Transaction.date) == selected_year).group_by(Transaction.category).all()
    
    expense_labels = [item[0] for item in expense_data]
    expense_values = [float(item[1]) for item in expense_data]
    
    # --- MODIFIED: BAR CHART LOGIC IS NOW DATABASE-AWARE ---
    six_months_ago = datetime.utcnow() - relativedelta(months=5)
    six_months_ago = six_months_ago.replace(day=1)

    # Check which database dialect is being used
    if db.get_engine().dialect.name == 'postgresql':
        date_format_str = func.to_char(Transaction.date, 'YYYY-MM')
    else: # Default to SQLite
        date_format_str = func.strftime('%Y-%m', Transaction.date)

    monthly_data_query = db.session.query(
        date_format_str.label('month_str'),
        Transaction.type,
        func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= six_months_ago
    ).group_by('month_str', Transaction.type).order_by('month_str').all()
    
    # ... (The rest of the bar chart and budget logic remains the same) ...
    monthly_totals = defaultdict(lambda: {'income': 0, 'expense': 0})
    for month_str, trans_type, total in monthly_data_query:
        month_dt = datetime.strptime(month_str, '%Y-%m')
        month_label = month_dt.strftime('%b \'%y')
        monthly_totals[month_label][trans_type] = float(total)

    bar_chart_labels = []
    income_data = []
    expense_data_bar = []
    for i in range(6):
        month = datetime.utcnow() - relativedelta(months=5-i)
        month_label = month.strftime('%b \'%y')
        bar_chart_labels.append(month_label)
        income_data.append(monthly_totals[month_label]['income'])
        expense_data_bar.append(monthly_totals[month_label]['expense'])
    
    budgets_query = Budget.query.filter_by(
        user_id=current_user.id, month=selected_month, year=selected_year).all()
    budgets_dict = {b.category: b.amount for b in budgets_query}

    spent_dict = dict(zip(expense_labels, expense_values))
    all_categories = set(expense_labels) | set(budgets_dict.keys())
    
    budget_progress = []
    for category in all_categories:
        spent = spent_dict.get(category, 0)
        budget = budgets_dict.get(category, 0)
        percentage = (spent / budget * 100) if budget > 0 else 0
        budget_progress.append({
            'category': category, 'spent': spent,
            'budget': budget, 'percentage': percentage
        })

    # MODIFIED: The transaction history table now filters by the selected month and year.
    transactions = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        func.extract('month', Transaction.date) == selected_month,
        func.extract('year', Transaction.date) == selected_year
    ).order_by(Transaction.date.desc()).all()
    
    return render_template('dashboard.html', title='Dashboard', form=form, transactions=transactions,
                           total_income=total_income, total_expenses=total_expenses, net_balance=net_balance,
                           expense_labels=expense_labels, expense_values=expense_values,
                           years=years, selected_month=selected_month, 
                           selected_year=selected_year, month_name=month_name,
                           bar_chart_labels=bar_chart_labels, income_data=income_data, 
                           expense_data_bar=expense_data_bar,
                           budget_progress=budget_progress)

# ... (all other routes for update, delete, budgets, import, export remain the same) ...

@main.route('/transaction/<int:transaction_id>/update', methods=['GET', 'POST'])
@login_required
def update_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.owner != current_user:
        abort(403)
    form = TransactionForm()
    if form.validate_on_submit():
        transaction.amount = form.amount.data
        transaction.type = form.type.data
        transaction.category = form.category.data
        transaction.date = form.date.data
        transaction.description = form.description.data
        db.session.commit()
        flash('Your transaction has been updated!', 'success')
        return redirect(url_for('main.dashboard'))
    elif request.method == 'GET':
        form.amount.data = transaction.amount
        form.type.data = transaction.type
        form.category.data = transaction.category
        form.date.data = transaction.date
        form.description.data = transaction.description
    form.submit.label.text = 'Update Transaction'
    return render_template('update_transaction.html', title='Update Transaction', form=form)


@main.route('/transaction/<int:transaction_id>/delete', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.owner != current_user:
        abort(403)
    db.session.delete(transaction)
    db.session.commit()
    flash('Your transaction has been deleted!', 'success')
    return redirect(url_for('main.dashboard'))


@main.route('/budgets', methods=['GET', 'POST'])
@login_required
def budgets():
    try:
        selected_month = int(request.args.get('month', datetime.utcnow().month))
        selected_year = int(request.args.get('year', datetime.utcnow().year))
    except (ValueError, TypeError):
        selected_month = datetime.utcnow().month
        selected_year = datetime.utcnow().year

    years = range(datetime.utcnow().year, datetime.utcnow().year - 5, -1)
    month_name = datetime(selected_year, selected_month, 1).strftime('%B')
    
    form = BudgetForm()
    if form.validate_on_submit():
        existing_budget = Budget.query.filter_by(
            user_id=current_user.id, category=form.category.data,
            month=selected_month, year=selected_year).first()
        
        if existing_budget:
            existing_budget.amount = form.amount.data
            flash('Budget for that category has been updated!', 'success')
        else:
            budget = Budget(category=form.category.data, amount=form.amount.data,
                            month=selected_month, year=selected_year, user_id=current_user.id)
            db.session.add(budget)
            flash('New budget has been set!', 'success')
            
        db.session.commit()
        return redirect(url_for('main.budgets', month=selected_month, year=selected_year))

    budgets = Budget.query.filter_by(user_id=current_user.id, month=selected_month, year=selected_year).all()
    
    return render_template('budgets.html', title='Budgets', form=form, budgets=budgets,
                           years=years, selected_month=selected_month, 
                           selected_year=selected_year, month_name=month_name)


@main.route('/budget/<int:budget_id>/delete', methods=['POST'])
@login_required
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    if budget.user_id != current_user.id:
        abort(403)
    
    month, year = budget.month, budget.year

    db.session.delete(budget)
    db.session.commit()
    flash('Budget has been deleted!', 'success')
    return redirect(url_for('main.budgets', month=month, year=year))

@main.route('/import_csv', methods=['GET', 'POST'])
@login_required
def import_csv():
    form = CSVUploadForm()
    if form.validate_on_submit():
        try:
            csv_file = io.TextIOWrapper(form.csv_file.data, encoding='utf-8')
            reader = csv.reader(csv_file)
            next(reader, None)
            transactions_to_add = []
            for row in reader:
                if len(row) < 4: continue
                transaction_date = datetime.strptime(row[0], '%Y-%m-%d').date()
                transaction_amount = float(row[1])
                transaction_type = row[2].lower()
                transaction_category = row[3]
                transaction_description = row[4] if len(row) > 4 else None
                if transaction_type not in ['income', 'expense']: continue
                transaction = Transaction(
                    date=transaction_date, amount=transaction_amount, type=transaction_type,
                    category=transaction_category, description=transaction_description,
                    owner=current_user)
                transactions_to_add.append(transaction)
            db.session.add_all(transactions_to_add)
            db.session.commit()
            flash(f'{len(transactions_to_add)} transactions have been successfully imported!', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred during import: {e}. Please check the file format.', 'danger')
    return render_template('import_csv.html', title='Import CSV', form=form)

@main.route('/export_csv')
@login_required
def export_csv():
    try:
        month = int(request.args.get('month', datetime.utcnow().month))
        year = int(request.args.get('year', datetime.utcnow().year))
    except (ValueError, TypeError):
        month = datetime.utcnow().month
        year = datetime.utcnow().year
    transactions = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        func.extract('month', Transaction.date) == month,
        func.extract('year', Transaction.date) == year
    ).order_by(Transaction.date.asc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Type', 'Category', 'Amount', 'Description'])
    for t in transactions:
        writer.writerow([t.date.strftime('%Y-%m-%d'), t.type, t.category, t.amount, t.description])
    output.seek(0)
    filename = f"transactions_{year}_{month:02d}.csv"
    return Response(
        output, mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={filename}"})

