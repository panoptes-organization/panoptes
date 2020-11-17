
/*Initialization of search field. Adding a listener on the field as soon as the page loads.
* Everytime we type inside the search field,
* */
window.onload = function(){
    document.getElementById("search").addEventListener("keyup", event => {
        //we don't support searching IME composition, see Microsoft IME for details
        if (event.isComposing || event.keyCode === 229) {
        return;
      }
      else {
          tableSearch(event);
          // if the key pressed is the "enter" key, we redirect to our new page, sending the user's
          // input as a url parameter
          if (event.keyCode === 13 && document.getElementById("search").value !== "") {
              window.location.replace("/searchResults?q=" + document.getElementById("search").value)
          }
      }
});
};
