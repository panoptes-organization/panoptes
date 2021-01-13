
/*Initialization of search field. Adding a listener on the field as soon as the page loads.
* Everytime we type inside the search field,
* */

$( document ).ready(function() {
    //listener for every delete table button
    $('.delete').click(function(event) {
        let button = $(event.target);
        let table = button.closest('table').DataTable();
        let row = table.row(event.target.closest('tr'));
        let id = event.target.closest('tr').firstElementChild.innerText;
        let modal = $('#deleteConfirmationModal');
        modal.attr('rowId',id);
        modal.attr('rowIndex',row.index());
        modal.attr('tableId',button.closest('table').attr('id'));
        modal.find('.modal-body').html(
            '<p>Do you want to delete workflow with ID: '+id+'?</p>');
        modal.modal('show');
    });

    //listener for deleteConfirmationModal's OK button
    $('.confirmDelete').click(function(myEvt) {
        let deleteConfirmationModal = $('#deleteConfirmationModal');
        deleteConfirmationModal.modal('hide');
         let rowId = deleteConfirmationModal.attr('rowId');
         let rowIndex = deleteConfirmationModal.attr('rowIndex');
         let tableId = deleteConfirmationModal.attr('tableId');
         deleteWorkflow(rowId,rowIndex,tableId);
    });

        //listener for deleteConfirmationModal's OK button
    $('.confirmDeleteAll').click(function() {
         deleteAllWorkflows();
    });

    //listener for deleteFailedModal's or editFailedModal's OK buttons
    $('.renameFailed, .deleteFailed').click(function(myEvt) {
        location.reload();
    });

    //initialization of all tables
    let tables = document.getElementsByClassName("fullTable");
    for(let t of tables){
        let table = $(t).DataTable({
            "ordering": true, // false to disable sorting (or any other option)
            "paging":true,
              columnDefs: [
                  {
                      targets: "_all",
                      className: 'dt-center'
                  }],
            "initComplete": function() {
                $("#workFlowsTable_wrapper")
                    .prepend('<div class="dataTables_length"><button id="deleteAll" title="Clean up database" class="btn btn-danger delete">' +
                        '<i class="far fa-trash-alt fa-xl"></i></button></div>');
                if (this.DataTable().rows().count() === 0 ) {
                    $("#deleteAll").attr("disabled","");
                }
                else{
                    $("#deleteAll").attr("enabled","");
                }
            }
        });
        $('.dataTables_length').addClass('bs-select');

    }

    $('#deleteAll').click(function(event) {
        let modal = $('#deleteAllConfirmationModal');
        modal.find('.modal-body').html(
            '<p>This operation will delete all workflows, even running ones.<br>Do you want to delete all workflows?  </p>');
        modal.modal('show');
    });

    let informTables = document.getElementsByClassName("informTable");
    for(let t of informTables){
        $(t).DataTable({
            "ordering": false, // false to disable sorting (or any other option)
            "paging":false,
            "searching":false,
            "info":false,
              columnDefs: [
                  {
                      targets: "_all",
                      className: 'dt-center'
                  }]
        });
        $('.dataTables_length').addClass('bs-select');
    }


    //listener for add button (add button is enabled after clicking the edit button)
    $(document).on("click", ".add", function(event){
     let idColumn = event.target.closest('tr').children[0];
     let aTag = $(idColumn).children().get(0);
     let href;
     //in some tables, there's no url in the name field
     if($(aTag) && $(aTag).is("a")){
        href = aTag.href;
     }
		var empty = false;
        //getting user's input for multiple inputs, for now it's just one.
		var input = $(this).parents("tr").find('input[type="text"]');
        input.each(function(){
			if(!$(this).val()){
				$(this).addClass("error");
				empty = true;
			} else{
                $(this).removeClass("error");
            }
		});
		$(this).parents("tr").find(".error").first().focus();
		//if there's no input error
		if(!empty){
			input.each(function(){
			    let field = $(this);
			    let newValue  = $(this).val();
			    //create a tag with input as text value
                let updateData = {"name":$(this).val()};
                //call the backend to store the updatedData
                $.ajax({
                    url: "/api/workflow/" + idColumn.innerText,
                    method: "PUT",
                    contentType: "application/json",
                    data: JSON.stringify(updateData),
                    timeout: 2000,
                    async: true,
                    success: function (data, textStatus, jqXHR) {
                        if (href) {
                            let atag = "<a href='" + href + "'>" + newValue + "</a>";
                            $(field).parent("td").html(atag);
                        } else {
                            $(field).parent("td").html(newValue);
                        }
                    },
                    //in case of error, we show an error modal
                    error: function (data, jqXHR, textStatus, errorThrown) {
                        console.log("Error renaming field in database");
                        let editFailedModal = $("#editFailedModal");
                        editFailedModal.find('.modal-body').html(
                            '<p>Renaming the workflow failed, page will reload</p>');
                        editFailedModal.modal('show');
                    }
                });
			});
			$(this).parents("tr").find(".add, .edit").toggle();
		}
    });

    // Edit row's name field on edit button click
	$(document).on("click", ".edit", function(){
	    $(this).parents("tr").find("td:nth-child(2)").html('<input type="text" class="form-control" value="' + $(this).parents("tr").children().get(1).innerText + '">');
		//we hide the edit button, so that the add button can appear
	    $(this).parents("tr").find(".edit").hide();
		$(this).parents("tr").find(".add").css("display","inline-block");
    });
});

