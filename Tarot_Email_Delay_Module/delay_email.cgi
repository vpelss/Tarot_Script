#!/usr/bin/perl

##################################################################
#
#  (C) Emogic Tarot Card Reader Delay Email Module by The ScriptMan at http://www.somewhereincanada.com
#  This software is NOT to be sold!
#
#######################################################################

use File::Copy;

print "Content-type: text/html\n\n";

#NOTE: delay_email.cgi is to be run by a cron job. Suggested time; once an hour.
# cron job will look similar to:
# perl HTML_ROOT/cgi/tarot/delay_email.cgi >> email_delay.log

#permissions set to 777
#change to suit your file structure
$path_to_delay_email = "c:/home/cgi/tarot/data/email_delay";

#permissions set to 777
#change to suit your file structure
$path_to_email_archive = "c:/home/cgi/tarot/data/email_archive";

$SEND_MAIL= "/usr/lib/sendmail -t";
#example: $SEND_MAIL="/usr/lib/sendmail -t";

#$SMTP_SERVER="mail.yourdomain.com";
#use SMTP_SERVER if SEND_MAIL is unavailable, BUT NOT BOTH
#example: $SMTP_SERVER="mail.yourdomain.com";

#minimum hours to respond via email
$min_hours_to_respond = 1;

#maximum hours to respond via email
$max_hours_to_respond = 2;

unlink "$path_to_delay_email/placeholder.txt" || die('cant delete placeholder'); #remove placeholder.txt file from directory

# get all the emails waiting to be sent
opendir(THEDIR, "$path_to_delay_email/") || mkdir("$path_to_delay_email/", 0777) || die("Category directory $path_to_delay_email could not be opened or created.");
my @allfiles = readdir THEDIR;
closedir THEDIR;

foreach $filename (@allfiles)
        {
        #get date file was created
        $filedate = $filename;
        $filedate =~ s/\.txt//;

        $max_time_to_respond = $max_hours_to_respond * 60 * 60; #in seconds
        $min_time_to_respond = $min_hours_to_respond * 60 * 60; #in seconds

        #seed random routine
        srand(time ^ $$);
        $fudge_factor = int(rand($max_time_to_respond-$min_time_to_respond)); #in seconds
        $time_email_been_waiting = time() - $filedate; #time in seconds the email has been waiting
        $send_email_at = $min_time_to_respond + $fudge_factor;

        if ($time_email_been_waiting > $send_email_at) # are we ready to send yet?
             {
                #open file/email to send
                $file_to_send = "$path_to_delay_email/$filename";

                if (not -f $file_to_send) {next;} #skip directories, etc

                #read email we want to send
                open (DelayEmail , "$file_to_send") || die "Can't open $file_to_send";
                @filedata = <DelayEmail>;
                close DelayEmail;

               #send email
               $to = shift(@filedata);
               $to =~ s/\n//;
               $from = shift(@filedata);
               $from =~ s/\n//;
               $subject = shift(@filedata);
               $subject =~ s/\n//;

               while ($mg = shift(@filedata)) {$message = "$message$mg";}; #put rest of email into $message

               $mailresult=&sendmail($from , $from , $to, $SMTP_SERVER, $subject, $message);
               if ($mailresult ne "1")
                    {
                    print "MAIL NOT SENT. SMTP ERROR: $mailresult\nSendmail: $SEND_MAIL or SMTP Server: $SMTP_SERVER\n$file_to_send\nTO: $to\nFROM: $from\nSUBJECT: $subject\nMESSAGE: $message\n";
                    }
               else
                   {
                   #copy to email archive folder
                   copy($file_to_send ,"$path_to_email_archive/$filename");
                   unlink $file_to_send; #delete file!
                   print "\nfilename: $file_to_send sent\n"; #send data to log
                   }
               };
           };

exit;

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
