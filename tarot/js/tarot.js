//tarot.js must be at end of page

var Cookie   = new Object();
Cookie.day   = 86400000;
Cookie.week  = Cookie.day * 7;
Cookie.month = Cookie.day * 31;
Cookie.year  = Cookie.day * 365;

function getCookie(name) {
  var cookies = document.cookie;
  var start = cookies.indexOf(name + '=');
  if (start == -1) return null;
  var len = start + name.length + 1;
  var end = cookies.indexOf(';',len);
  if (end == -1) end = cookies.length;
  return unescape(cookies.substring(len,end));
}

function setCookie(name, value, expires, path, domain, secure) {
  value = escape(value);
  expires = (expires) ? ';expires=' + expires.toGMTString() :'';
  path    = (path)    ? ';path='    + path                  :'';
  domain  = (domain)  ? ';domain='  + domain                :'';
  secure  = (secure)  ? ';secure'                           :'';

  document.cookie =
    name + '=' + value + expires + path + domain + secure;
}

function deleteCookie(name, path, domain) {
  var expires = ';expires=Thu, 01-Jan-70 00:00:01 GMT';
  (path)    ? ';path='    + path                  : '';
  (domain)  ? ';domain='  + domain                : '';

  if (getCookie(name))
    document.cookie = name + '=' + expires + path + domain;
}

//place at end of templates!!!!!!!!!!!!!!
//set cookie so there is one reading for 24 hours for each name, question, deck, and spread
var when = new Date();
when.setTime (when.getTime() + (24 * 60 * 60 * 1000)); // 24 hrs from now 
//setCookie("<%custom1%><%custom2%><%template%><%database%>", "<%records%>", when);
if  (typeof custom1 === 'undefined') {custom1 = '';}
if  (typeof custom2 === 'undefined') {custom2 = '';}
if  (typeof template === 'undefined') {template = '';}
if  (typeof database === 'undefined') {database = '';}
if  (typeof records === 'undefined') {records = '';}
setCookie(custom1 + custom2 + template + database , records , when);

$(window).resize(fontsizes);

function fontsizes()
	{
	var fontsize = $("body").width() * .04;
	var maxfont = 20;
	if ( fontsize >= maxfont ) { fontsize = maxfont }
 	$("*").not(".facebook_button").css(
		{"font-size" : fontsize ,
		"font-family" : "cursive" 
		});
	var widthcardimage = $("body").width() * .25;
	var maxwidth = 112;
	if ( widthcardimage > maxwidth ) { widthcardimage = maxwidth } 
	$(".facecards").width( widthcardimage ); // set facecards width
	}   

fontsizes();
