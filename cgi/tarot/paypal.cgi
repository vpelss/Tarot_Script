#!/usr/bin/perl

$version = "version11";

##################################################################
#
#  (C) Emogic Tarot Card Reader Paypal Module by The ScriptMan at http://www.somewhereincanada.com
#  This software is NOT FREEWARE!
#  To register it visit : http://www.emogic.com/scriptman/
#  You may not redistribute this script.
#
#######################################################################

use LWP::UserAgent;
use URI::Escape;

#load up common variables and routines.
require "paypal_vars.cgi";

#tell paypal we are ok so it will not attempt to notify us again and again and again
if ($ENV{'REQUEST_METHOD'}) { print "Content-type: text/html\n\n"; }

# PayPal Instant Payment Notification Script
# read post from PayPal system and add 'cmd=_notify-validate'
read (STDIN, $query, $ENV{'CONTENT_LENGTH'});
$query .= '&cmd=_notify-validate';

# post full "query + &cmd=_notify-validate" back to PayPal system to validate
#note that $query must be EXACTLY as PayPal sent it
$ua = new LWP::UserAgent;
$req = new HTTP::Request 'POST',$paypalsite;
$req->content_type('application/x-www-form-urlencoded');
$req->content($query);
$res = $ua->request($req); #result from PayPal are in $res based on our request $req

# split recieved variables from PayPal's first call, above, to paypal.cgi into pairs
#use the following code. other routines mess up query
@pairs = split(/&/, $query);
$count = 0;
foreach $pair (@pairs)
        {
        ($name, $value) = split(/=/, $pair);
        $value =~ tr/+/ /;
        $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
        $variable{$name} = $value;
        $count++;
        }

if ($res->is_error)
        {
        #HTTP error from PayPal site
        open (PayPalLog, ">>$PayPalLog");
        print PayPalLog "error $res->{status_line} \n";
        close PayPalLog;
        exit;
        }

if ($res->content eq 'INVALID')
        {
        #log for manual investigation
        open ACCOUNT, "$path_to_tarot_script/data/paypal/INVALID_$txn_id";
        print ACCOUNT "$item_name|$payment_status|$mc_gross|$payer_email|$custom";
        close ACCOUNT;
        exit;
        }

# assign PayPal variables to local variables
$item_name = $variable{'item_name'};
$receiver_email = $variable{'receiver_email'};
$custom = $variable{'custom'};
$payment_status = $variable{'payment_status'};
$mc_gross = $variable{'mc_gross'};
$txn_id = $variable{'txn_id'};
$payer_email = $variable{'payer_email'};

#check if user paid enough
if ($mc_gross < $payment_amount)
                {
                #user didn't pay us enough. No reading for them!
                open (PayPalLog, ">>$PayPalLog");
                print PayPalLog "$payer_email paid $mc_gross but we are charging $payment_amount. $txn_id: $tarotURL\?$custom \n";
                close PayPalLog;
                $mailresult=&sendmail($receiver_email , $receiver_email , $payer_email, $SMTP_SERVER, "Tarot reading error $payer_email", "You paid $mc_gross but we are charging $payment_amount");
                exit;
                }

if ($receiver_email ne "$paypaladdress") # check that receiver_email is our paypal account to prevent piggy back readings.
        {
        open (PayPalLog, ">>$PayPalLog") or die "Can't open $PayPalLog";
        print PayPalLog "$txn_id: $receiver_email is not our paypal account ($paypaladdress). Someone is trying to piggy back. \n";
        close PayPalLog;
        exit;
        }

# check that txn_id has not been previously processed
$pass = 1;
opendir(THEDIR, "$path_to_tarot_script/data/paypal/");
my @allfiles = readdir THEDIR;
closedir THEDIR;
foreach $line ( @allfiles )
        {
        if ($line =~ /$txn_id/) {$pass = 0};
        };
if ($pass == 0)
        {
        open (PayPalLog, ">>$PayPalLog");
        print PayPalLog "$txn_id: already existed. \n";
        close PayPalLog;
        exit;
        }

if (($payment_status eq "Completed")) # check the payment_status=Completed
        {
        #log the reading
        open (PayPalLog, ">>$PayPalLog");
        print PayPalLog "$txn_id: $tarotURL\?$custom \n";
        close PayPalLog;

        #print out a record of purchase
        open (TXN, ">$path_to_tarot_script/data/paypal/$txn_id");
        foreach $key ( keys %variable )
                {
                print TXN "$key : $variable{$key} <br>\n" ;
                };
        close TXN;

        #do tarot reading here by calling tarot.cgi
        $ENV{'REQUEST_METHOD'} = 'GET';
        $ENV{'QUERY_STRING'} = "$custom&password=$paypal_only_password"; # pass query string to $ENV{'QUERY_STRING'} so the &parse_form in tarot.cgi can process it!
        require "tarot.cgi"; #this actually calls and runs the tarot.cgi script

=pod
alternate
        #do tarot reading here by calling tarot.cgi url
        $query = uri_escape($custom,"^A-Za-z0-9\-_.!~*'()@&=");
        $ua = new LWP::UserAgent;
        $req = new HTTP::Request 'POST',"$tarotURL";
        $req->content_type('application/x-www-form-urlencoded');
        $req->content($query);
        $res = $ua->request($req);
=cut

        exit;
        }

#we should not make it to here
# unknown error
open (PayPalLog, ">$PayPalLog");
print PayPalLog "Made it to end of paypal.cgi error. Maybe pending payment\? $res->{status_line} \n";
close PayPalLog;