$(document).ready(function(){
	
	// Select/Deselect checkboxes
	var checkbox = $('table tbody input[type="checkbox"]');
	$("#selectAll").click(function(){
		if(this.checked){
			checkbox.each(function(){
				this.checked = true;                        
			});
		} else{
			checkbox.each(function(){
				this.checked = false;                        
			});
		} 
	});
	checkbox.click(function(){
		if(!this.checked){
			$("#selectAll").prop("checked", false);
		}
	});


	$("#btnCertify").click(function () {
		console.log("Certify clicked.");
		var message ="";
		var idArray = [];
		var idString = "";
		// PUT SHOPNUMBER IN ARRAY OF IDs
		idArray.push(document.getElementById("shopNumber").innerHTML);
	
		// PUT TRAINING CLASS ID INTO ARRAY OF IDs
		idArray.push(document.getElementById("trainingClassID").innerHTML);


		//Loop through all checked CheckBoxes in GridView.
		$("#checkbox1:checked").each(function () {
			var row = $(this).closest("tr")[0];
			message += row.cells[2].innerHTML;
			message += "   " + row.cells[1].innerHTML;
			message += "   " + row.cells[3].innerHTML;
			message += "\n";
			idArray.push(row.cells[2].innerHTML);
			idString += (row.cells[2].innerHTML +',');
		});	
		// Creating a XHR object 
		let xhr = new XMLHttpRequest(); 
		let url = "/certifySelected"; 
	
		// Open a connection 
		xhr.open("POST", url, true); 
		// Set the request header i.e. which type of content you are sending 
		xhr.setRequestHeader("Content-Type", "application/json"); 

		// Create a state change callback 
		xhr.onreadystatechange = function () { 
			if (xhr.readyState === 4 && xhr.status === 200) { 
				// Print received data from server 
				result.innerHTML = this.responseText;
				console.log("Result - " + result.innerHTML)
				alert(result.innerHTML)
				//console.log('Result - ' + result.innerHTML) 
			} 
		}; 

		// Converting JSON data to string 
		var data = JSON.stringify(idArray); 
		// Sending data with the request 
		xhr.send(data); 
		alert('Data sent') 
		
	});
});
	/*function() {
		var httpRequest;
		document.getElementById("ajaxButton").addEventListener('click', makeRequest);
	  
		function makeRequest() {
		  httpRequest = new XMLHttpRequest();
	  
		  if (!httpRequest) {
			alert('Giving up :( Cannot create an XMLHTTP instance');
			return false;
		  }
		  httpRequest.onreadystatechange = alertContents;
		  httpRequest.open('GET', 'test.html');
		  httpRequest.send();
		}
	  
		function alertContents() {
			try {
				if (httpRequest.readyState === XMLHttpRequest.DONE) {
					if (httpRequest.status === 200) {
					alert(httpRequest.responseText);
					} else {
					errorMsg='Status of request -'+httpRequest.status;
					alert(errorMsg);
					alert('There was a problem with the request.');
					}
				}
			}
			catch(e) {
				alert('Caught Exception: ' + e.description);
			}
		  }
		
}) */ 
	

	
		//var id = 3;
		//idArray.unshift(id);
		//msg = "idArray w/id -" + idArray;
		//console.log(msg);

/*		const href = window.location.href;

		const params = new URLSearchParams(window.location.search);  
		const URLid = params.get("id"); 
		msg = "URL -" + href + ' ?' + URLid; 
		console.log(msg);
*/
		//$.ajax({
		//	type : 'POST',
		//	url: '/postmethod',
		//	dataType: 'json',
		//	data : JSON.stringify(idArray),
		//	contentType:"application/json; charset=UTF-8"
		//}); 
		
		//Display selected Row data in Alert Box.
		//alert(message);	
		//alert(idString);