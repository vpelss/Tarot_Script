##################################################
#
#Variables for (tarot.cgi and core.cgi) functionality
#
# used in:
# require "tarot.cgi";
#################################################

#only allow calls from these sites
@HTTP_REFERER = ();
#@HTTP_REFERER = ('127.0.0.1','www.emogic.com','www.somewhereincanada.com');

$site_url = "YOUR_SITE_URL";
#example $site_url = "https://www.emogic.com";
#required in spreadtemplate_email.html so URL is included in email readings
#Use the <%site_url%> in spreadtemplate_email.html like: <%site_url%><%card2%><%cardimage%>

$url_to_index = 'URL_TO_INDEX';

$short_path_to_script = "SHORT_PATH_TO_SCRIPT";
#example: "/public_html/cgi/tarot";

$full_path_to_script = "FULL_PATH_TO_SCRIPT";
#eg: "/home/emogic/public_html/cgi/tarot";

$short_path_to_index = "SHORT_PATH_TO_INDEX";

$full_path_to_index = "FULL_PATH_TO_INDEX";
#example: $path_to_index ="/home/emogic/public_html/tarot";

$path_to_input_archive = "$full_path_to_script/data/input_archive";
$path_to_delay_email = "$full_path_to_script/data/email_delay";
$path_to_email_archive = "$full_path_to_script/data/email_archive";

#you need to create one for each new spread and also create an entry in the initial index.html form
#$templatepath{'reference variable "template" in calling form index.html'} = "/home/emogic/public_html/tarot/spreads/three_card.html";
$templatepath{'three_card'} = "$full_path_to_index/spreads/email/three_card.html";
$templatepath{'relationship'} = "$full_path_to_index/spreads/email/relationship.html";
$templatepath{'celtic_cross'} = "$full_path_to_index/spreads/email/celtic_cross.html";
$templatepath{'golden_dawn'} = "$full_path_to_index/spreads/email/golden_dawn.html";
$templatepath{'focused'} = "$full_path_to_index/spreads/email/focused.html";

$templatepath{'circle'} = "$full_path_to_index/spreads/ocaat/circle.html";

#you need to create one for each new database and also create an entry in the initial index.html form
#$databasepath{'reference variable database in calling form index.html'} = "/home/emogic/public_html/tarot/databases/emogic.cgi";
$databasepath{'emogic'} = "$full_path_to_index/databases/emogic.cgi";
$databasepath{'leila'} = "$full_path_to_index/databases/leila.cgi ";

#head input, css, js, etc
$path_to_head = "$full_path_to_index/spreads/head.html";

#header
$path_to_header = "$full_path_to_index/spreads/header.html";

#footer
$path_to_footer = "$full_path_to_index/spreads/footer.html";


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
#$from = "Tarot Mailer wampserver@wampserver.invalid";

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
