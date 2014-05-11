/*=========================================================
* market.js
* https://ojo-ticket.appspot.com/market/static/js/market.js
*==========================================================
* Copyright 2013 Aristote Diasonama
*======================================================== */
    
	/* ADD GETWEEK TO DATE
	 * ==================== */
	 Date.prototype.getWeek = function() {
         var onejan = new Date(this.getFullYear(),0,1);
         return Math.ceil((((this - onejan) / 86400000) + onejan.getDay()+1)/7);
     } 
	 
	 
	 
	 /* Function to alert the user an error happened
	  * ==================== */
	  function we_are_lost(message){
		  if (typeof(message) === "undefined")
		  {
			  message = "<h4>Oups! On s'est perdu!</h4> Essayez de recommencer ou raffraichir la page. En cas de persistence de l'erreur, Nos techniciens seront notifiés et s'en chargeront!"
		  }
		  bootbox.alert(message);
	  }
	 
	  /* Function to send a message to the server
	  * ==================== */
	 function send_contact_message(){
		 var form = $("#contact-form");
		 var url = 'rpc/contact';
		 $.ajax({
			 type: "POST",
			 url:url, 
			 dataType:"json",
			 async: false,
			 data: form.serialize(), 
			 success:function(data){
				 success_message = '<div class="alert alert-success">Votre message a bien été réçu! Nous y repondrons dans le meilleur délai possible. Merci! </div>'
				 $("#contact-form-div").html(success_message);
			 },
			 error:function(error){
				 $('#contact-form-error').show();
				 window.location.hash = "#contact-form-error";
			 }
			 
		 });
				 
	 }
	 
	 
	 /* Function to attend an event
	 * ==================== */
	function attend_event(event_key, url){
		if(typeof url == "undefined") url = '/rpc/event/attend';
		$div = $('.btn-going-'+event_key);
		$div.children('button').attr('disabled', 'true');
		
		$.post(url, {'event_key':event_key})
		.done(function(attend_key){
			var html = '<div class="btn-group">'
                    +  '  <button class="btn btn-success dropdown-toggle" data-toggle="dropdown">J\'y serai <span class="caret"></span></button>'
                    +  '    <ul class="dropdown-menu">'
                    //+  '      <li><a href="#">Peut-être</a></li>'
                    +  '      <li><a href="#"  onClick="kill_attend(\'' + event_key + '\', \'' + attend_key + '\', \''+ url + '\'); return false;">Je n\'y serai pas</a></li>'
                    +  '   </ul>'
                    +  '</div>'
			$div.html(html)	 
			
		})
		.fail(function(error){
			$div.children('button').removeAttr('disabled');
			we_are_lost();
			
			
		});
	}
	
	/* Function to rate an event
	  * ==================== */
	  
	 function rate_event(event_key, score)
	 {
		url = '/rpc/event/review';
		$.post(url, {'event_key':event_key, 'score':score})
		.done(function(attend_key){
			
		})
		.fail(function(error){
			$div.children('button').removeAttr('disabled');
			we_are_lost();
			
			
		});
	 }
	
	 /* Function to report an event
	  * ==================== */
	function report_event(event_key, url){
		if(typeof url == "undefined") url = '/rpc/event/report';
	
		$.post(url, {'event_key':event_key})
		.done(function(data){
			bootbox.alert("Nous avons bien réçu votre demande! Notre équipe examinera cet event de près et prendra une décision conséquente. Merci car Grâce à votre aide, nous pouvons garder ce site propre!"); 
			
		})
		.fail(function(error){
			
			bootbox.alert("Une erreur est survenue! Notre équipe d'ingénieurs a été notifiée et y travaillera le plus vite possible! Merci de continuer de nous aider à garder ce site propre!");
			
			
		});
	}
	
	 /* Function to cancel to attend an event
	 * ==================== */
	function kill_attend(event_key, attend_key, url){
		if(typeof url == "undefined") url = '/rpc/event/attend';
		$div = $('.btn-going-'+event_key);
	
		$.post(url, {'attend_key':attend_key, 'event_key':event_key})
		.done(function(){
			var html = '<div class="btn-group">'
                    +  '  <button class="btn btn-success dropdown-toggle" data-toggle="dropdown">Je n\'y serai pas <span class="caret"></span></button>'
                    +  '    <ul class="dropdown-menu">'
                    //+  '      <li><a href="#">Peut-être</a></li>'
                    +  '      <li><a href="#" onClick="attend_event(\''+ event_key +'\', \'' + url +'\'); return false;">J\'y serai</a></li>'
                    +  '   </ul>'
                    +  '</div>';
			$div.html(html);
			
		})
		.fail(function(error){
			
			we_are_lost();
		});
	}
	  
	
	
	
	
	/* Function to subscribe to a user
	 * ==================== */
	function subscribe_to_user(user_id, url){
		if(typeof url == "undefined") url = 'rpc/'+ user_id + '/subscribe';
		$div = $('.btn-subscribe-'+ user_id);
		$button = $div.children('button');
		$button.button('loading');
		$.post(url)
		.done(function(subscription_key){
			
			var html = '<button href="" class="btn btn-success btn-unsubscribe pull-right" onClick=\'unsubscribe("' + user_id + '", ' + subscription_key + ', "'+ url + '"); return false;\'><span><i class="icon-ok-sign" data-loading-text="En cours..." ></i> Abonné</span></button>';
                
			$div.html(html);
			
		})
		.fail(function(error){
		    mybutton.button('reset');
			we_are_lost();
		});
	}
	
	
	 /* Function  to unsubscribe an event
	 * ==================== */
	function unsubscribe(user_id, subscription_key, url){
		if(typeof url == "undefined") url = '/rpc/'+ user_id + '/subscribe';
		$div = $('.btn-subscribe-'+ user_id);
		$button = $div.children('button')
		$button.button('loading');
		$.post(url, {subscription_key:subscription_key})
		.done(function(){
			var html = '<button href="" id="subscribe-button" role="button" class="btn btn-primary pull-right" onClick="subscribe_to_user(\''+user_id + '\', \'' + url + '\'); return false;" data-loading-text="En cours...">S\'abonner</button>'
			$div.html(html);
			
		})
		.fail(function(error){
			mybutton.button('reset');
			we_are_lost();
		});
	}
	
	
	/* MARKET CLASS DEFINITION
	 * ======================= */
	var Market = function(user){
	
        this.user = user;
		this.filter_key = 'all';
		this.sort_order = 'date_event';
		this.more = true;
		this.events = null;
		this.users = null;
		this.cursor = 15;
		var self = this;
		
		
		
		
		
	};
	
	Market.prototype = {
		
		constructor: Market
		
		/**
		* Update the list of events of the market by making an AJAX call to the server according to the url we are viewing
		*
		*/
		
		,update_events: function(){
		 var that = this;
		 $.ajax({
		type:"GET",
		url:'/rpc'+ window.location.pathname,
		dataType:"json",
		async: false,
		data: {'cursor':this.cursor, 'filter_key':this.filter_key, 'sort_order':this.sort_order},
		success: function(data){
			that.more = data.more;
			that.cursor = data.cursor;
			that.events =  data.events;
		},
		error: function(error){
			        console.log(error);
			  }
		
		
	})
		}
		
		
		
		/**
		* Update the the sort order of the events and then update events according to the new sort_order
		*/
		
		,update_events_sorted_by: function(sort_by){
		 this.cursor = 0;
		 this.sort_order = sort_by;
		 this.update_events();

		}
		
		/**
		* Update the filter of the events and then update events according to the new filter
		*/
		
		, update_events_filtered_by: function(filter_by){
			this.cursor = 0;
			this.filter_key = filter_by;
			this.update_events();
			
		}
		
		/**
		* get a json event and return an html report button 
		*
		*/
		,event_button_report: function(an_event){
			if(this.user && this.user.type == "student" && this.user.id != an_event.seller_id)
			{
			var html = ' <div class="dropdown pull-right "><button type="button" class="dropdown-toggle close" data-toggle="dropdown"><i class="icon-chevron-down"></i></button><ul class="dropdown-menu" role="menu" aria-labelledby="dLabel"><li role="presentation"><a role="menuitem" tabindex="-1" href="#" onClick="report_event(\''+an_event.key+'\'); return false;">Signaler comme inappropriée</a></li></ul></div>';
			}
			else var html = '';
			
			return html;
			
			
		}
		/**
		* get a json event and return an html attend button if one
		*
		*/
		, event_button_attend: function(an_event){
			var html = '';
			if(this.user && this.user.type == "student" && this.user.id != an_event.seller_id)
			{   
			    html += '<div class="btn-going-'+an_event.key+' attend-button">\n';
				if(an_event.attending){
					
					html += '<div class="btn-group">'
                    +  '  <button class="btn btn-success dropdown-toggle" data-toggle="dropdown">J\'y serai <span class="caret"></span></button>'
                    +  '    <ul class="dropdown-menu">'
                    //+  '      <li><a href="#">Peut-être</a></li>'
                    +  '      <li><a href="#"  onClick="kill_attend(\'' + an_event.key + '\', \'' + an_event.attend_key + '\'); return false;">Je n\'y serai pas</a></li>'
                    +  '   </ul>'
                    +  '</div>';
				}
			else{
				html += '<button role="button" class="btn btn-primary" onClick="attend_event(\''+an_event.key+'\'); return false;"><i class="icon-thumbs-up"></i> J\' y serai</button>\n';
						 
				}
				
				html += '</div>\n';
			}
			
			return html;
		   }
		

		
		/**
		* return an array containing 2 elements. the first is the event thumbnail and the second the event modal
		*
		*/
		  
		, event_to_html: function(an_event){
			var events = new Array();
			var window_width = window.innerWidth;	
			var html = '<li class="span4">\n'
			         + '  <div class="thumbnail">\n'
					 + '   <div class="row-fluid"><div  style="height:100%;">';
				if(window_width >= 768)
			   html += '    <a class="event-info-link" href="#evMod-'+an_event.key + '" data-toggle="modal">'
				     + '      <img class="event-image" src="';
				else
			   html += '    <a class="event-info-link" href="'+an_event.seller_id+'/'+an_event.id+'" data-toggle="modal">'
				     + '      <img class="event-image" src="';
				if (an_event.image_url)
				html += an_event.image_url + '=s266';
				else html +=  an_event.image;
			   
			   html += '" alt="Event Image">\n'
					 + '    </a>';
					 
			   html += '    <div class="caption">\n';
					 
			 
			   html += this.event_button_report(an_event);
			   html += '      <h4 class="text-center event-name"><a itemprop="url" href="' + an_event.seller_id + '/'+an_event.id+'">' + an_event.name + '</a></h4>\n'
					 + '      <p class="event-organiser">Publié par: ' ;
					 if(an_event.seller_id){
						 html += '<a href="/'+an_event.seller_id+'">' + an_event.seller + '</a>';
					 }
					 else{
						 html += an_event.seller;
					 }
				     html += '</p>\n'
					      + '      <p class="event-organiser"><span><i class="icon-time"></i> ' + (new Date(an_event.date_event*1000)).toLocaleDateString()+ ' A '+ 
					          (new Date(an_event.date_event*1000)).toLocaleTimeString()+ '</span><br/><span><i class="iconic-map-pin-alt"> </i><strong>'+ 
							  an_event.venue_name + '</strong></span></p>\n';
					
					 
					 html +=  '      <div class="row-fluid">\n';
					 html +=  this.event_button_attend(an_event);
					 html += '     </div>\n';
					
					 html += '      </div>\n' //
					 + '    </div>\n'
					 + '  </div>\n'
					 + '</li>';
			
			if(window_width >= 768){		 
			var html2 = '<div id="evMod-'+an_event.key+'" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="evMod-'+an_event.key+'Label" aria-hidden="true" style="width:800px;">\n'
			          + '  <div class="modal-header">\n'
                      + '    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>\n'
                      + '    <h3 id="evMod-'+an_event.key+'Label">'+an_event.name+'</h3>\n'
                      + '  </div>\n'
					  + '  <div class="modal-body">\n'
                      + '    <div class="row-fluid">\n'
                      + '      <div class="span5"> <img src="';
			    if (an_event.image_url)
				 html2 += an_event.image_url + '=s266';
				else html2 +=  an_event.image;
				 html2 +='" alt="Event Image"></div>\n'
                      + '      <div class="span7">\n'
                      + '        <div class="row-fluid">\n'
                      + '          <dl class="dl-horizontal">\n'
                      + '            <dt> C\'est quoi? </dt>\n'
                      + '            <dd> '+an_event.description +' </dd> <br/>\n'
                      + '            <dt> Quand? </dt>\n'
                      + '            <dd> ' + (new Date(an_event.date_event*1000)).toLocaleDateString()+ ' A '+(new Date(an_event.date_event*1000)).toLocaleTimeString() + '</dd> <br/>\n'
                      + '            <dt> Où ? </dt>\n'
                      + '            <dd>\n' 
                      + '             <address>\n'
		              + '               <strong>'+ an_event.venue_name + '</strong><br>'+ an_event.venue_addresse
	                  + '             </address>\n'
                      + '            </dd>\n';
			   if(an_event.terms){
				   html2 += '<dt> Conditions ? </dt><dd>' + an_event.terms + '</dd> <br/>';
			   }
					  
               html2 += '          </dl>\n'
                      + '        </div>\n'
                      + '        <i class="icon-arrow-right"> </i> Voir la <a href="'+an_event.seller_id+'/'+an_event.id+'"> page de l\'event</a>' + this.event_button_attend(an_event)
                      + '        </div>\n';
					 if(an_event.url){
						 html2 += '<p class="event-organiser event-source pull-right"><small>Source: <a style="overflow:hidden" href="'+an_event.url+'" target="_blank">'+ an_event.url+'</a></small></p>';
					 } 
                  html2+= '      </div>\n'
                      + '    </div>\n'
                      + '    <div class="modal-footer">\n'
                      + '    </div>\n'
                      + ' </div>\n'
			}
			
					 
			if(window_width > 768)
			return {'thumbnail':html, 'modal':html2};
			else return {'thumbnail':html, 'modal':''};
			
			
			
		}
		
		
		/**
		* Get the current list of events with of all the events transformed into html thumbnailed_view
		*
		*/
		,get_events_list_html: function(){
			
			events = new Array();
			if(this.events === null) return events
		    for (var i=0;i<this.events.length;i++)
			{
				events.push(this.event_to_html(this.events[i]));
			}
			console.log(events.length)
			return events
			
		}
		
		
		,add_data_to_target: function(data, target, append){
			if (typeof(append) === 'undefined'){
				append = true;
			}
			if (!data.length){
				if (!append)
				html = "<span class='text-center'><strong>Il n'y a aucun événement dans cette catégorie</strong></span>";	
			}
			else {
			var html = '<div class="block-of-3 row-fluid">';
		        html += data.reduce(function(a,b, index){
			
			          if ((index+1) % 3 == 0){
				        return a + b.thumbnail + '</div><div class="block-of-3 row-fluid">';
			          }
			          else{
				       return a + b.thumbnail ;
			          }
	
		         }, '');
		
		        html += '</div>';
			var html2 = data.reduce(function(a,b){
				return a + b.modal;
				
			}, '');
			
			}
			if (append){
				$(target).append(html);
				$('#all-modals').append(html2);
			}
			else{
		    $(target).html(html);
			$('#all-modals').html(html2);
			}
		
		}
		
		,add : function(func, element){
		    var that = this;
			$(element).bind('change', function(e){
				var key = this.value;
				
				if (func === 'sorter'){
					that.update_events_sorted_by(key);
				}
				
				else if(func === 'filter'){
				   var $this = $(this);
	               var filter = this
	               if(key=== 'week' || key === 'today' || key === 'month' || key === 'tomorrow' || key === 'all'){
	                   $('option.custom-date', filter).val('date')
		               $('input.custom-date').hide()
	               }
	
                   else if(key === 'date'){
	                   var $input = $('input.custom-date');
		
		               $input.css('display','');
		               $input.datepicker( {
                           onSelect: function(date) {
			
			                   $('option.custom-date', filter).val(date)
			                   $this.trigger('change')
                           },
                           minDate:"+0d"
                      });
		              
					   $input.datepicker( "show" );
	   
	                   return false
	               }
	               that.update_events_filtered_by(key);
	       
		       }
				
		    var target =  $(this).data('target');
			events = that.get_events_list_html();
		    that.add_data_to_target(events, target, false);
			
		    });	
		}
		
		
		,add_sorter: function(element){
			this.add('sorter', element);
		}
		
		
		,add_filter: function(element){
			this.add('filter', element);
			
		}
		
	    , load_more_events:function(){
			
			if(this.more){
			    this.update_events();
			    events = this.get_events_list_html();
			    this.add_data_to_target(events, $('#events'), append=true);
			}
		
		}
		, load_first_15:function(){
			this.update_events();
			events = this.get_events_list_html();
			this.add_data_to_target(events, $('#events'), append=false);
		}
		, subscription_button: function(a_user){
			var html = '';
			if (a_user.subscription_key)
			{
				html += '<button class="btn btn-success btn-unsubscribe pull-right " onClick="unsubscribe(\''+ a_user.id +'\', '+ a_user.subscription_key +'\', /rpc/'+a_user.id+'/subscribe\'); return false;" data-loading-text="En cours..."><span><i class="icon-ok-sign" ></i> Abonné </span></button>'; 
			}
			
             else
			 {
                 html += '<button id="subscribe-button" role="button" class="btn btn-primary pull-right" onClick="subscribe_to_user(\''+ a_user.id +'\', /rpc/'+a_user.id+'/subscribe); return false;" data-loading-text="En cours...">S\'abonner</button>';
			 }
			return html;
		}
		,update_users: function(){
		 var that = this;
		 $.ajax({
		type:"GET",
		url:'/rpc'+ window.location.pathname,
		dataType:"json",
		async: false,
		data: {'cursor':this.cursor, 'filter_key':this.filter_key, 'sort_order':this.sort_order},
		success: function(data){
			that.more = data.more;
			that.cursor = data.cursor;
			that.users =  data.users;
			console.log(that.users)
		},
		error: function(error){
			        console.log(error);
			  }
		
		
	})
		}
		
		, user_to_html: function(person){
			
			html = '';
			html += '<div class="row-fluid element">\n'
                 + '  <div class="pull-left" style="margin-right:1%;">\n'
                 + '    <div id="profile-picture" class="thumbnail" style="width:70px; height:70px;"><img src="'+ person.profile_picture + '" style="width:100%; height: 100%;"/>\n'
                 + '    </div>\n'
                 + '  </div>\n'
                 + '  <div class="pull-left user-detail" ><a href="/' + person.id+'">'+person.fullname+' </a>';
              if (person.description){
			html += '    <p>'+person.description + '</p>';
                    }
               if (person.type == "student")
			   {
            html += '     <p>';
			
               if (person.gender == 'male') html += 'Étudiant '; 
			   else html += 'Étudiante ';
			   if (person.major) html += 'en ' + person.major;  
            html += '      </p>'
			   }
			   else {
				   
            html += '      <p>Association</p>';
			   }
                    
            html += '       <p>'
                  + '         <span style="color:#F00">' + person.events_published  + '</span>'; 
			if(person.events_published <= 1) html += ' event publié';
			else html += ' events publiés'; 
            html += '       </p>'
                    
                  + '     </div>'
                
                  + '     <div class="subscription-button">' + this.subscription_button(person)
                  + '     </div>'  
                  + ' </div>';
			
			return html;
		}
		
		,get_users_list_html: function(){
			
			users = new Array();
			if(this.users === null) return users
		    for (var i=0;i<this.users.length;i++)
			{
				users.push(this.user_to_html(this.users[i]));
			}
			console.log(users.length)
			return users
			
		}
		
		/**
		* Insert users into the target div
		*
		*/
		, add_users_to_target: function(users, target, append){
			if (typeof(append) === 'undefined'){
				append = true;
			}
			if (!users.length){
				if (!append)
				users = "<span class='text-center'><strong>Où sont donc passés nos utilisateurs?</strong></span>";	
			}
			
			if (append){
				$(target).append(users);
			}
			else{
		    $(target).html(users);
			}
			
			
		}
		
		 , load_more_users:function(){
			
			if(this.more){
			    this.update_users();
			    users = this.get_users_list_html();
			    this.add_users_to_target(users, $('#users'), append=true);
			}
		
		}
		
		/**
		* Load the first 15 users to the user div
		*
		*/
		, load_first_15_users:function(){
			this.update_users();
			users = this.get_users_list_html();
			this.add_users_to_target(users, $('#users'), append=false);
			
		}
	}

