# ColorLife
An application to add colors to portraiture photos !

## Getting started in 20 minutes

- Clone this repo
- Install requirements
- Configure Flask and Stripe Keys in your environment
- Run the script
- Check http://localhost:5000
- Done! :tada:


<p align="center">
  <img src="github/Home_Page" width="600px" alt="Home Page">
</p>

<p align="center">
  <img src="github/Login_Page" width="600px" alt="Login Page">
</p>

<p align="center">
  <img src="github/Profile_Page" width="600px" alt="Profile Page">
</p>

## Informations
1. Signup to use the app
2. Go to the profile page
3. Select the image you want to apply colors and click on the pay with card button
4. Stripe is in test mode (email: admin@admin.com, card number: 4242 4242 4242 4242, date: 12/20 and cvc 123)

## Local Installation

### Clone the repo
```shell
$ git clone https://github.com/cydessole/ColorLife.git
```

### Install requirements

```shell
$ pip install -r requirements.txt
```

### Environnment

```shell
$ FLASK_APP=project
$ export STRIPE_PUBLISHABLE_KEY=<YOUR_STRIPE_PUBLISHABLE_KEY>
$ export STRIPE_SECRET_KEY=<YOUR_STRIPE_SECRET_KEY>
```

### Run the script
You have to run this script in the github directory not in project
```shell
$ flask run
```
