#!/usr/bin/perl

$version = "version11";

eval
{
use LWP::UserAgent;
use URI::Escape;

#load up common variables and routines.
require "paypal_vars.cgi";
};
warn $@ if $@;

eval { &main; };                            # Trap any fatal errors so the program hopefully
if ($@) { &cgierr("fatal error: $@"); }     # never produces that nasty 500 server error page.
exit;   # There are only two exit calls in the script, here and in in &cgierr.

sub main
{
%variable = &parse_form;

#pass custom variables if any
#note: &custom2= question &custom1= querent
foreach $num (1..50)
        {
        if ($in{"custom$num"} ne '')
             {
             $temp = $in{"custom$num"};
             $custombulk = "$custombulk&custom$num=$temp";
             }
        }

#no email fail
if (! &valid_address($variable{'email'}))
        {
        print "Content-type: text/html\n\n";
        print "$variable{'email'} is not a valid email address to send the Tarot reading to. Please try again.\n\n";
        exit;
        };

print "Content-type: text/html\n\n";

print qq|

<HTML>
  <HEAD>
         <TITLE>Tarot Payment Form</TITLE>
  </HEAD>
  <BODY>

<!-- ************ Change the forms variable values below to suit your servers configuration. *************** -->

<!-- change ACTION to point to your paypal -->
<FORM NAME="TarotForm" ACTION="$paypalsite" METHOD="post">

<INPUT TYPE="hidden" NAME="amount" VALUE="$payment_amount"> <!--The amount we are charging-->
<INPUT TYPE="hidden" NAME="cmd" VALUE="$Paypal_cmd">
<INPUT TYPE="hidden" NAME="redirect_cmd" VALUE="$paypal_redirect_cmd">
<INPUT TYPE="hidden" NAME="business" VALUE="$paypaladdress"> <!--The email of the PayPal account we want to send the money too.-->
<INPUT TYPE="hidden" NAME="return" VALUE="$return_path"> <!--This generates the final page after PayPal processing. Modify it to suit your installation!-->
<INPUT TYPE="hidden" NAME="item_name" VALUE="$variable{'item_name'}">
<INPUT TYPE="hidden" NAME="notify_url" VALUE="$notify_path"> <!--This sends the Tarot reading to the visitor. Modify it to suit your installation!-->
<INPUT TYPE="hidden" NAME="mc_currency" VALUE="$currency"> <!--The currancy type. Set to Canadian in this example. See PayPal.com-->
<INPUT TYPE="hidden" NAME="currency_code" VALUE="$currency"> <!--The currancy type. Set to Canadian in this example. See PayPal.com-->
<INPUT TYPE="hidden" NAME="custom" VALUE="custom1=$variable{'custom1'}&custom2=$variable{'custom2'}&email=$variable{'email'}&databasepath=$variable{'databasepath'}&templatepath=$variable{'templatepath'}&vars=$variable{'vars'}$custombulk">

<p>Verify the following is correct, then click on the PayPal button to proceed.</p>

Name: $variable{'custom1'}
<br>
Question: $variable{'custom2'}
<br>
Email: $variable{'email'}

<p>This reading will cost $currency_character $payment_amount $currency</br>

<INPUT TYPE="image" SRC="$paypal_button" NAME="submit" ALT="Make payments with PayPal - it's fast, free and secure!">
<!--Submit button.-->
</FORM>

</BODY>
</HTML>

|;
};

exit;

sub cgierr {
# --------------------------------------------------------
# Displays any errors and prints out FORM and ENVIRONMENT
# information. Useful for debugging.
#
    if (!$html_headers_printed) {
        print "Content-type: text/html\n\n";
        $html_headers_printed = 1;
    }
    print "<PRE>\n\nCGI ERROR\n==========================================\n";
    $_[0]      and print "Error Message       : $_[0]\n";
    $0         and print "Script Location     : $0\n";
    $]         and print "Perl Version        : $]\n";

    print "\nForm Variables\n-------------------------------------------\n";
    foreach $key (sort keys %in) {
        my $space = " " x (20 - length($key));
        print "$key$space: $in{$key}\n";
    }
=pod
    print "\nEnvironment Variables\n-------------------------------------------\n";
    foreach $env (sort keys %ENV) {
        my $space = " " x (20 - length($env));
        print "$env$space: $ENV{$env}\n";
    }
=cut
    print "\n</PRE>";
    exit -1;
};

sub parse_form {
# --------------------------------------------------------
# Parses the form input and returns a hash with all the name
# value pairs. Removes SSI and any field with "---" as a value
# (as this denotes an empty SELECT field.

        my (@pairs, %in);
        my ($buffer, $pair, $name, $value);

        if ($ENV{'REQUEST_METHOD'} eq 'GET') {
                @pairs = split(/&/, $ENV{'QUERY_STRING'});
        }
        elsif ($ENV{'REQUEST_METHOD'} eq 'POST') {
                read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
                 @pairs = split(/&/, $buffer);
        }
        else {
                &cgierr ("This script must be called from the Web\nusing either GET or POST requests\n\n");
        }
        PAIR: foreach $pair (@pairs) {
                ($name, $value) = split(/=/, $pair);

                $name =~ tr/+/ /;
                $name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

                $value =~ tr/+/ /;
                $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

                $value =~ s/<!--(.|\n)*-->//g;                          # Remove SSI.
                if ($value eq "---") { next PAIR; }                  # This is used as a default choice for select lists and is ignored.
                (exists $in{$name}) ?
                        ($in{$name} .= "~~$value") :              # If we have multiple select, then we tack on
                        ($in{$name}  = $value);                                  # using the ~~ as a seperator.
        }
        return %in;
};

sub valid_address
 {
  $testmail = $_[0];
  if ($testmail =~/ /)
   { return 0; }
  if ($testmail =~ /(@.*@)|(\.\.)|(@\.)|(\.@)|(^\.)/ ||
  $testmail !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/)
   { return 0; }
   else { return 1; }
}