/**
 * This function searches for the user input inside the table's rows
 * in the column "nameColumn". We show the rows that match our input
 * and hide the rest
 *
 * @param {string} event - The event of writing inside the search field
 */
function tableSearch(event) {
    let value = document.getElementById("search").value;
    for (const row of document.getElementsByClassName("tableRow")) {
        let name = row.querySelectorAll(".nameColumn")[0].innerText;
        if (!name.toLowerCase().includes(value)) {
            row.setAttribute("hidden","");
        }
            else {
            row.removeAttribute("hidden");
        }
	}
}