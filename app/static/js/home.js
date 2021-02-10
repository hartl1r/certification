// TEST FOR LOADED PAGE
//$('.datepicker').pickadate()

window.onload=function(){
    shop1Routine();
    shop2Routine();
    }
// staffID = localStorage.getItem('staffID')
// if (!staffID) {
//     staffID = prompt("Enter staff ID - ")
//     localStorage.setItem('staffID',staffID)
// }

// DEFINE EVENT LISTENERS
document.getElementById('selectpicker').addEventListener('change',memberSelectedRtn)
document.getElementById("cancelMemberID").addEventListener("click",cancelMember)
document.getElementById("processMemberID").addEventListener("click",processMember)
document.getElementById('certifiedRA').onclick = function(ev) {
    if (ev.target.checked) {
        document.getElementById('certifiedRA').value='True'
    }
    else {
        document.getElementById('certifiedRA').value='False' 
    }
}
document.getElementById('certifiedBW').onclick = function(ev) {
    if (ev.target.checked) {
        document.getElementById('certifiedBW').value='True'
    }
    else {
        document.getElementById('certifiedBW').value='False' 
    }
}
function shop1Routine() {
    // SET BUTTONS FOR SHOP 1 (ROLLING ACRES)
    const shop1Table = document.getElementById("shop1Table")
    const shop1Rows = shop1Table.getElementsByTagName('tr')
    let irow = 2
    let seatsTaken = 0
    for (irow = 2; irow < shop1Rows.length; irow++) {
        let seatsTaken = shop1Table.rows[irow].cells[4].textContent
        const reportBtn = shop1Table.rows[irow].querySelector(".reportBtn")
        const viewBtn = shop1Table.rows[irow].querySelector(".viewBtn")
        const deleteBtn = shop1Table.rows[irow].querySelector(".deleteBtn")
        if (seatsTaken == "0") 
            {reportBtn.style.visibility = 'hidden'
            deleteBtn.style.visibility = 'visible'
            viewBtn.style.visibility = 'hidden'}
        else 
            {reportBtn.style.visibility = 'visible'
            deleteBtn.style.visibility = 'hidden'
            viewBtn.style.visibility = 'visible'}
    }
};

function shop2Routine() {
    // SET BUTTONS FOR SHOP 2 (BROWNWOOD)
    const shop2Table = document.getElementById("shop2Table")
    const shop2Rows = shop2Table.getElementsByTagName('tr')
    let irow = 2
    let seatsTaken = 0
    for (irow = 2; irow < shop2Rows.length; irow++) {
        let seatsTaken = shop2Table.rows[irow].cells[4].textContent
        const reportBtn = shop2Table.rows[irow].querySelector(".reportBtn")
        const viewBtn = shop2Table.rows[irow].querySelector(".viewBtn")
        const deleteBtn = shop2Table.rows[irow].querySelector(".deleteBtn")
        if (seatsTaken == "0") 
            {reportBtn.style.visibility = 'hidden'
            deleteBtn.style.visibility = 'visible'
            viewBtn.style.visibility = 'hidden'}
        else 
            {reportBtn.style.visibility = 'visible'
            deleteBtn.style.visibility = 'hidden'
            viewBtn.style.visibility = 'visible'}
    }
}
function memberSelectedRtn() {
    selectedMember = this.value
    lastEight = selectedMember.slice(-8)
    currentMemberID= lastEight.slice(1,7)
    document.getElementById('selectpicker').value=''
    console.log('currentMemberID - '+ currentMemberID)
    $.ajax({
        url : "/getMemberData",
        type: "GET",
        data : {
            memberID:currentMemberID,
            },
 
        success: function(data, textStatus, jqXHR)
        {
            if (data.hdgName) {
                document.getElementById('modalTitle').innerHTML = data.hdgName}

            if (data.memberID) {
                document.getElementById('memberID').value = data.memberID}

            if (data.homePhone) {
                document.getElementById('homePhone').value = data.homePhone}

            if (data.cellPhone) {
                document.getElementById('cellPhone').value = data.cellPhone}

            if (data.eMail) {
                document.getElementById('eMail').value = data.eMail}

            console.log('type of date.certifiedRAvalue - '+typeof(data.certifiedRAvalue))

            if (data.certifiedRAvalue == 'True') {
                document.getElementById('certifiedRA').checked = true}
                console.log('certifiedRAvalue - '+data.certifiedRAvalue)
            
            if (data.certifiedRAdate) {
                document.getElementById('certifiedRAdate').value = data.certifiedRAdate}
                console.log('CURRENT certifiedRAdate - '+ data.certifiedRAdate)

            if (data.certifiedBWvalue == 'True') {
                document.getElementById('certifiedBW').checked = true}

            if (data.certifiedBWdate) {
                document.getElementById('certifiedBWdate').value = data.certifiedBWdate}            
                    
        },
        error: function(result){
            alert("Error ..."+result)
        }
    })    
    $('#memberModalID').modal('show')
}

    // SET UP LINK TO MEMBER FORM 
//     var linkToMemberBtn = document.getElementById('linkToMember');
//     link='/index/' + currentMemberID +'/' + staffID
//     linkToMemberBtn.setAttribute('href', link)
//     linkToMemberBtn.click()
// }

function cancelMember() {
    $('#memberModalID').modal('hide')
}

function processMember() {
    memberID = document.getElementById('memberID').value
    homePhone = document.getElementById('homePhone').value
    cellPhone = document.getElementById('cellPhone').value
    eMail = document.getElementById('eMail').value
    certifiedRA = document.getElementById('certifiedRA')
    certifiedRAdate = document.getElementById('certifiedRAdate').value
    certifiedBW = document.getElementById('certifiedBW')
    certifiedBWdate = document.getElementById('certifiedBWdate').value
    
    if (certifiedRA.checked) {
        certifiedRAvalue ='true'
    }
    else {
        certifiedRAvalue='false'
    }
    if (certifiedBW.checked) {
        certifiedBWvalue ='true'
    }
    else {
        certifiedBWvalue='false'
    }
      
    $.ajax({
        url : "/updateMemberData",
        type: "GET",
        data : {
            memberID:memberID,
            homePhone:homePhone,
            cellPhone:cellPhone,
            eMail: eMail,
            certifiedRAvalue:certifiedRAvalue,
            certifiedRAdate:certifiedRAdate,
            certifiedBWvalue:certifiedBWvalue,
            certifiedBWdate:certifiedBWdate
            },

        success: function(data, textStatus, jqXHR)
        {
            alert(data.msg)
        },
        error: function(result){
            alert("Error ..."+result)
        }
    }) 
    
    $('#memberModalID').modal('hide')
}


