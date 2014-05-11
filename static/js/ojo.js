/*=========================================================
* ojo.js
* https://ojo-ticket.appspot.com/static/js/ojo.js
*==========================================================
* Copyright 2013 Aristote Diasonama
*======================================================== */


 


/* FUNCTION TO TELL SERVER YOU FORGOT PASSWORD
 */

function forgot_password(){
	
	var url = '/rpc/forgot'
	bootbox.prompt("Quelle est l'addresse email que tu utilises pour te connecter?", function(result){
		
		if(result != null){
			
			$.post(url, {'email':result})
		.done(function(data){
			bootbox.alert("Un email avec lien de renouvellement a été envoyé à l'addresse "+result+". Veuillez suivre ce lien pour changer votre mot de passe!"); 
			
		})
		.fail(function(error){
			if(error.status == 404) message = "Nous n'avons trouvé aucun utilisateur associé à l'email "+result+". Assurez-vous que vous avez bien écrit l'email ou encore qu'il s'agit bien de l'email que vous utilisez pour vous connecter";
			else message = "Une erreur est survenue! Nous n'avons pas été en mesure de faire aboutir votre requête. Réessayez un peu plus tard"
			bootbox.alert(message);
			
			
		});
	
		}
		
	});
}

/* FUNCTION TO AJAX RESET PASSWORD
 */
 
 function reset_password(){
	 alert_div = $('#reset-password-message')
	 form_data = $('#reset-password-form').serialize()
	 url = '/rpc/reset_password'
	  $.ajax({
			 type: "POST",
			 url:url, 
			 dataType:"json",
			 async: false,
			 data: form_data, 
			 success:function(data){
				alert_div.addClass('alert-success');
				alert_div.html('<h4>Votre nouveau mot de passe a bien été enregistré!</h4> Vous serez maintenant rédirigé vers votre page d\'accueil!').show().alert();
				setTimeout(function(){window.location.href = "/";}, 7000);
				
				 
				 },
			 error: function(error){
				   
				
					if(error.status === 400) message = 'Vos deux nouveaux emails ne sont pas identiques!';
					else if(error.status === 403) message = 'L\'ancien mot de passe fourni n\'est pas correct';
					else message ='Une erreur est survenue lors de cette opération! Nos techniciens ont été informés! Vous pourrez réessayer un peu plus tard'
			        alert_div.html('<p>'+message+'</p>').addClass('alert-error').show().alert();
					window.location.hash="#reset-password-message";
					
			  }});
 }
 

// SIGN USER UP

/* AJAX FUNCTION TO SEND FORM DATA TO SERVER AND HANDLE RESPONS
 */
 function signup(form_data, url_to_signup, category){
	 var callback =$("#student-signup-form").data('callback');
	 
	 
	 if(callback)
	 {
		 url_to_signup = url_to_signup + '?callback=' + callback;
		 
	 }
	 
	 if (category === 'student')
	 {
		 var message = "Votre compte a été créé. Un lien de confirmation a été envoyé à votre addresse email de l'université Laval fournie. Veuillez confirmez votre email afin de continuer à utiliser le site sans interruption. Bienvenue dans notre communauté. Enjoy";
	 }
	 else
	 {
		 var message = "Nous vous remercions d'avoir choisi EventBuck. Un réprésentant vous contactera sous peu pour confirmer les informations que vous avez fournies. Bienvenue dans notre communauté. Enjoy";
	 }
	  $.ajax({
			 type: "POST",
			 url:url_to_signup , 
			 dataType:"json",
			 async: false,
			 data: form_data, 
			 success:function(data){
				 bootbox.alert(message, function(response){
					 console.log(data.redirect);
					 if(callback && data.redirect)
					 {
						 window.location.href = callback;
					 }
					else
				 	{
					 	window.location.href = "/";
					}
				 });
				 
				 },
			 error: function(error){
				   
					console.log(error);
					if(error.status === 400) message = error.responseText;
					else if(error.status === 409) message = 'Un utilisateur avec un des emails fournis existe déjà';
					else message = "<h4>Oups! On s'est perdu!</h4> Essayez de recommencer ou raffraichir la page. En cas de persistence de l'erreur, Nos techniciens seront notifiés et s'en chargeront!";
			        $("#signup-error").html('<p>'+message+'</p>').show().alert();
					window.location.hash = "#signup-error";
					
			  }});
 }

$("#student-signup-form").on('submit', function(event){
	
	var form = $(this) ;
	var that = this;
	var url = '/rpc/signup';
	var form_data = form.serialize();
	var category = 'student';
	signup(form_data, url, category);
	
	return false;
	
	
});

