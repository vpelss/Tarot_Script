#!/usr/bin/perl

$ENV{'REQUEST_METHOD'} = 'GET';
$ENV{'QUERY_STRING'} = $ARGV[0]; # pass query string to $ENV{'QUERY_STRING'} so the &parse_form in tarot.cgi can process it!
require "tarot.cgi"; #this actually calls and runs the tarot.cgi script



