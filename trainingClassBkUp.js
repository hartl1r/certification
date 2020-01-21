$(document).ready(function() {
	// Activate tooltip
	//$('[data-toggle="tooltip"]').tooltip();
	
	// Select/Deselect checkboxes
	var checkbox = $('table tbody input[type="checkbox"]');
});


/*	$("#selectAll").click(function(){
		if(this.checked){
			checkbox.each(function(){
				this.checked = true;                        
			});
		} else{
			checkbox.each(function(){
				this.checked = false;                        
			});
		}); */
	
/*
	checkbox.click(function(){
		if(!this.checked){
			$("#selectAll").prop("checked", false);
		});
	}); 
}); */

	/*function sendArray(Status) {
		$.ajax({
			type : "POST",
			url : '/queryJson',
			dataType: "json",
			data: JSON.stringify("1,2,3,4"),
			contentType: 'application/json;charset=UTF-8',
			success: function (data) {
				console.log(data);
				}
			})
		} */

	/* $("#selectAll2").click(function() {
		if(this.checked){
			checkbox.each(function(){
				this.checked = true;                        
			});
		} else{
			checkbox.each(function(){
				this.checked = false;                        
			});
		} 

	});	 */

/*	$("#btnCertify").click(function () {
		console.log("Certify clicked.");
		var message ="";
		var idArray = [];
		var idString = "";
		//Loop through all checked CheckBoxes in GridView.
		$("#checkbox1:checked").each(function () {
			var row = $(this).closest("tr")[0];
			message += row.cells[1].innerHTML;
			message += "   " + row.cells[2].innerHTML;
			message += "   " + row.cells[3].innerHTML;
			message += "\n";
			idArray.push(row.cells[1].innerHTML);
			idString += (row.cells[1].innerHTML +',');
			//Display selected Row data in Alert Box.
			alert(message);
			sendArray();
		});		
	});
}); */

/*	function loadDoc() {
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
		  if (this.readyState == 4 && this.status == 200) {
		   document.getElementById("demo").innerHTML = this.responseText;}
			};
		xhttp.open("GET", "ajax_info.txt", true);
		xhttp.send();
		} */


/* -------------------------------------------------------------------------------------------------		
	function sendArray() {
		var idArray = [];
		var idString = "";
		//Loop through all checked CheckBoxes in GridView.
		$("#checkbox1:checked").each(function () {
			var row = $(this).closest("tr")[0];
			message += row.cells[1].innerHTML;
			message += "   " + row.cells[2].innerHTML;
			message += "   " + row.cells[3].innerHTML;
			message += "\n";
			idArray.push(row.cells[1].innerHTML);
			idString += (row.cells[1].innerHTML +',');
			//Display selected Row data in Alert Box.
			alert(message);
		});

		$.get(
			url="queryExample",
			data={idArray}, 
			success=function(data) {
			   alert('page content: ' + data);
			)
		
	}
	 -------------------------------------------------------------------------------- */
		/* Send string to server
		var xhttp;  
		xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
				console.log(this.responseText);
				strArray=idArray.toString();
				msg="str = " + strArray;
				console.log(msg);
				console.log("before GET");
				xhttp.open("GET","/queryExample?language=Python",true);
				console.log("after GET");
				//xhttp.open("GET", "certifySelected?str="+str, true);
				xhttp.send();
				return false;}	
			else {
				console.log(this.responseText);
				return false;
			}  */
			//document.getElementById("txtHint").innerHTML = this.responseText;
			
/*		};
		
	}  */
