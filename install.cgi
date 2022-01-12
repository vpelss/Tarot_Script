#!/usr/bin/perl

##################################################################
#
#  (C)2002-2005 Emogic Tarot Card Reader Installation Script v8.1 by The ScriptMan at http://www.emogic.com.com
#  This software is NOT FREEWARE!
#  To register it visit : http://www.emogic.com/scriptman/
#  You may not redistribute this script.
#
#######################################################################

eval {
        use CGI qw/:standard/;
        use CGI::Cookie;
        use File::Copy;
        use File::Find;
	use lib '.'; #nuts, PERL has changed. add local path to @INC
        require "FileSystem.pm";
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
%in = &parse_form; #get arguments from the calling form

print "Content-type: text/html\n\n";

if ($in{remove}) {&remove; exit;};

if (%in == 0)
     {
     &novars;
     }
else
    {
    &vars;
    };

exit;
}

sub novars
{
#try and find some perl paths and settings....
$sendmail = `whereis sendmail`;
$plocation = `whereis perl`;
@perlloc = split(" ",$plocation);
@mailloc = split(" ",$sendmail);

print qq|
<B>Tarot Script Installation</B>

<p><b>IMPORTANT</b>: This automatic script will only install your script to run from http://www.yoursite.com/cgi/tarot (or cgi-bin) and  http://www.yoursite.com/tarot locations. It is a very basic install to get you up and running fast.
<br>For more detailed installations and other locations, you must manually install this script. If these folders already exist and contain files, it is suggested you make a backup before installation.

<P><b>If you are unsure, install the Tarot Script manually. We will not be responsible for data loss due to the use of install.cgi</b>

<p>
Perl Executable:$^X
<p>
Perl Version:$]
<p>
<form action="install.cgi">

Location of Perl:$perlloc[0]
<p>

<INPUT TYPE="TEXT" NAME="HTTP_HOST" Value="http://$ENV{HTTP_HOST}" size="40"> Server URL must be the base URL address with the preceding http:// eg: http://www.emogic.com
<P>
<INPUT TYPE="TEXT" NAME="SERVER_ADMIN" Value="$ENV{SERVER_ADMIN}" size="40"> Email Admin address that tarot readings will be sent from. <b>Must be in form of: youremail\\\@site.com</b>
<P>
<INPUT TYPE="TEXT" NAME="DOCUMENT_ROOT" Value="$ENV{DOCUMENT_ROOT}" size="40"> Document root. The FULL path to where HTML documents are located. eg: eg: /home/working/public_html
<P>
<INPUT TYPE="TEXT" NAME="TAROT_SCRIPT_PATH" Value="cgi/tarot" size="40"> Tarot script directory. Path where the Tarot script is to be located. (only cgi and cgi-bin is accepted) eg: cgi/tarot (script files will go to 'Document root/cgi/tarot')
<P>
<INPUT TYPE="TEXT" NAME="TAROT_HTML_PATH" Value="tarot" size="40"> Tarot directory. Path where the Tarot HTML documents are to be located. eg: tarot (will put HTML docs in 'Document root/tarot')
<P>
<INPUT TYPE="TEXT" NAME="INSTALL_SCRIPT_ROOT" Value="$ENV{SCRIPT_PATH}" size="40"> install.cgi Script path. The FULL path where this script and the data files are located. eg: /home/working/public_html/cgi/Tarot_Script
<P>

<INPUT TYPE="TEXT" NAME="sendmail" Value="$mailloc[1]" size="40"> Sendmail path. The path to where sendmail is located. <b>Usually /usr/lib/sendmail -t. The -t is strongly encouraged and may be required!</b>
<P>

<INPUT TYPE="SUBMIT" NAME="Submit1" value="Install Tarot Script">
</form>
|;

}

