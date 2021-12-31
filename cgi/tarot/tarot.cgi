#!/usr/bin/perl

$version = "version18";

##################################################################
#
#  (C) Emogic Tarot Card Reader
#  This software is NOT FREEWARE!
#  To register it visit : http://www.emogic.com/
#  You may not redistribute this script.
#
#######################################################################
#
# Form supplied VARIABLES

# Form supplied VARIABLES

# template
# database
# records 1,2,4
# custom5..50
# $custom1 - name of person seeking reading
# $custom2 - The question they are seeking an answer to
# $Email - the email address you want the tarot reading sent to. It is not required. If it is used you must have a valid $TemplateFile_email defined.

#troubleshooting try without -w

########################################################################

eval {
     use CGI;
        #for paypal
        use LWP::UserAgent;
        use URI::Escape;


        #load up common variables and routines. //houses &cgierr
	use lib '.'; #nuts, PERL has changed. add local path to @INC
        #require $in{vars};
        require "core_vars.cgi";
        #require "paypal_vars.cgi";

        };
warn $@ if $@;

if ($@) {
    print "Content-type: text/plain\n\n";
    print "Error including libraries: $@\n";
    print "Make sure they exist, permissions are set properly, and paths are set correctly.";
    exit;
}

eval { &main; };                            # Trap any fatal errors so the program hopefully
if ($@) { &cgierr("fatal error: $@"); }     # never produces that nasty 500 server error page.
exit;   # There are only two exit calls in the script, here and in in &cgierr.