// FACEBOOK SIGNUP

$('#facebook-signup-form').on('submit', function(event){
	FB.getLoginStatus(function(response) {

  if (response.authResponse) {
    token = response.authResponse.accessToken;
	document.getElementById('access-token').value=token;
  }
	});
		
	var form = $(this) ;
	var that = this;
	var url = '/rpc/signup/fb';
	var form_data = form.serialize();
	var category = 'student';
	signup(form_data, url, category);
	
	return false;
	
	
});

// ADD A DATETIME PICKER TO A DATETIME FIELD WITH ID DATE_EVENT

$(document).ready(function(e) {
				
	          $(function() {
                $("#date_event").datetimepicker({minDate:"+0d"});
               });
                
            });




// function to delete an event
	
	function delete_event(url){
		var mybutton = $("#delete-button");
		bootbox.confirm("Etes vous sûr de vouloir supprimer cet event?\n Cette opération est irreversible!", function(response){
		if (response === true)
		{
		mybutton.button('deleting');
		
		$.ajax({
			type:"POST",
			url: url,
			success: function(data){
				bootbox.alert("Votre event a bien été supprimé. Vous serez rédirigé vers la liste de vos autres événements", function(reponse){
					window.location.href = "/myevents";
				});
			},
			
			error: function(request, error){
				
				bootbox.alert("Une erreur s'est produite lors de la suppression de votre event!\n Nous nous excusons pour l'incovénient. Nos ingénieurs ont été notifiés, vous pouvez réessayer un peu plutard");
			}
			
		});
		
		}
		
		});
	}
				

// function to publish an event
	function publish_event(url){
		var mybutton = $("#publish-button");
		mybutton.button('loading');
		
		$.ajax({
			type:"POST",
			url: url,
			success: function(data){
				document.getElementById('published-status').style.display='';
				document.getElementById('publish-button').style.display='none';
				$('.publish-success').fadeIn(400);
				setInterval(function(){$('.publish-success').fadeOut(400);},10000);
			},
			
			error: function(error){
				console.log(error);
				if(error.status === 403){
					message = "<h4> Accès réfusé </h4>Vous n'êtes pas autorisé à publier un event vu que votre compte n'a pas encore été vérifié.<br> \
					           Nous vous avions envoyé un lien de vérification à votre addresse email "+error.responseText+" lors de votre enregistrement. Veuillez suivre ce lien pour confirmer votre compte <br>\
							   Au cas où vous ne l'avez pas réçu, <a class='btn btn-small btn-primary' href='#' onclick='send_verification_link()'>cliquez ici</a> pour réenvoyer le lien";
					$('.publish-error div').html(message);
					$('.publish-error').fadeIn(400);
				}
				else{
				$('.publish-error').fadeIn(400);
				setInterval(function(){$('.publish-error').fadeOut(400);},10000);
				}
				mybutton.button('reset');
			}
			
		});
	}
	
	
// function to resend verification link

 function send_verification_link(){
	 url = '/rpc/verification';
	 $.post(url)
		.done(function(data){
			bootbox.alert("Nous avons réenvoyé un lien de verification à votre addresse email @ulaval.ca. Veuillez cliquer sur le lien pour confirmer votre compte.\n Si vous ne trouvez toujours pas le message, vérifiez votre dossier spam"); 
		})
		.fail(function(error){
			
			bootbox.alert("Une erreur est survenue! Notre équipe d'ingénieurs a été notifiée et y travaillera le plus vite possible!")       
			})
		.always(function(){
			$('.alert').alert('close');
		
			
			
		});
 }
	
	
	

//Work around to enable the function reduce in case it is not enabled
if ('function' !== typeof Array.prototype.reduce) {
  Array.prototype.reduce = function(callback, opt_initialValue){
    'use strict';
    if (null === this || 'undefined' === typeof this) {
      // At the moment all modern browsers, that support strict mode, have
      // native implementation of Array.prototype.reduce. For instance, IE8
      // does not support strict mode, so this check is actually useless.
      throw new TypeError(
          'Array.prototype.reduce called on null or undefined');
    }
    if ('function' !== typeof callback) {
      throw new TypeError(callback + ' is not a function');
    }
    var index = 0, length = this.length >>> 0, value, isValueSet = false;
    if (1 < arguments.length) {
      value = opt_initialValue;
      isValueSet = true;
    }
    for ( ; length > index; ++index) {
      if (!this.hasOwnProperty(index)) continue;
      if (isValueSet) {
        value = callback(value, this[index], index, this);
      } else {
        value = this[index];
        isValueSet = true;
      }
    }
    if (!isValueSet) {
      throw new TypeError('Reduce of empty array with no initial value');
    }
    return value;
  };
}


