//create autocomplete objects for all inputs
/*var options = {
    types: ['(cities)']
}

var input1 = document.getElementById("from");
var autocomplete1 = new google.maps.places.Autocomplete(input1, options);

var input2 = document.getElementById("to");
var autocomplete2 = new google.maps.places.Autocomplete(input2, options);
*/

function onLoadFillManufcature(){
    // Request to fill the first select object
    var firs_select_name = "manufacturer";
    var manufacture_select_ele = document.getElementById(firs_select_name);
    var header = {
        "Accept" :  "application/json",
        "Content-Type" : "application/json"
   };
   var req_json = {
       //"manufacturer" : "none",
       "cols" : [firs_select_name, firs_select_name + "_code"],
   };
   console.log(req_json);
   var url = "/cars_query";
   postRequest_car(url, req_json, header, manufacture_select_ele);
}

function onChangeSelectCar(t){
    var id = t.id; // // Changed select id
    var select_ele = document.getElementById(id); // Changed select element
    if (select_ele.value == "none"){
        // First option - description
        return;
    }

    var next_select_ele;
    var selects_ele = document.forms["myForm"].getElementsByTagName("select");
  
    var req_json = {};

    for(let i = 0; i < selects_ele.length; i++){
        req_json[selects_ele[i].id + "_code"] = [parseInt(selects_ele[i].value)];

      if(selects_ele[i].id == id)
        if(i == selects_ele.length - 1){
          // Lest select item
          return;
        }
        else{
            next_select_ele = selects_ele[i+1];
            req_json["cols"] = [next_select_ele.id, next_select_ele.id + "_code"]
            break;
        }
    }

   var header = {
        "Accept" :  "application/json",
        "Content-Type" : "application/json"
   };
   console.log(req_json);
   var url = "/cars_query";
   postRequest_car(url, req_json, header, next_select_ele);
    //console.log(resp);
    //console.log(id);
    //console.log(select_ele.value);
}

function postRequest_car(url, data, header, next_select_ele){
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.setRequestHeader("Accept", header["Accept"]);
    xhr.setRequestHeader("Content-Type", header["Content-Type"]);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
          console.log(xhr.status);
          //console.log(xhr.responseText);
          cleanAllSelectElementsAfterSelectElement(next_select_ele);
          putRespInNextSelectElement(JSON.parse(xhr.responseText), next_select_ele);
        }};
    
    let req_data = JSON.stringify(data);

    xhr.send(req_data);
}

function putRespInNextSelectElement(respons_json, next_select_ele){
    // The function fill the next select element in the new data by creating new appropreate options
    console.log(respons_json);
    console.log(next_select_ele.id);

    var newOption, optionText;
    for (const [key, value] of Object.entries(respons_json)){
        // create option using DOM
        newOption = document.createElement('option');
        optionText = document.createTextNode(value);
        // set option text
        newOption.appendChild(optionText);
        // and option value
        newOption.setAttribute('value',key);

        next_select_ele.appendChild(newOption);
    }
}

function cleanAllSelectElementsAfterSelectElement(select_ele){
    // Reset all select ellements in "myForm" that come after given select_ele from this form
    var select_elems = document.forms["myForm"].getElementsByTagName("select");
    var j = select_elems.length;
    for(let i = 0; i < select_elems.length; i++){
        if (select_elems[i].id == select_ele.id){
            j = i;
        }
        if(i >= j){
            cleanSelectElement(select_elems[i]);
        }
    }
}

function cleanSelectElement(select_ele){
    while(select_ele.length > 1){
        select_ele.remove(1);
    }
}

function submit_form(){
    var selects_ele = document.forms["myForm"].getElementsByTagName("select");
    var car_json = {};
    for(let i = 0; i < selects_ele.length; i++){
        if(selects_ele[i].value == "none"){
            alert("Fill all fildes in car");
        }
        car_json[selects_ele[i].id + "_code"] = [parseInt(selects_ele[i].value)];
    }
    // Need ro encapsulate DB columns name
    car_json["cols"] = ["average_consumption"]

    var path_json = {};
    path_json['origin'] = document.getElementById('from').value;
    path_json['destination'] = document.getElementById('to').value;
    path_json['time'] = document.getElementById('exp_time').value;  // date-time format: yyyy-dd-mmThh:mm
    var req_json = {
        'car' : car_json,
        'path' : path_json,
        'fuel' : 'gasoline',
    };
   var header = {
        "Accept" :  "application/json",
        "Content-Type" : "application/json"
   };
   console.log(req_json);
   var url = "/submit_form";

   postRequest_submit(url, req_json, header, "output_div");
}

function postRequest_submit(url, data, header, output_div_id){
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.setRequestHeader("Accept", header["Accept"]);
    xhr.setRequestHeader("Content-Type", header["Content-Type"]);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
          console.log(xhr.status);
          cleanOutputElement(output_div_id);
          putRespInOutputElement(JSON.parse(xhr.responseText), output_div_id);
        }};
    
    let req_data = JSON.stringify(data);

    xhr.send(req_data);
}

function cleanOutputElement(output_div_id){
    var labelsInOutputDiv = document.getElementsByClassName(output_div_id);
    for(let i = 0; i < labelsInOutputDiv.length; i++){
        labelsInOutputDiv[i].innerHTML="";
    }
}

function putRespInOutputElement(resp_json, output_div_id){
    var output_div = document.getElementById(output_div_id);
    output_div.removeAttribute("hidden");

    // Fill information of the first options in routes
    document.getElementById("distance").innerHTML = resp_json['routes'][0]['distance'];
    document.getElementById("time").innerHTML = resp_json['routes'][0]['time'];
    document.getElementById("total").innerHTML = resp_json['routes'][0]['total'];
    
    document.getElementById("consumption").innerHTML = resp_json['consumption'];
    document.getElementById("price").innerHTML = resp_json['price'];
}