sub main
{
#get arguments from the calling form
 my $q = CGI->new;
 %in = $q->Vars;

#try and sanitize inputs to avoid xss
foreach $key (keys %in) {
         $in{$key} =~ s/[^A-Za-z0-9\.\@\_\, ]*//g;
         }
#$text =~ s/[^A-Za-z0-9 ]*/ /g;

#open file to archive questions
$filename = "$path_to_input_archive/input_archive.txt";
open (QARCHIVE, ">>$filename") or die ("Can't open $filename");
foreach $item (keys %in) #build up all input keys
         {
         $build = "$build , ( $item=$in{$item} )";
         }
print QARCHIVE "$build\n";
close QARCHIVE;

#called from valid site including paypal!
$temp = 0; #fail
foreach $item (@HTTP_REFERER)
         {
         if ($ENV{'HTTP_REFERER'} =~ /^http:|^https:\/\/$item/) {$temp = 1}
         }
if ((@HTTP_REFERER != ()) and ($temp == 0))
      {
      print "Content-type: text/html\n\n";
      print "Bad HTTP_REFERER : $ENV{'HTTP_REFERER'}";
      print '\n\n';
      exit;
      }

 if ( ($ENV{'HTTP_REFERER'} =~ /^http:\/\/www.paypal.com/) or ($ENV{'HTTP_REFERER'} =~ /^https:\/\/www.paypal.com/) )
      {#call from paypal, respond to paypal
      &paypal();
      }

#GET our tarot deck
#open (DATABASE, "$in{databasepath}") || die("no database file at $in{databasepath}");
open (DATABASE, "$databasepath{$in{database}}") || die("no deck path at $databasepath{$in{database}} $in{database}");
@db= <DATABASE>;
close DATABASE;

#build a hash %db_def of the field names and positions eg: #field_name => ['position']
@field_names_array  = split(/\|/,$db[0]); #this is a list of all database field names from first line of database
shift @db; #remove fields name from deck database
$field_count = @field_names_array;
foreach $field (0..($field_count - 1)) #create field hash %db_def of the field names eg: #field_name => ['position']
         {
         $fn = $field_names_array[$field];
         $fn =~ s/\n//;
         $fn =~ s/\r//;
         $db_def{$fn} = $field;
         }

@db = grep(/\w/, @db); #remove blank lines in db!!!

#load page template , header and footer
#put em all together
#open (PAGETEMPLATESOURCE, "$in{templatepath}") || die("no template file at $in{templatepath}");
open (PAGETEMPLATESOURCE, "$templatepath{$in{template}}") || die("no template path at $templatepath{$in{template}}");
open (HEADERESOURCE, "$path_to_header") || die("no header at $path_to_header");
open (FOOTERSOURCE, "$path_to_footer") || die("no footer at $path_to_footer");
$header = join("" , <HEADERESOURCE> );
$pagetemplate = join("" , <PAGETEMPLATESOURCE>);
#$pagetemplate = join("" , <HEADERESOURCE> , <PAGETEMPLATESOURCE> , <FOOTERSOURCE>);
$footer = join("" , <FOOTERSOURCE>);
close FOOTERSOURCE;
close HEADERSOURCE;
close PAGETEMPLATESOURCE;

$pagetemplate =~ s/\<\%header\%\>/$header/g; #replace all <%header%> tokens
$pagetemplate =~ s/\<\%footer\%\>/$footer/g; #replace all <%footer%> tokens

if ($email_delayed)
   {
   #load page template
   open (PAGETEMPLATESOURCE, "$email_delay_template") || die("no template file at $in{templatepath}");
   $delay_email_template = join("" , <PAGETEMPLATESOURCE>);
   close PAGETEMPLATESOURCE;
   }

#clear @cards that will be selected
#this variable will hold the cards we select and put them in a cookie
@records = ();

# @pickedcards is global array containing picked cards so we don't pick same card twice
# it will contain the picked cards card number .
@pickedcards = ();
# global array containing picked record (lines in deck.txt) so we don't pick same record twice
@pickedrecord = ();

#case where we are forcing records from &records=7,8,9 in url
@records = split(',' , $in{records});

# number of records in deck
$recordcount = @db;
$numberofrecordslefttopick = $recordcount ;

# create a list of all available token types
# the $token list will then be card1 to card20 as there should be no need to have more than 20 cards layed out
@alltokentypes = ();
foreach $num (1..50)
        {
        push @alltokentypes , "<\%object$num\%>";
        }

# create a list of all possible custom token types
#used to allow users to create their own spreads
# the $token list will then be custom1 to custom20 as there should be no need to have more than 20 custom tokens layed out
@allcustomtypes = ();
foreach $num (1..50)
        {
        push @allcustomtypes , "custom$num";
        }

#seed random routine
srand(time ^ $$);

#%cookies = fetch CGI::Cookie;

#get the yummy cookies!
# cookies are seperated by a comma and a space, this will
# split them and return a hash of cookies
@rawCookies = split(/; /,$ENV{'HTTP_COOKIE'});
#%cookies;
    foreach(@rawCookies)
      {
      ($key, $val) = split (/=/,$_);
      $key =~ s/%([A-Fa-f\d]{2})/chr hex $1/eg; #unescape cookie data!
      $val =~ s/%([A-Fa-f\d]{2})/chr hex $1/eg; #unescape cookie data!
      $val =~ s/[^A-Za-z0-9\.\@\_\,]*//g; #sanitize to avoid xss
      $cookies{$key} = $val;
      }

#if there were cookies then we are still in the same day so we show the cookie cards and do not need to pick random ones below
#base cookie on username , question , and templatefile name (spread)
#remember no space in cookie name!
$NameQuestionPaths = join('' , $in{'custom1'} , $in{'custom2'} , $in{'template'}, $in{'database'});

#see if we have a cookie set for this name and question. If so call &replacetokens() with each card in list
#note: list of cards is integers of card number seperated by '|'
if ($cookies{$NameQuestionPaths} ne "")
     {
        #use cards from cookie
        #cards are seperated by |
        @records = split(',' , $cookies{$NameQuestionPaths});
        }
else
    {
    #this is where we select random cards if we don't already have cookie cards
    #for each $token type generated, pick a card and replace it in the html template
    foreach $tokentype ( @alltokentypes )
        {
        if (&thereisatokeninpagetemplate($tokentype,$pagetemplate)) #see if the $token exists in the html template. if so, replace it
                {
                $recordnumber = &pickacard();# this returns a random card from deck.cgi. It keeps track of cards already picked and does not return those.
                if ($recordnumber == -1) {last;} #if out of cards break out
                @records = (@records , $recordnumber); #remember cards for users cookie
                }
        }
    }

#pass custom variables if any
#note:&custom2=$in{'Question'}&custom1=$in{Querent}
foreach $num (1..50)
        {
        if ($in{"custom$num"} ne '')
             {
             $temp = $in{"custom$num"};
             $custombulk = "$custombulk&custom$num=$temp";
             }
        }

#replace database tokens
$count = 0;
foreach $temp (@records) #note that each $tmpcard from the cookie is really a record number in our deck.cgi database
                {
                #we have to generate the <%object1%> tokens, etc
                $token = $alltokentypes[$count];
                $count = $count + 1;
                &replacetokens($temp , $token , $pagetemplate); #replace all occurances of the $token in the $pagetemplate
                }

#replace global variables in $pagetemplate
$pagetemplate =~ s/\<\%site_url\%\>/$site_url/g; #replace all <%site_url%> tokens
$pagetemplate =~ s/\<\%databasepath\%\>/$databasepath{$in{database}}/g; #replace all <%databasepath%> tokens
$pagetemplate =~ s/\<\%templatepath\%\>/$templatepath{$in{template}}/g; #replace all <%templatepath%> tokens
$pagetemplate =~ s/\<\%database\%\>/$in{database}/g; #replace all <%database%> tokens
$pagetemplate =~ s/\<\%template\%\>/$in{template}/g; #replace all <%template%> tokens

#records can be placed in the template under
$recordsjoined = join(',' , @records);
$pagetemplate =~ s/\<\%records\%\>/$recordsjoined/g; #replace all <%records%> tokens

#replace all custom types on page
foreach $customtype ( @allcustomtypes )
        {
        my $temp = $in{$customtype};
        $temp =~ s/\<.\>//g;# remove xss stuff
        $pagetemplate =~ s/\<\%$customtype\%\>/$temp/g; #replace all <%customXX%> tokens
        }

if ( &valid_address($in{'email'}) && ($email_enabled) ) #see if the forms email variable exist
        {
        $message = $pagetemplate;

        $time = time();
        $filename = "$time.txt";

        $email_package = "$in{'email'}\n$from\n$subject\n\n$message\n.\n";

        if ($email_delayed)
                {
                open (emailDelay, ">$path_to_delay_email/$filename");
                print emailDelay $email_package;
                close emailDelay;
               #later run delay_email.cgi using a cron job
                }
        else
                {
                if (($SEND_MAIL ne "") || ($SMTP_SERVER ne ""))
                       {
                       $mailresult=&sendmail($from , $from , $in{'email'}, $SMTP_SERVER, "$subject", $message);
                       if ($mailresult ne "1") {
                             print "Content-type: text/html\n\n";
                             print "MAIL NOT SENT. SMTP ERROR: $mailcodes{'$mailresult'}<br>Sendmail: $SEND_MAIL or SMTP Server: $SMTP_SERVER @mailloc\n<br><$sendmail>";
                             exit;
                             }
                       open (emailArchive, ">$path_to_email_archive/$filename");
                       print emailArchive $email_package;
                       close emailArchive;
                     }
                }
      }

#choose what to print to screen.
if ($email_delayed) {$pagetemplate = $delay_email_template};
&print_screen($pagetemplate);

};
#end of main routine
#end of main routine
#end of main routine
#end of main routine
#end of main routine
#end of main routine
#end of main routine
#end of main routine
#end of main routine