sub vars
{
$INSTALL_SCRIPT_ROOT = $in{INSTALL_SCRIPT_ROOT};
$TAROT_SCRIPT_ROOT = "$in{DOCUMENT_ROOT}/$in{TAROT_SCRIPT_PATH}";
$TAROT_ROOT = "$in{DOCUMENT_ROOT}/$in{TAROT_HTML_PATH}";

#copy all /cgi files to destination
print "Making $TAROT_SCRIPT_ROOT/ \n";
if (not -d "$TAROT_SCRIPT_ROOT/") {mkdir("$TAROT_SCRIPT_ROOT/" , 0777) or die("Can't make $TAROT_SCRIPT_ROOT/");};
print "<br>Done.<p> \n";
print "Copying $INSTALL_SCRIPT_ROOT/cgi/tarot/ to $TAROT_SCRIPT_ROOT/ \n";
&copyDir("$INSTALL_SCRIPT_ROOT/cgi/tarot/","$TAROT_SCRIPT_ROOT/") or die("Can't copy from $INSTALL_SCRIPT_ROOT/cgi/tarot/ to $TAROT_SCRIPT_ROOT/");
print "<br>Done.<p> \n";
#set the permission for tarot.cgi
chmod (0755,"$TAROT_SCRIPT_ROOT/tarot.cgi") or die('CHMOD of tarot.cgi failed.');

#copy all tarot html files to destination
print "Making $TAROT_ROOT/ \n";
if (not -d "$TAROT_ROOT/"){mkdir("$TAROT_ROOT/" , 0777) or die ("Can't make $TAROT_ROOT/");};
print "<br>Done.<p> \n";
print "Copying $INSTALL_SCRIPT_ROOT/tarot/ to $TAROT_ROOT/ \n";
&copyDir("$INSTALL_SCRIPT_ROOT/tarot/","$TAROT_ROOT/") or die("Can't copy $INSTALL_SCRIPT_ROOT/tarot/ to $TAROT_ROOT/");
print "<br>Done.<p> \n";

#modify file variables
#load tarot_vars.cgi
open (tarot_vars, "$TAROT_SCRIPT_ROOT/core_vars.pm") or die("Can't open $TAROT_SCRIPT_ROOT/core_vars.pm");
@tarot_vars= <tarot_vars>;
close tarot_vars;
$tarot_vars = join("" , @tarot_vars);

#replace variables in core_vars.pm
if ($in{SERVER_ADMIN} ne '') {$tarot_vars =~ s/EMAIL_ADDRESS/$in{SERVER_ADMIN}/g;} #email replace
if ($in{sendmail} ne '') {$tarot_vars =~ s/SENDMAIL_PATH/$in{sendmail}/g;} #$SEND_MAIL="SENDMAIL_PATH";
if ($in{HTTP_HOST} ne '') {$tarot_vars =~ s/YOUR_SITE_URL/$in{HTTP_HOST}/g;} #$site_url='YOUR_SITE_URL';
if ($TAROT_SCRIPT_ROOT ne '') {$tarot_vars =~ s/TAROT_SCRIPT_ROOT/$TAROT_SCRIPT_ROOT/g;} #$path_to_tarot_script = "TAROT_SCRIPT_ROOT";
if ($in{TAROT_SCRIPT_PATH} ne '') {$tarot_vars =~ s/TAROT_SCRIPT_PATH/$in{DOCUMENT_ROOT}\/$in{TAROT_SCRIPT_PATH}/g;} #TAROT_SCRIPT_PATH;
if ($in{TAROT_HTML_PATH} ne '') {$tarot_vars =~ s/TAROT_HTML_PATH/$in{TAROT_HTML_PATH}/g;} #TAROT_HTML_PATH;

#write modified tarot_vars.cgi
open (tarot_vars, ">$TAROT_SCRIPT_ROOT/core_vars.pm") or die("Can't write to $TAROT_SCRIPT_ROOT/core_vars.pm");
print tarot_vars $tarot_vars;
close tarot_vars;

=pod
#change /cgi/ if necessary in index.html
@list=('index.html','databases/emogic.cgi','databases/leila.cgi');

foreach $item (@list)
         {
         #read index.html
         open (htmlindex, "$TAROT_ROOT/$item") or die("Can't open $TAROT_ROOT/$item");
         @htmlindex = <htmlindex>;
         close htmlindex;
         $htmlindex = join("" , @htmlindex);

         #replace all paths with correct ones in all files!!!!
         $htmlindex =~ s/\<\%site_url\%\>\/tarot/\<\%site_url\%\>\/$in{TAROT_HTML_PATH}/gi;
         $htmlindex =~ s/cgi\/tarot/$in{TAROT_SCRIPT_PATH}/gi;
         $htmlindex =~ s/tarot\/spreads/$in{TAROT_HTML_PATH}\/spreads/gi;
         $htmlindex =~ s/tarot\/databases/$in{TAROT_HTML_PATH}\/databases/gi;
         $htmlindex =~ s/tarot\/tarot.css/$in{TAROT_HTML_PATH}\/tarot.css/gi;
         $htmlindex =~ s/tarot\/images/$in{TAROT_HTML_PATH}\/images/gi;

         #write new index.html file!
         open (htmlindex, ">$TAROT_ROOT/$item") or die("can't write to $TAROT_ROOT/$item");
         print htmlindex $htmlindex;
         close htmlindex;
         }
=cut

#set file permissions. not required?

print "<P>Finished.<P>Test Tarot script installation:<br>";
print "<p><a href='$in{HTTP_HOST}/$in{TAROT_HTML_PATH}/' target='_blank'>$in{HTTP_HOST}\/$in{TAROT_HTML_PATH}\/<\/a>";

print qq|
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>

<form action="install.cgi">
<P>
<INPUT TYPE="Hidden" NAME="remove" Value="1">
<INPUT TYPE="SUBMIT" NAME="Submit1" value="Remove installation folder and files in folder below">
<P>
BE SURE THE FOLDER BELOW IS THE ONE YOU WANT TO DELETE! If unsure, do it manually.
<P>
<INPUT TYPE="TEXT" NAME="INSTALL_SCRIPT_ROOT" Value="$INSTALL_SCRIPT_ROOT" size="40">
</form>
|;

}

sub remove
{
if ($in{INSTALL_SCRIPT_ROOT})
    {
    print "Removing installation files from $in{INSTALL_SCRIPT_ROOT}.";
    removeDir ($in{INSTALL_SCRIPT_ROOT});
    print "<p>Done.";
    }
else
    {
    print "No path was entered."
    };
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
}

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
    print "\nEnvironment Variables\n-------------------------------------------\n";
    foreach $env (sort keys %ENV) {
        my $space = " " x (20 - length($env));
        print "$env$space: $ENV{$env}\n";
    }
    print "\n</PRE>";
    exit -1;
}