//FUNCTION TO UPLOAD A PICTURE ON THE FLY USING HIDDEN IFRAMES
function fileUpload(form, action_url, div_id, second_div_id)
{
// Create the iframe...

var iframe = document.createElement("iframe");
iframe.setAttribute("id","upload_iframe");
iframe.setAttribute("name","upload_iframe");
iframe.setAttribute("width","0");
iframe.setAttribute("height","0");
iframe.setAttribute("border","0");
iframe.setAttribute("style","width: 0; height: 0; border: none;");

// Add to document...

if(typeof(form.parentNode) != 'undefined') form.parentNode.appendChild(iframe);
else document.getElementById(div_id).appendChild(iframe);

window.frames['upload_iframe'].name="upload_iframe";

iframeId = document.getElementById("upload_iframe");

// Add event...
var eventHandler = function()  {

if (iframeId.detachEvent)
iframeId.detachEvent("onload", eventHandler);
else
iframeId.removeEventListener("load", eventHandler, false);

// Message from server...
if (iframeId.contentDocument) {
content = iframeId.contentDocument.body.innerHTML;
} else if (iframeId.contentWindow) {
content = iframeId.contentWindow.document.body.innerHTML;
} else if (iframeId.document) {
content = iframeId.document.body.innerHTML;
}

if(typeof(div_id) != 'undefined') document.getElementById(div_id).innerHTML = content;
if(typeof(second_div_id) != 'undefined') document.getElementById(second_div_id).innerHTML = content; 


// Del the iframe...
setTimeout('iframeId.parentNode.removeChild(iframeId)', 250);

}

if (iframeId.addEventListener)
iframeId.addEventListener("load", eventHandler, true);
if (iframeId.attachEvent)
iframeId.attachEvent("onload", eventHandler);

// Set properties of form...
form.setAttribute("target","upload_iframe");
form.setAttribute("action", action_url);
form.setAttribute("method","post");
form.setAttribute("enctype","multipart/form-data");
form.setAttribute("encoding","multipart/form-data");

// Submit the form...
form.submit();

document.getElementById(div_id).innerHTML = '<center><img src="/static/img/loader.gif" /></center>';



}


// EDIT user notifications settings
$('#rpc-edit-notif').on('submit', function(event){
	
	//prevent form from submitting
	event.preventDefault();
	var form = $(this) ;
	var that = this;
	var url = '/rpc/edit/notifications';
	var form_data = form.serialize();
	// post the form to the server
	$.ajax({
			 type: "POST",
			 url:url, 
			 dataType:"json",
			 async: false,
			 data: form_data, 
			 success:function(data){
				 
				$('.edit-success').fadeIn(400);
				setInterval(function(){$('.edit-success').fadeOut(400);},10000);
				
			 },
			 error: function(error){
			        
				$('.edit-error').fadeIn(400);
				setInterval(function(){$('.edit-error').fadeOut(400);},10000);
		
			  }});
			 
			 return false;
	
});

// edit user attributes in place

$("#rpc-edit-user").on('submit', function(event){
       
	   //prevent form from submitting
	   event.preventDefault();
	   
	
	    var form = $(this) ;
		var that = this
		var url = '/rpc/edit';
		var form_data = form.serialize()
			 

			 // post the form to the server
			 $.ajax({
			 type: "POST",
			 url:url, 
			 dataType:"json",
			 async: false,
			 data: form_data, 
			 success:function(data){
				 
				 if ($("#upload-picture").val().length != 0){
			         fileUpload(that, '/shop/profile/picture','profile-picture','target-profile-picture'); 
	 
		          }
				  
				  if (data.hasOwnProperty('name')){
					   $('p.screen-name').html(data.name);
					   $('#user-name').html(data.name);
				  }
				  if (data.hasOwnProperty('description')) $('p.user-description').html(data.description);
				  if (data.hasOwnProperty('major')) $('span.user-major').html(data.major);			  
				 $(".highlighted").hide();
                 $(".default").show();
                 $('#overlay').remove();
                 $('body').css('overflow', 'auto');
	             
				 
				 
				 return false;
				 

				 
				
			 },
			 error: function(error){
			        bootbox.alert(error);
			  }});
			 
			 return false;
			
		  });
		  
		  
		  
	// SEND EVENT FORM TO SERVER
    function post_event(form, edit){
	var result;
	var $form = $(form);
	
	
	
	var url_to_post = $form.attr( 'action' )
	var form_data = $(form).serialize();
		
	
	  $.ajax({
			 type: "POST",
			 url:url_to_post, 
			 dataType:"json",
			 async: false,
			 data: form_data, 
			 success:function(response){
				 result = response
			
				 },
			 error: function(error){
				   
					console.log(error);
					if(error.status === 400) message = error.responseText;
					
					else message = "<h4>Oups! On s'est perdu!</h4> Un problème est survenu lors de cette opération. Essayez de recommencer ou raffraichir la page. En cas de persistence de l'erreur, Nos techniciens seront notifiés et s'en chargeront!";
			        $("#create-event-error").html('<p>'+message+'</p>').show().alert();
					window.location.hash = "#create-event-error";
					
			  }});
			  
			  return result;
 
	}
	

	