sub thereisatokeninpagetemplate{
#take the $tokentype argument given
#see if token exists on pagetemplate.html
#if so return 1, if not return 0

my ($token);

$token = $_[0];
return ($_[1] =~ m/$token/) or 0;
};

sub pickacard(){
#this routine gets a unique random record returned from &pickarecord() and gets the records cardnumber
#it sees if card has been chosen, and if it has, tries again
#if the record has not been chosen, it returns the RECORDNUMBER!!!!! not the card number. The data is stored in records!
# if &pickarecord() returns -1 this routine will return -1 indicating no more cards

# $cardpicked = 1 means that the card has been picked
$cardpicked = 0;
while ($cardpicked == 0)
        {
        #get an availabele random record
        $chosenrecord = &pickarecord();

        #any cards left?
        if ($chosenrecord == -1)
                {
                #no more cards. Return 0
                return -1;
                }

        #get the card number from the record
        $deckline = $db[$chosenrecord];
        ($cardnumber) = split(/\|/,$deckline);

        #has this card been used?
        if ($pickedcards[$cardnumber] == 0)
                {
                #card has not been chosen before. choose it and tell everyone about it. return it!
                $pickedcards[$cardnumber] = 1;
                $cardpicked = 1;
                }
        }

return $chosenrecord;
};