window.onload = function(){
    document.getElementById("search").addEventListener("keyup", event => {
        //we don't support searching IME composition, see Microsoft IME for details
        if (event.isComposing || event.keyCode === 229) {
        //do nothing
        }
        else {
          // if the key pressed is the "enter" key, we redirect to our new page, sending the user's
          // input as a url parameter
          if (event.keyCode === 13 && document.getElementById("search").value !== "") {
              window.location.replace("/searchResults?q=" + document.getElementById("search").value)
          }
        }
});
};

function deleteWorkflow(rowId,rowIndex, tableId) {
    let table = $('#' + tableId).DataTable();
    let row = table.row(rowIndex);
    //call backend to delete the workflow
    $.ajax({
        url: "/api/workflow/" + rowId,
        method: "DELETE",
        async: true,
        timeout: 2000,
        success: function (data, textStatus, jqXHR) {
            if (location.pathname.includes("/workflow/")) {
                //if we are in a specific workflow page and we delete it, we redirect to /workflows
                location.href = "/workflows";
            } else {
                table
                    .row(row)
                    .remove()
                    .draw(false);
                //delete completed, hide the modal
                if ($('#workFlowsTable').DataTable().rows().count() === 0 ) {
                    $("#deleteAll").attr("disabled","");
                }
                $('#deleteConfirmationModal').modal('hide');
            }
        },
        //on error, show fail modal
        error: function (data, jqXHR, textStatus, errorThrown) {
            let deleteFailedModal = $("#deleteFailedModal");
            deleteFailedModal.find('.modal-body').html(
                '<p>Deleting the workflow failed, page will reload</p>');
            deleteFailedModal.modal('show');
        }
    });
}

function deleteAllWorkflows(){
     let table = $('#workFlowsTable').DataTable();
     //call backend to delete the workflow
     $.ajax({
         url: "/api/workflows/all",
         method: "DELETE",
         async: true,
         timeout: 2000,
         success: function (data, textStatus, jqXHR) {
             table
                 .clear()
                 .draw(false);
                 //delete completed, hide the modal
                if ($('#workFlowsTable').DataTable().rows().count() === 0 ) {
                    $("#deleteAll").attr("disabled","");
                }
             $('#deleteAllConfirmationModal').modal('hide');
         },
         //on error, show fail modal
         error: function (data, jqXHR, textStatus, errorThrown) {
             let deleteFailedModal = $("#deleteFailedModal");
             deleteFailedModal.find('.modal-body').html(
                 '<p>Deleting all workflows failed, page will reload</p>');
             deleteFailedModal.modal('show');
         }
     });
}
