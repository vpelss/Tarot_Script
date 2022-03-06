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
		use strict;
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

#set in main
my $SHORT_PATH_TO_SCRIPT;
my $FULL_PATH_TO_SCRIPT;
my $URL_TO_SCRIPT;
my $SHORT_PATH_TO_INDEX;
my $FULL_PATH_TO_INDEX;
my $URL_TO_INDEX;
my $FULL_PATH_TO_INSTALL_SCRIPT;

eval { &main; };                            # Trap any fatal errors so the program hopefully
if ($@) { &cgierr("fatal error: $@"); }     # never produces that nasty 500 server error page.
exit;   # There are only two exit calls in the script, here and in in &cgierr.

sub main
{
%in = &parse_form; #get arguments from the calling form

$SHORT_PATH_TO_SCRIPT = $in{'SHORT_PATH_TO_SCRIPT'};
$FULL_PATH_TO_SCRIPT = "$in{'DOCUMENT_ROOT'}/$SHORT_PATH_TO_SCRIPT";
$URL_TO_SCRIPT = "$in{'HTTP_HOST'}/$SHORT_PATH_TO_SCRIPT";
$SHORT_PATH_TO_INDEX = $in{'SHORT_PATH_TO_INDEX'};
$FULL_PATH_TO_INDEX = "$in{'DOCUMENT_ROOT'}/$SHORT_PATH_TO_INDEX";
$URL_TO_INDEX = "$in{'HTTP_HOST'}/$SHORT_PATH_TO_INDEX";
$FULL_PATH_TO_INSTALL_SCRIPT = $in{'FULL_PATH_TO_INSTALL_SCRIPT'};

print "Content-type: text/html\n\n";

if ($in{remove}) {&remove; exit;};

if (%in == 0){
     &novars;
     }
else{
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

$Tarot_Script_Path = Cwd::cwd();

print qq|
<B>Tarot Script Installation</B>

<p><b>WE WILL NOT BE RESPONSIBLE FOR DATA LOSS DUE TO THE USE OF install.cgi</b></p>

<P><b>If you are unsure, install the Tarot Script manually.<b></p>

<p><b>IMPORTANT</b>: This automatic script will only install your script to run from http://www.yoursite.com/cgi/tarot (or cgi-bin) and  http://www.yoursite.com/tarot locations. It is a very basic install to get you up and running fast.
<br>For more detailed installations and other locations, you must manually install this script. If these folders already exist and contain files, it is suggested you make a backup before installation.

<p>
Perl Executable:$^X
<p>
Perl Version:$]
<p>

<form action="install.cgi">

Location of Perl:$perlloc[0]
<p>

<INPUT TYPE="TEXT" name="HTTP_HOST" Value="https://$ENV{HTTP_HOST}" size="40"> Server URL must be the base URL address with the preceding https:// eg: https://www.emogic.com
<P>
<INPUT TYPE="TEXT" name="SERVER_ADMIN" Value="$ENV{SERVER_ADMIN}" size="40"> Email Admin address that tarot readings will be sent from. <b>Must be in form of: youremail\\\@site.com</b> DO NOT FORGET THE \\
<P>
<INPUT TYPE="TEXT" name="DOCUMENT_ROOT" Value="$ENV{DOCUMENT_ROOT}" size="40"> Document root. The FULL path to where HTML documents are located. eg: eg: /home/working/public_html
<P>
<INPUT TYPE="TEXT" name="SHORT_PATH_TO_SCRIPT" Value="cgi/tarot" size="40"'> Tarot script directory. Path where the Tarot script is to be located. (only cgi and cgi-bin is accepted) eg: cgi/tarot (script files will go to '[Document root]/cgi/tarot')
<P>
<INPUT TYPE="TEXT" name="SHORT_PATH_TO_INDEX" Value="tarot" size="40"> Tarot directory. Path where the Tarot HTML documents are to be located. eg: tarot (will put HTML docs in '[Document root]/tarot')
<P>
<INPUT TYPE="TEXT" name="FULL_PATH_TO_INSTALL_SCRIPT" Value="$Tarot_Script_Path" size="40"> install.cgi Script path. The FULL path where this script and the data files are located. eg: /home/working/public_html/cgi/Tarot_Script
<P>

<INPUT TYPE="TEXT" name="sendmail" Value="$mailloc[0]" size="40"> Sendmail path. The path to where sendmail is located. <b>Usually /usr/lib/sendmail -t. The -t is strongly encouraged and may be required!</b>
<P>

<INPUT TYPE="SUBMIT" name="Submit1" value="Install Tarot Script">
</form>

|;
}

