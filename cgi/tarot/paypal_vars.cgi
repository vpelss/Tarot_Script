###########################################################
#
#Variables for Tarot Script's paypal.cgi functionality. (purchased separately) (not required) (allows you to automaticly charge for a tarot reading)
#
###########################################################

$site_url = "";

$paypalsite = 'https://www.paypal.com/cgi-bin/webscr';
#$paypalsite = 'https://www.sandbox.paypal.com/cgi-bin/webscr';

$paypaladdress = "info\@yourpaypalemail.com";
#$paypaladdress = "vince\@vince.com";
#eg: $paypaladdress = "vince\@vince.com";
#Must be the PRIMARY PayPal email address where payments will be deposited
#The \ is MANDITORY

$payment_amount = '2.00';
# this will force a minimum payment in dollars. Visitors can always pay mor :)

$currency = "CAD";
#CAD = Canadian dollars USD = US dollars. See PayPal.com

$currency_character = '$';
#could be £ or other...

$notify_path = "$site_url/cgi/tarot/paypal.cgi";
#Paypal calls this routine first to verify payment, then to action.

$return_path = "$site_url/cgi/tarot/receipt.cgi";
#Paypal will give the user the option to return to this page

$paypal_only_password = '';
# Set to any password to block free readings
# Set to '' if you still will allow free readings at your site.

$payment_rx_message = "Your payment was recieved.<br>Your Tarot Reading will arrive in less than 24 hours.<br>Return to <a href='$site_url/tarot'>$site_url/tarot</a>";
#payment received message to show in reciept.cgi

$Paypal_cmd = '_ext-enter';
#paypal cmd value. do not modify

$paypal_redirect_cmd = '_xclick';
#paypal redirect_cmd value. do not modify

$paypal_button = 'http://images.paypal.com/images/x-click-but6.gif';

$PayPalLog = 'data/PayPalLog.txt';
#Eg: $PayPalLog = 'data/PayPalLog.txt';
#where paypal.cgi will log success and errors