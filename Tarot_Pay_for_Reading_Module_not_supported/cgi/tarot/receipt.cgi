#!/usr/bin/perl

$version = "version11";

eval {   # Trap any fatal errors so the program hopefully fails gracefully

require "paypal_vars.cgi";

%variable = &parse_form;

$payment_status = $variable{'payment_status'};

print "content-type: text/html\n\n";

print "<html>
<head>";

if ($variable{'mc_gross'} < $payment_amount)
                {
                #user didn't pay us enough. No reading for them!
                print "$variable{'payer_email'} paid $variable{'mc_gross'} but we are charging $payment_amount. <p>No reading sent.<p>\n";
                foreach $key ( keys %variable )
                        {
                        print "$key : $variable{$key} <br>\n" ;
                        };
                exit;
                }

if ($payment_status eq "Completed") {
        print "<title>Payment Received</title>
        </head>
        <body>
        <p>
        $variable{'first_name'}:<br><br>
        You made a payment in the amount of: \$$variable{'mc_gross'}<br>
        Transaction ID: $variable{'txn_id'}<br>
        <br>
        $payment_rx_message
        <p>
        </body>
        </html>";

foreach $key ( keys %variable )
                {
                print "$key : $variable{$key} <br>\n" ;
                };

        }
else {
        print "<title>Payment Pending</title>
        </head>
        <body>";

         print "
        $variable{'first_name'}, your payment is pending.<br><br>
        Your pending payment is in the amount of: \$$variable{'mc_gross'}<br>
        Transaction ID: $variable{'txn_id'}<br>
        <br>
        This payment may be pending because it was made by a check, and it has not yet cleared.<br><br>
        </body>
        </html>";

        foreach $key ( keys %variable ) {
                print "$key : $variable{$key} <br>\n" ;
                };
        }
};

if ($@) { &cgierr("fatal error: $@"); }     # never produces that nasty 500 server error page.

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