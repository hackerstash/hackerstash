from flask import Blueprint, render_template, request

contact = Blueprint('contact', __name__)


@contact.route('/contact', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('contact/index.html')

    return render_template('contact/index.html')
