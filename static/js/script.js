window.onload=start;
function start(){
	slidingMenu();
	dynamicDateForm();
//function for sliding menu for the navigation starts here

//function for dinamic date selection in the sign up form starts here
function dynamicDateForm() {
	document.getElementById("months").selectedIndex=0;
	document.getElementById("days").onchange=saveDay;
	document.getElementById("months").onchange=populateDays;
	document.getElementById("years").onchange=populateYears;
	
}
var year;
var day;
var theMonth;
var monthDays;
function saveDay(){
	day=document.getElementById("days").value;
	}

function populateDays(){
	monthDays=new Array(0,31,29,31,30,31,30,31,31,30,31,30,31);
	var monthStr=this.options[this.selectedIndex].value;
	//if(year%4==0){
		//monthDays[2]=29;
		//}
	if(monthStr!="" ){
		 theMonth=parseInt(monthStr);
		
		if(day>monthDays[theMonth]){
			document.getElementById("days").options.length=0;
		for(var i=0;i<=monthDays[theMonth];i++){
			document.getElementById("days").options[i]=
			new Option(i+1);
			}
		}
		}
	}
	function populateYears(){
		year=document.getElementById("years").value;
	if(year%4!=0 && document.getElementById("days").value==29){
		monthDays[2]=28;
		document.getElementById("days").options.length=0;
		for(var i=0;i<=monthDays[theMonth];i++){
			document.getElementById("days").options[i]=
			new Option(i+1-1);
			}
		}
}
}
//function for dinamic date selection in the sign up form ends here	
//function to validate Sigg in form starts here
	function validateSignInForm()
	{
	var allGood;
	var x=document.forms["formLogin"]["userEmail"].value;
	var y=x;
	var z=document.forms["formLogin"]["userPassword"].value;
	var atpos=x.indexOf("@");
	var dotpos=x.lastIndexOf(".");
	if (x==null || x=="")
  		{
  			alert("Please enter your email");
			allGood=false;
  		}
	else if(atpos<1 || dotpos<atpos+2|| dotpos+2>=x.length){
		alert("Not a valid e-mail address");
		allGood=false;
		}
	else if (z==null || z=="")
  		{
  			alert("Please enter your password");
			allGood=false;
  		}
		return allGood;
	}
//function to validate sign in form ends here
//functoin to validate sign up form starts here	
function validateSignUpForm(){
		var allGood;
	var fName=document.forms["formSignUp"]["firstName"].value;
	var lName=document.forms["formSignUp"]["lastName"].value;
	var email=document.forms["formSignUp"]["email"].value;
	var email2=document.forms["formSignUp"]["emailConfirm"].value;
	var pwd=document.forms["formSignUp"]["password"].value;
	var atpos=email.indexOf("@");
	var dotpos=email.lastIndexOf(".");
	var sex=document.forms["formSignUp"]["gender"].value;
	var year=document.forms["formSignUp"]["birthYear"].value;
	var month=document.forms["formSignUp"]["birthMonth"].value;
	var day=document.forms["formSignUp"]["birthDay"].value;
	if (fName==null || fName=="")
  		{
  			alert("Please enter your first name");
			allGood=false;
  		}
	else if(lName==null || lName=="")
	{
		alert("Please enter your last name");
			allGood=false;	
	}
	else if (email==null || email=="")
	{
		alert("Please enter your email");
		allGood=false;
	}
	else if(atpos<1 || dotpos<atpos+2|| dotpos+2>=email.length){
		alert("Not a valid e-mail address");
		allGood=false;
		}
	else if(email2==null || email2=="")
	{
		alert("Please re enter your email");
		allGood=false;
	}
	else if(email!=email2)
	{
		alert("Please enter the same email ");
		allGood=false;
	}
	else if (pwd==null||pwd=="")
	{
		alert("Please enter your password");
		allGood=false;
	}
	else if(pwd.length<6)
	{
		alert("Your password should have at least 6 characters");
		allGood=false;
	}
	else if(sex==null|| sex=="")
	{
		alert("Select a sex");
		allGood=false;
	}
	else if(year==null|| year=="")
	{
		alert("Enter the year of your birthday");
		allGood=false;
	}
	else if(month==null || month=="")
	{
		alert("Enter the month of your birthday");
		allGood=false;
	}
	else if(day=null || day=="")
	{
		alert("Enter the day of your birthday");
		allGood=false;
	}
			return allGood;
}
//function to validate signup form ends here
//ajax function and sliding function

function ajaxCall(attr, page){
$(document).ready(function(){
  $(attr).ready(function(){
    $("#main").load(page);
  });
});
}

//sliding elements
function slide(elt1,elt2){
$(document).ready(function(){
  $(elt1).ready(function(){
    $(elt2).slideToggle();
  });
});
}
//search bar function
jQuery(function($){
$("#searchbox").watermark('search');
});
$(document).ready(function(){
$("#searchbox").keyup(function() 
{
	var searchbox=$(this).val();
	var dataString='searchword='+searchbox;
	if(searchbox==''){ 
	$("#search").hide();
	}
	else{
	$.ajax({type:"POST",url:"../search.php",data:dataString,cache:false,success:function(html){
		$("#search").html(html).show();
		}
	});
	}return false;
});
});	



