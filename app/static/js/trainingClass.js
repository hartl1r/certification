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
	