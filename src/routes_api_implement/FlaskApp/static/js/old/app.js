//create autocomplete objects for all inputs
//var options = {
//      types: ['(cities)']
//}
//var input1 = document.getElementById('from');
//new google.maps.places.Autocomplete(input1, option);
//var input2 = document.getElementById("to");
//var autocomplete2 = new google.maps.places.Autocomplete(input2, options)

//var input1 = document.getElementById("from");
//var autocomplete1 = new google.maps.places.Autocomplete(input1, options);

//var input2 = document.getElementById("to");
//var autocomplete2 = new google.maps.places.Autocomplete(input2, options);

//function initialize() {
//  var input1 = document.getElementById("from");
//  new google.maps.places.Autocomplete(input1, options);
//  var input2 = document.getElementById("to");
//  new google.maps.places.Autocomplete(input2, options);
//}

//google.maps.event.addEventListener(window, 'load', initialize);


//create autocomplete objects for all inputs
var options = {
    types: ['(cities)']
}

var input1 = document.getElementById("from");
var autocomplete1 = new google.maps.places.Autocomplete(input1, options);

var input2 = document.getElementById("to");
var autocomplete2 = new google.maps.places.Autocomplete(input2, options);