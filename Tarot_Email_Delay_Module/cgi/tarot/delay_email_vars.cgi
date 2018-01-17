#NOTE: delay_email.cgi is to be run by a cron job. Suggested time; once an hour.
# cron job will look similar to:
# perl HTML_ROOT/cgi/tarot/delay_email.cgi >> email_delay.log

#permissions set to 777
$path_to_delay_email = "/home/boilover/public_html/cgi/tarot/data/email_delay";

#permissions set to 777
$path_to_email_archive = "/home/boilover/public_html/cgi/tarot/data/email_archive";

$SEND_MAIL= "/usr/lib/sendmail -t";
#example: $SEND_MAIL="/usr/lib/sendmail -t";

#$SMTP_SERVER="mail.yourdomain.com";
#use SMTP_SERVER if SEND_MAIL is unavailable, BUT NOT BOTH
#example: $SMTP_SERVER="mail.yourdomain.com";

#minimum hours to respond via email
$min_hours_to_respond = 1;

#maximum hours to respond via email
$max_hours_to_respond = 2;