// IMPORT FACEBOOK EVENT
function import_fbevent(event_id){
	
	
}

$("#import-facebook-event").on('submit', function(event){
	
	event.preventDefault();
	var facebook_link = $(this).find('input[name="link"]').val();
	var event_id = facebook_link.split('/');
	var ce_form = $('#create-event-form');
	event_id = event_id[event_id.length - 2]
	
	
	FB.getLoginStatus(function(response) {

      if (response.authResponse) {
        FB.api('/'+event_id, function(response) {
		  ce_form.find('input[name="is_facebook"]').val(true);
          ce_form.find('input[name="name"]').val(response.name);
		  ce_form.find('textarea[name="description"]').val(response.description);
		  ce_form.find('input[name="venue_name"]').val(response.location);
		  if(typeof(response.venue.street) != 'undefined')
		    ce_form.find('input[name="venue_addresse"]').val(response.venue.street +', '+ response.venue.city + ', ' + response.venue.state);
		  if(typeof(response.venue.latitude) != 'undefined')
		    ce_form.find('input[name="geo_location"]').val(response.venue.latitude + ','+response.venue.longitude);
		  ce_form.find('input[name="url"]').val(facebook_link);
		  var start_time = response.start_time;
		  start_time = start_time.split('T');
          date = start_time[0];
          date = date.split('-');
		  date = [date[2], date[1], date[0]].join('/');
          if(!response.is_date_only)
		  {
          time = start_time[1];
          time = time.split(':');
          time = [time[0], time[1]].join(':');
          start_time = [date, time].join(' ');
		  }
		  else{
			  start_time = date;
		  }
		  ce_form.find('input[name="date_event"]').val(start_time);
		  
		  FB.api('/'+event_id+'/?fields=picture.type(square)', function(response){
			  var image_url = response.picture.data.url.replace('https:', '');
			  var image = '<img src="' + image_url + '" width="200px" alt="Pas d\'image" >'
			  ce_form.find('input[name="image_url"]').val(image_url);
			  $('#event-picture').html(image)
			  
		  });
          
		  
		 		  });
				  
      } 
	  else {
        
      }
});
	
	return false;
	
});
	
// CREATE_EVENT
$("#create-event-form").on('submit', function(event){
	
	event.preventDefault();
	
	var message = "Votre event a été créé. Patientez pendant que nous vous rédirigeons vers la page de l'event";
	var has_image = false
	var form = $(this) ;
	
	var image = form.find('input[name="image"]').val()
	console.log(image);
	if(image != '' ){
		var has_image = true
		
	}

	var response = post_event(form, edit=false);
	console.log(response)
	if(typeof(response) != 'undefined')
	{
	 bootbox.alert(message);
	 if (has_image) {
	    var url = fileUpload(this, response.upload_url, 'event-picture');
	 }
	setTimeout(function(){window.location.href = response.event_url;}, 3000);
	}
	
	return false;

	
});

// EDIT_EVENT
$("#edit-event-form").on('submit', function(event){
	event.preventDefault();
	var message = "Votre event a été modifié. Vous devez patienter au maximum 30 minutes avant de voir le changement apparaitre dans la liste des events. Patientez pendant que nous vous rédirigeons vers la page de l'event";
	var has_image = false;
	var that = this;
	var form = $(this) ;
	
	var image = form.find('input[name="image"]').val()
	if(image != ''){
		var has_image = true
	}

	var response = post_event(form, edit=true);
	console.log(response)
	if(typeof(response) != 'undefined')
	{
	 bootbox.alert(message);
	 if (has_image) {
	    var url = fileUpload(this, response.upload_url, 'event-picture');
	 }
	setTimeout(function(){window.location.href = response.event_url;}, 3000);
	}
	return false;
	
	
});	   
		   