from market import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from market.models import Items, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route("/market", methods=['GET', 'POST'])
# Below decorator ensure that user is logged in before accessing market page...We can force unauthorized user to
# to land on login page by making change in __init__ file in login manager
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST':
        item_name = request.form.get('purchased_item')
        item_object = Items.query.filter_by(name=item_name).first()
        if item_object:
            if current_user.can_purchase(item_object):
                item_object.owner = current_user.id
                current_user.budget -= item_object.price
                db.session.commit()
                flash(f'Congrats! You have successfully purchased {item_name} for {item_object.price}$', category='success')
            else:
                flash(f"Sorry you don't have sufficient money to buy {item_name}.", category='danger')

        # Sell Item logic
        sold_item = request.form.get('sold_item')
        s_item_object = Items.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')
        return redirect(url_for('market_page'))


    # If you want to remove the items from the market after purchasing by any owner then enable the below code
    if request.method == 'GET':
        items = Items.query.filter_by(owner=None)
        owned_items = Items.query.filter_by(owner=current_user.id)
        #items = Items.query.all()

        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_add=form.email_address.data,
                              password=form.password1.data)
        # print(f'Just printing plain text user provided password from form before hashing> {form.password1.data}')
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully. You are now logged in as: {user_to_create.username}', category="success")
        return redirect(url_for('market_page'))
    if form.errors != {}:  # If error received from form validator class
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')

    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):

            login_user(attempted_user)
            flash(f'Welcome! You are now logged in as: {attempted_user.username}', category='success')

            return redirect(url_for('market_page'))

        else:
            flash(f'Username or password is incorrect. Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash(f'You have been logged out', category='info')
    return redirect(url_for('home_page'))


# dynamic routing example....here we can pass any dynamic value as string like below...that's what facebook does
@app.route("/about/<username>")
def about(username):
    return f'Hello {username} you are visiting about page'
