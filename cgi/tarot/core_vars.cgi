##################################################
#
#Variables for (tarot.cgi and core.cgi) functionality
#
# used:
# require "core.cgi";
#################################################

#only allow calls from these sites
@HTTP_REFERER = ();
#@HTTP_REFERER = ('127.0.0.1','www.emogic.com','www.somewhereincanada.com');

$site_url = "YOUR_SITE_URL";
#example $site_url = "https://www.emogic.com";
#$site_url = "YOUR_SITE_URL";
#required in spreadtemplate_email.html so URL is included in email readings
#Use the <%site_url%> in spreadtemplate_email.html like: <%site_url%><%card2%><%cardimage%>
#you may want to leave blank if mixed http:// and https:// access is required but you may need to modify templates and databse
#you MUST use if you will be emailing your readings. Or your images will not show.
#$site_url = "http://127.0.0.1";

$path_to_script = "TAROT_SCRIPT_PATH";
#$path_to_script = "TAROT_SCRIPT_PATH";
#example: $path_to_script ="/home/emogic/public_html/cgi/tarot";
#$path_to_script = "/home/emogic/public_html/cgi/tarot";

$path_to_input_archive = "$path_to_script/data/input_archive";

$path_to_delay_email = "$path_to_script/data/email_delay";

$path_to_email_archive = "$path_to_script/data/email_archive";

#you need to create one for each new spread and also create an entry in the initial index.html form
#$templatepath{'reference variable "template" in calling form index.html'} = "/home/emogic/public_html/tarot/spreads/three_card.html";
$templatepath{'three_card'} = "../../tarot/spreads/email/three_card.html";
$templatepath{'relationship'} = "../../tarot/spreads/email/relationship.html";
$templatepath{'celtic_cross'} = "../../tarot/spreads/email/celtic_cross.html";
$templatepath{'golden_dawn'} = "../../tarot/spreads/email/golden_dawn.html";
$templatepath{'tri'} = "../../tarot/spreads/email/custom.html";
$templatepath{'dotgo'} = "../../tarot/spreads/dotgo.html";

$templatepath{'three_card_ocaat'} = "../../tarot/spreads/ocaat/three_card.html";
$templatepath{'relationship_ocaat'} = "../../tarot/spreads/ocaat/relationship.html";
$templatepath{'celtic_cross_ocaat'} = "../../tarot/spreads/ocaat/celtic_cross.html";
$templatepath{'golden_dawn_ocaat'} = "../../tarot/spreads/ocaat/golden_dawn.html";
$templatepath{'circle'} = "../../tarot/spreads/ocaat/circle.html";

$templatepath{'three_card_mobile'} = "../../tarot/spreads/tablet/three_card_mobile.html";

$templatepath{'cfs'} = "../../cfs/spreads/chinesefortunesticks.html";
$templatepath{'ptf'} = "../../PictureTheFuture/spreads/ptf.html";

#you need to create one for each new database and also create an entry in the initial index.html form
#$databasepath{'reference variable database in calling form index.html'} = "/home/emogic/public_html/tarot/databases/emogic.cgi";
$databasepath{'emogic'} = "../../tarot/databases/emogic.cgi";
$databasepath{'leila'} = "../../tarot/databases/leila.cgi ";

$databasepath{'cfs'} = "../../cfs/databases/cfs.cgi ";
$databasepath{'ptf'} = "../../PictureTheFuture/databases/ptf.cgi ";

#header
$path_to_header = "../../tarot/spreads/header.html";

#footer
$path_to_footer = "../../tarot/spreads/footer.html";


$SEND_MAIL= "SENDMAIL_PATH";
#example: $SEND_MAIL="/usr/lib/sendmail -t";
#$SEND_MAIL= "SENDMAIL_PATH";

#$SMTP_SERVER="mail.yourdomain.com";
#use SMTP_SERVER if SEND_MAIL is unavailable, BUT NOT BOTH
#example: $SMTP_SERVER="mail.yourdomain.com";

$email_enabled = 1;
#set to 0 if you want to disable email tarot readings

$from = "Tarot Mailer EMAIL_ADDRESS";
#This will be in all Email from addresses
#example $from = "Tarot Mailer vpelss\@emogic.com";
#THE SLASH IS MANDITORY!
#$from = "Tarot Mailer EMAIL_ADDRESS";

$subject = "Your Tarot Reading";
#email subject. Note: The script adds the visitors name will show at the end

#set to 1 ONLY if you wish to delay emails sent.
#If set to 0 emails are sent immediately and no cron job is required
#see delay_email_var.cgi settings
#NOTE: delay_email.cgi is to be run by a cron job. Suggested time; once an hour.
# cron job will look similar to:
# perl HTML_ROOT/cgi/tarot/delay_email.cgi >> email_delay.log
$email_delayed = 0;

#template to show when delaying emails. must be full path for script
$email_delay_template = "../../tarot/spreads/emailwillbesent.html";
#example: $email_delay_template = "../../tarot/spreads/emailwillbesent.html"

##################
#PAYPAL Stuff
##################

#$paypalsite = 'https://www.paypal.com/cgi-bin/webscr';
$paypalsite = 'https://www.sandbox.paypal.com/cgi-bin/webscr';

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