sub pickarecord(){
#this chooses a random number from 1 to @deck (numbet of deck.txt records), and returns it.
#it will only return each record number once by using @recordpicked
#if all records have been tried, it returns -1

# $recordpicked = 1 means that the card has been picked
$recordpicked = 0;
while ($recordpicked == 0)
        {
        #assume record will be picked
        $recordpicked = 1;

        #pich a random number within range
        $temppick = int(rand($recordcount));

        #have we picked this record before?
        if ($pickedrecord[$temppick] == 0)
                {
                #record has not been picke before. go ahead and pick it
                #mark it a picked
                $pickedrecord[$temppick] = 1;
                #break out of while loop
                $recordpicked = 1;
                #count number of records picked so we can notify
                $numberofrecordslefttopick = $numberofrecordslefttopick - 1 ;
                }
        }

#return 0 and if no available records left
if ($numberofrecordslefttopick <= 0)
        {
        $temppick = -1;
        }

return $temppick;
};

sub cgierr {
# --------------------------------------------------------
# Displays any errors and prints out FORM and ENVIRONMENT
# information. Useful for debugging.
#
    if (!$html_headers_printed) {
        print "Content-type: text/html\n\n";
        $html_headers_printed = 1;
    }
    print "OK <PRE>\n\nCGI ERROR\n==========================================\n";
    $_[0]      and print "Error Message       : $_[0]\n";
    $0         and print "Script Location     : $0\n";
    #$]         and print "Perl Version        : $]\n";

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

sub replacetokens{
# arguments: card database record number , first half of token to replace in pagetemplate , pagetemplate passed by reference
#take the given record number, exctract all record data
#replace all possible tokens in pagetemplate
#return by reference only
my ($selected , $pick);

#get argument value (card number picked) (1 to @deck(number of deck.txt records))

$pick = $_[0];
$token = $_[1]; #use the token fed from the functions second argument
# $_[2] will be the selected $pagetemplate and modified by reference

#this is the random record chosen
$selected = $db[$pick];

#get all picked card record data out of $selected
@record  = split(/\|/,$selected);

#replace all tokens based on columns #'s named in %db_def
# %db_def is PosnName => Column #
foreach $key ( keys %db_def ) {
        $replaceme = $record[$db_def{$key}];
        $_[2] =~ s/$token\<\%$key\%\>/$replaceme/g;
        };
};

sub print_screen
{
print "Content-type:text/html\n\n";

#print @alltokentypes;
#print @records;
print $_[0];
print "\n\n";
print "\n\n";
print "\n\n";

#scent our script
print qq|
<!--Script by Emogic http://www.emogic.com/-->
|;
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

sub bad_email
{
print qq|

Content-type: text/html

<FONT SIZE="+1">
<B>
SORRY! Your request could not be processed because of an
improperly formatted e-mail address. Please use your browser's
back button to return to the form entry page.
</B>
</FONT>

|;
}

sub sendmail  {
# error codes below for those who bother to check result codes <gr>
# 1 success
# -1 $smtphost unknown
# -2 socket() failed
# -3 connect() failed
# -4 service not available
# -5 unspecified communication error
# -6 local user $to unknown on host $smtp
# -7 transmission of message failed
# -8 argument $to empty
#
#  Sample call:
#
# &sendmail($from, $reply, $to, $smtp, $subject, $message );
#
#  Note that there are several commands for cleaning up possible bad inputs - if you
#  are hard coding things from a library file, so of those are unnecesssary
#

    my ($fromaddr, $replyaddr, $to, $smtp, $subject, $message) = @_;

    $to =~ s/[ \t]+/, /g; # pack spaces and add comma
    $fromaddr =~ s/.*<([^\s]*?)>/$1/; # get from email address
    $replyaddr =~ s/.*<([^\s]*?)>/$1/; # get reply email address
    $replyaddr =~ s/^([^\s]+).*/$1/; # use first address
    $message =~ s/^\./\.\./gm; # handle . as first character
    $message =~ s/\r\n/\n/g; # handle line ending
    $message =~ s/\n/\r\n/g;
    $smtp =~ s/^\s+//g; # remove spaces around $smtp
    $smtp =~ s/\s+$//g;

    if (!$to)
    {
        return(-8);
    }

 if ($SMTP_SERVER ne "")
  {
    my($proto) = (getprotobyname('tcp'))[2];
    my($port) = (getservbyname('smtp', 'tcp'))[2];

    my($smtpaddr) = ($smtp =~
                     /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/)
        ? pack('C4',$1,$2,$3,$4)
            : (gethostbyname($smtp))[4];

    if (!defined($smtpaddr))
    {
        return(-1);
    }

    if (!socket(MAIL, AF_INET, SOCK_STREAM, $proto))
    {
        return(-2);
    }

    if (!connect(MAIL, pack('Sna4x8', AF_INET, $port, $smtpaddr)))
    {
        return(-3);
    }

    my($oldfh) = select(MAIL);
    $| = 1;
    select($oldfh);

    $_ = <MAIL>;
    if (/^[45]/)
    {
        close(MAIL);
        return(-4);
    }

    print MAIL "helo $SMTP_SERVER\r\n";
    $_ = <MAIL>;
    if (/^[45]/)
    {
        close(MAIL);
        return(-5);
    }

    print MAIL "mail from: <$fromaddr>\r\n";
    $_ = <MAIL>;
    if (/^[45]/)
    {
        close(MAIL);
        return(-5);
    }

    foreach (split(/, /, $to))
    {
        print MAIL "rcpt to: <$_>\r\n";
        $_ = <MAIL>;
        if (/^[45]/)
        {
            close(MAIL);
            return(-6);
        }
    }

    print MAIL "data\r\n";
    $_ = <MAIL>;
    if (/^[45]/)
    {
        close MAIL;
        return(-5);
    }

   }

  if ($SEND_MAIL ne "")
   {
     open (MAIL,"| $SEND_MAIL");
   }

    print MAIL "To: $to\n";
    print MAIL "From: $fromaddr\n";
    #print MAIL "Reply-to: $replyaddr\n" if $replyaddr;
    print MAIL "Subject: $subject\n";
    print MAIL qq|Content-Type: text/html; charset="iso-8859-1"
   Content-Transfer-Encoding: quoted-printable
   |
   ;
    print MAIL "\n\n";
    #print MAIL 'Mime-Version: 1.0'."\n";
    #print MAIL 'content-type:' . "text/HTML\n\n"; # <----------------- put the double \n\n here
    #print MAIL "Content-Transfer-Encoding: quoted-printable\n\n";

    print MAIL "$message";

    print MAIL "\n.\n";

 if ($SMTP_SERVER ne "")
  {
    $_ = <MAIL>;
    if (/^[45]/)
    {
        close(MAIL);
        return(-7);
    }

    print MAIL "quit\r\n";
    $_ = <MAIL>;
  }

    close(MAIL);
    return(1);
}

sub paypal
{
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
      }

#see if we are in a pay for reading mode only
if ($paypal_only_password ne '')
        {
        #$in{'password'} is created in paypal.cgi from tarot_vars.cgi. $paypal_only_password is in tarot_vars.cgi.
        if ($paypal_only_password ne $in{'password'})
                {
                open (ErrorLog, ">>data/ErrorLog.txt") or die "Can't open $file_to_send";
                print ErrorLog "Call might not be from paypal.cgi Referer: $ENV{HTTP_REFERER} $paypal_only_password <> $in{'password'}\n";
                close ErrorLog;
                print "Content-type:text/html\n\n";
                die ("This is a pay for tarot site. Call not from paypal.cgi Referer: $ENV{HTTP_REFERER}\n");
                exit;
                }

        }
}
