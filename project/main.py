# main.py

from flask import Blueprint, request,redirect, render_template,flash
from flask_login import login_required, current_user
import stripe
from .ML import *

stripe_keys = {
  'secret_key': os.environ['STRIPE_SECRET_KEY'],
  'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}
key=stripe_keys['publishable_key']

stripe.api_key = stripe_keys['secret_key']

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH=os.path.join(APP_ROOT, 'ML_models/colorful_model.h5')


model=load_model(MODEL_PATH)
global graph
graph = tf.get_default_graph()

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile',methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        upload=False
        # show the upload form
        return render_template('profile.html',upload=upload,name=current_user.name,key=key)

    if request.method == 'POST':
        # check if a file was passed into the POST request
        if 'image' not in request.files:
            upload = False
            flash('No file was uploaded. Payment stopped')
            return render_template('profile.html',upload=upload,name=current_user.name,key=key)

        image_file = request.files['image']


        if image_file.filename == '':
            upload = False
            flash('No file was uploaded. Payment stopped')
            return render_template('profile.html',upload=upload,name=current_user.name,key=key)


        if image_file:
            upload = False
            try:

                New_Photo=model_predict(image_file,model,graph)
                del image_file
                APP_ROOT = os.path.dirname(os.path.abspath(__file__))
                FILE_PATH = os.path.join(APP_ROOT, 'static/result/photo.png')
                if FILE_PATH.is_file():
                    os.remove(FILE_PATH)
                imsave(FILE_PATH, New_Photo)
                upload = True
            except Exception:
                upload=False

            if upload:
                try:
                    amount = 99 # amount in cents
                    customer = stripe.Customer.create(
                        email='sample@customer.com',
                        source=request.form['stripeToken']
                    )
                    stripe.Charge.create(
                        customer=customer.id,
                        amount=amount,
                        currency='usd',
                        description='Flask Charge'
                    )
                    return render_template('profile.html',upload=upload,name=current_user.name,key=key)
                except stripe.error.StripeError:
                    flash('Payment error, Payment stopped')
                    return render_template('profile.html',upload=upload,name=current_user.name,key=key)
            else:
                flash('An error occurred, try again., Payment stopped')
                return render_template('profile.html',upload=upload,name=current_user.name,key=key)

@main.route('/predict',methods=['POST'])
@login_required
def predict():
    image_url = url_for('static/result/result.png')
    return render_template(
        'predict.html',
        image_url=image_url
    )
