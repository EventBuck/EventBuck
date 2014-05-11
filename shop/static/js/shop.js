/*=========================================================
* shop.js
* https://ojo-ticket.appspot.com/shop/static/js/shop.js
*==========================================================
* Copyright 2013 Aristote Diasonama
*======================================================== */


function initialize_google_maps() {
 
  var defaultBounds = new google.maps.LatLngBounds(
      new google.maps.LatLng(46.803849, -71.242776),
      new google.maps.LatLng(46.77326, -71.301956));
  var options = {
      bounds: defaultBounds,
	  componentRestrictions: {country: 'ca'},
	  types: ['establishment']
       };

  var input = /** @type {HTMLInputElement} */(document.getElementById('venue_name'));
  
  
  var autocomplete = new google.maps.places.Autocomplete(input, options);
 
  
    google.maps.event.addListener(autocomplete, 'place_changed', function() {
    input.className = '';
    var place = autocomplete.getPlace();
    if (!place.geometry) {
      // Inform the user that the place was not found and return.
      input.className = 'notfound';
	  
      return;
    }

   

    var address = '';
    if (place.address_components) {
      address = [
        (place.address_components[0] && place.address_components[0].short_name || ''),
        (place.address_components[1] && place.address_components[1].short_name || ''),
        (place.address_components[2] && place.address_components[2].short_name || '')
      ].join(' ');
    }
    
	document.getElementById("geolocation").value = place.geometry.location;
	
	input.name = 'old_name'
	var new_name = document.createElement('input');
	new_name.type = 'hidden';
	new_name.name = 'venue_name';
	new_name.value = place.name;
	
	input.parentNode.appendChild(new_name);
	
	
	document.getElementById("venue_addresse").value = address;
	
	

  });
  
 }

google.maps.event.addDomListener(window, 'load', initialize_google_maps)


