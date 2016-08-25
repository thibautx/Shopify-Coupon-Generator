from app import db
from models import Discount
from flask import Blueprint, render_template, request
from shopify import Shopify

shopify = Shopify()

api_module = Blueprint('api', __name__, url_prefix='/api')

@api_module.route('/generate', methods=['POST'])
def generate_discount():
    if request.method == 'POST':
        discount = Discount(**request.form.to_dict())
        shopify.add_discount(discount)
        db.session.add(discount)
        db.session.commit()
        return render_template('index.html', code=discount.code)