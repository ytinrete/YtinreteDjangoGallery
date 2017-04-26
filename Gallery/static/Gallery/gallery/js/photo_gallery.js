
function addBlock(name, src){
    var dataList = $("#dataList").get(0)
    var html = dataList.innerHTML
    html += '<div class="list-group-item card"><h2 class="item-name" id="fileName">'
    html += decodeURIComponent(name)
    html+= '</h2><img class ="item-img" id="pic" src="'
    html += 'getImage/?path='+src
    html+='"/>'
    dataList.innerHTML = html
}



$(function () {
    // 6 create an instance when the DOM is ready

    $('#jstree').jstree({
      "core" : {
        "animation" : 0,
        "check_callback" : true,
        "themes" : { "stripes" : true },
        'data' : {
          'url' : function (node) {
            aaa = node.path
            return node.id === '#' ?
              'getJsTreePath/?' : 'getJsTreePath/?path='+node.id;
          },
          'data' : function (node) {
            return { 'id' : node.id };
          }
        }
      },
      "types" : {
        "#" : {
          "valid_children" : ["folder"]
        },
        "folder" : {
          "valid_children" : ["default"]
        },
        "file" : {
          "icon" : "glyphicon glyphicon-file",
          "valid_children" : []
        },
        "default" : {
          "valid_children" : ["default","file"]
        }
      },
      "plugins" : [
        "contextmenu", "dnd", "search",
        "state", "types", "wholerow"
      ]
    });

    // 7 bind to events triggered on the tree
    $('#jstree').on("changed.jstree", function (e, data) {
//      console.log(data.selected);
    });

    $("#jstree").bind("select_node.jstree", function (e, data) {

        if(data.node.text.endsWith('.jpg')){

            var dataList = $("#dataList").get(0)
            dataList.innerHTML = ""
            addBlock(data.node.id, data.node.id)

            var navPath = $("#navPath").get(0)
            navPath.innerHTML = decodeURIComponent(data.node.id)
        }
    });

  });

// Variable to hold request
var request;

// Bind to the submit event of our form
$("#search").submit(function(event){

    // Prevent default posting of form - put here to work in case of errors
    event.preventDefault();

    // Abort any pending request
    if (request) {
        request.abort();
    }
    // setup some local variables
    var $form = $(this);

    // Let's select and cache all the fields
    var $inputs = $form.find("input, select, button, textarea");

    // Serialize the data in the form
    var serializedData = $form.serialize();

    // Let's disable the inputs for the duration of the Ajax request.
    // Note: we disable elements AFTER the form data has been serialized.
    // Disabled form elements will not be serialized.
    $inputs.prop("disabled", true);

    // Fire off the request to /form.php
    request = $.ajax({
        url: "searchPhoto",
        type: "get",
        data: serializedData
    });

    // Callback handler that will be called on success
    request.done(function (response, textStatus, jqXHR){
        // Log a message to the console
        console.log("Hooray, it worked!");

        var dataList = $("#dataList").get(0)
        dataList.innerHTML = ""

        if(response.length==0){
            addBlock("no such photo", "404,jpg")
        }

        for(var count=0;count<response.length;count++){
            addBlock(response[count]["path"], response[count]["path"])
        }

    });

    // Callback handler that will be called on failure
    request.fail(function (jqXHR, textStatus, errorThrown){
        // Log the error to the console
        console.error(
            "The following error occurred: "+
            textStatus, errorThrown
        );
    });

    // Callback handler that will be called regardless
    // if the request failed or succeeded
    request.always(function () {
        // Reenable the inputs
        $inputs.prop("disabled", false);
    });

});

