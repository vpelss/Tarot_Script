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
#$site_url = "http://home";
#required in spreadtemplate_email.html so URL is included in email readings
#Use the <%site_url%> in spreadtemplate_email.html like: <%site_url%><%card2%><%cardimage%>
#you may want to leave blank if mixed http:// and https:// access is required but you may need to modify templates and databse
#you MUST use if you will be emailing your readings. Or your images will not show.
#$site_url = "http://127.0.0.1";

$path_to_script = "TAROT_SCRIPT_PATH";
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
$templatepath{'focused'} = "../../tarot/spreads/email/focused.html";

$templatepath{'circle'} = "../../tarot/spreads/ocaat/circle.html";

#you need to create one for each new database and also create an entry in the initial index.html form
#$databasepath{'reference variable database in calling form index.html'} = "/home/emogic/public_html/tarot/databases/emogic.cgi";
$databasepath{'emogic'} = "../../tarot/databases/emogic.cgi";
$databasepath{'leila'} = "../../tarot/databases/leila.cgi ";

#head input, css, js, etc
$path_to_head = "../../tarot/spreads/head.html";

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
