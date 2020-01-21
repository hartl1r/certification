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
		//Loop through all checked CheckBoxes in GridView.
		$("#checkbox1:checked").each(function () {
			var row = $(this).closest("tr")[0];
			message += row.cells[1].innerHTML;
			message += "   " + row.cells[2].innerHTML;
			message += "   " + row.cells[3].innerHTML;
			message += "\n";
			idArray.push(row.cells[1].innerHTML);
			idString += (row.cells[1].innerHTML +',');
		});
		
		var id = 3;
		idArray.unshift(id);
		msg = "idArray w/id -" + idArray;
		console.log(msg);

		const href = window.location.href;

		const params = new URLSearchParams(window.location.search);  
		const URLid = params.get("id"); 
		msg = "URL -" + href + ' ?' + URLid; 
		console.log(msg);

		$.ajax({
			type : 'POST',
			url: '/postmethod',
			dataType: 'json',
			data : JSON.stringify(idArray),
			contentType:"application/json; charset=UTF-8"
		}); 
		
		//Display selected Row data in Alert Box.
		alert(message);	
		
	});
	
});
