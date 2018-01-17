
<?
#example only
chdir('cgi/tarot/');
$qs = "deckpath=../../tarot/databases/emogic.cgi&spreadpath=../../tarot/spreads/three_card.html";
#exec( "perl storecall.cgi \"$qs\" " ); 
passthru( "perl storecall.cgi \"$qs\" " ); 
 ?>