sub replace_tokens(){
	my $filename = $_[0];

	#load file
	open (FILE, $filename) or die("Can't open $filename");
	@file_text= <FILE>;
	close FILE;
	$file_text = join("" , @file_text);

	#replace tokens in file
	$file_text =~ s/EMAIL_ADDRESS/$in{SERVER_ADMIN}/g;
	$file_text =~ s/SENDMAIL_PATH/$in{sendmail}/g;
	$file_text =~ s/YOUR_SITE_URL/$in{HTTP_HOST}/g;
	$file_text =~ s/FULL_PATH_TO_SCRIPT/$FULL_PATH_TO_SCRIPT/g;
	$file_text =~ s/SHORT_PATH_TO_SCRIPT/$SHORT_PATH_TO_SCRIPT/g;
	$file_text =~ s/URL_TO_SCRIPT/$URL_TO_SCRIPT/g;
	my $FULL_PATH_TO_INDEX = "$in{DOCUMENT_ROOT}\/$SHORT_PATH_TO_INDEX";
	$file_text =~ s/FULL_PATH_TO_INDEX/$FULL_PATH_TO_INDEX/g;
	$file_text =~ s/URL_TO_INDEX/$URL_TO_INDEX/g;

	#write modified file
	open (FILE, ">$filename") or die("Can't write to $filename");
	print FILE $file_text;
	close FILE;
}

sub vars
{

#copy all /cgi files to destination
print "Making $FULL_PATH_TO_SCRIPT/ \n";
if (not -d "$FULL_PATH_TO_SCRIPT/") {mkdir("$FULL_PATH_TO_SCRIPT/" , 0777) or die("Can't make $FULL_PATH_TO_SCRIPT/");};
print "<br>Done.<p> \n";
print "Copying $FULL_PATH_TO_INSTALL_SCRIPT/cgi/tarot/ to $FULL_PATH_TO_SCRIPT/ \n";
&copyDir("$FULL_PATH_TO_INSTALL_SCRIPT/cgi/tarot/","$FULL_PATH_TO_SCRIPT/") or die("Can't copy from $FULL_PATH_TO_INSTALL_SCRIPT/cgi/tarot/ to $FULL_PATH_TO_SCRIPT/");
print "<br>Done.<p> \n";

chmod (0755,"$FULL_PATH_TO_SCRIPT/tarot.cgi") or die('CHMOD of tarot.cgi failed.'); #set the permission for tarot.cgi

#copy all tarot html files to destination
print "Making $FULL_PATH_TO_INDEX/ \n";
if (not -d "$FULL_PATH_TO_INDEX/"){mkdir("$FULL_PATH_TO_INDEX/" , 0777) or die ("Can't make $FULL_PATH_TO_INDEX/");};
print "<br>Done.<p> \n";
print "Copying $FULL_PATH_TO_INSTALL_SCRIPT/tarot/ to $FULL_PATH_TO_INDEX/ \n";
&copyDir("$FULL_PATH_TO_INSTALL_SCRIPT/tarot/","$FULL_PATH_TO_INDEX/") or die("Can't copy $FULL_PATH_TO_INSTALL_SCRIPT/tarot/ to $FULL_PATH_TO_INDEX/");
print "<br>Done.<p> \n";

&replace_tokens( "$FULL_PATH_TO_SCRIPT/core_vars.pm" );
&replace_tokens( "$FULL_PATH_TO_INDEX/index.html" );

print "<P>Finished.<P>Test Tarot script installation:<br>";
print "<p><a href='$URL_TO_INDEX' target='_blank'>$URL_TO_INDEX<\/a>";

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
<INPUT TYPE="TEXT" NAME="FULL_PATH_TO_INSTALL_SCRIPT" Value="$FULL_PATH_TO_INSTALL_SCRIPT" size="40">
</form>
|;

}

sub remove
{
if ($in{FULL_PATH_TO_INSTALL_SCRIPT})
    {
    print "Removing installation files from $in{FULL_PATH_TO_INSTALL_SCRIPT}.";
    removeDir ($in{FULL_PATH_TO_INSTALL_SCRIPT});
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
