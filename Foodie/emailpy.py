import global_config
from flask import Flask, render_template
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = global_config.get_config('gmail','username'),
	MAIL_DEFAULT_SENDER = global_config.get_config('gmail','username'),
	MAIL_PASSWORD = global_config.get_config('gmail','password')
	)
mail = Mail(app)

def send_mail(email_address, subject, location, cuisine, budget, restaurants):
	with app.app_context():
		try:
			msg = Message(subject,
			  recipients=[email_address])
			msg.html = render_template('email_template.html',
									   user=email_address.split('@')[0], 
									   cuisine=cuisine,
									   location=location,
									   budget=budget,
									   restaurants=restaurants)
			mail.send(msg)
			return True
		except Exception as e:
			print(e)
			return False

if __name__ == '__main__':
    import zomato_utils
    location = zomato_utils.get_valid_location('pune')
    print(location)
    cuisine = zomato_utils.get_valid_cuisine('chinese')
    print(cuisine)
    budget = zomato_utils.get_valid_budget('> 700')
    print(budget)
    top_10_restaurants = zomato_utils.get_top_restaurants_by_user_ratings(location['latitude'], location['longitude'], cuisine['cuisine_id'], budget['type'], top_n=10)
    print(top_10_restaurants)
    success = send_mail('keensam04@gmail.com', 'test', 'bengaluru', 'chinese', '> 700', top_10_restaurants)
    print(success)