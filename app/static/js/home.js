// TEST FOR LOADED PAGE
window.onload=function(){
    shop1Routine();
    shop2Routine();
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
