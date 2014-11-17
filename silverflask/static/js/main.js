$(document).ready(function() {
    function customMenu(node) {
        // The default set of all items
        var items = {
            renameItem: { // The "rename" menu item
                label: "Add Child Page",
                action: function () {
                },
                submenu: {
                    create_file: {
                        label: "Add Page",
                        action: function(context_node, node_id) {
                            console.log(node.li_attr["data-pageid"])
                            window.location.href = "/admin/add_page/Page?parent=" + node.li_attr["data-pageid"]
                        }
                    }
                }
            },
            deleteItem: { // The "delete" menu item
                label: "Delete",
                action: function () {
                }
            }
        };

        if ($(node).hasClass("folder")) {
            // Delete the "delete" menu item
            delete items.deleteItem;
        }

        return items;
    }

    $('#tree').jstree({
        'core': {
            "check_callback" : true,
            data: {
                'url': function (node) {
                    return node.id === '#' ?
                        '/admin/get_sitetree' :
                        '/admin/get_sitetree/' + node.id;
                },
                'data': function (node) {
                    return { 'id': node.id,
                        'abc': "asdjasljalksjdlasjkdajsdlkjasldja;lsj"
                    };
                }
            }
        },
        'plugins': ['contextmenu', 'dnd'],
        'contextmenu': {
            "items": customMenu
        },
        'dnd': {
            "copy": false
        }
    });

    $("#tree").on('dblclick.jstree', function(e, data) {
        var node = $(e.target).closest("a");
        window.location.href = node.attr("href")
    });

    $("#tree").on("move_node.jstree", function(e, data) {
        var new_parent_id = null;
        if(data.parent !== "#") {
            new_parent_id = $("#" + data.parent).data("pageid");
        }
        var self_id = data.node.li_attr["data-pageid"]
        var sort_url = $("#tree").data("sort_url")
        var send_data = {
            "new_parent": new_parent_id,
            "id": self_id,
            "new_position": data.position
        }
        $.ajax({
            type: "POST",
            url: sort_url,
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(send_data)
        });
        console.log("Drag finished.")
    });

    $(".async-upload-container").each(function(el, idx) {
        console.log("Doing this ", $(this))
        var self = $(this);
        var input = $("<input/>").prop("type", "file").addClass("hidden").prop("name", "file")
        $("body").append(input)
        input.fileupload({
            dataType: 'json',
            url: '/admin/upload',
            dropZone: self.children('.dropzone'),
            progressall: function () {
                console.log("progresstinating.")
            },
            add: function (e, data) {
                data.context = $('<p/>').text('Uploading...').appendTo($(this).parent());
                var img = document.createElement("img")
                img.file = data.files[0]
                img.classList.add("obj");
                $(this).parent()[0].appendChild(img)

                var reader = new FileReader();
                reader.onload = (function (aImg) {
                    return function (e) {
                        aImg.src = e.target.result;
                    };
                })(img);
                reader.readAsDataURL(data.files[0]);
                data.submit();
            },
            done: function (e, data) {
                url = "http://" + window.location.host + data.result.files[0].url;
                self.children("input[type=\"hidden\"]").val(data.result.files[0].id)
                $.each(data.result.files, function (index, file) {
                    $('<p/>').text(file.name).appendTo(document.body);
                });
            }
        });
        self.children('.open-file-dialog').click(function() {
            input.trigger("click")
        });
    });

    // Setup the design and the document
    // doc.config({livingDocsCss: "static/js/vendor/livingdocs-engine/public/assets/css/livingdocs.css"})
    doc.design.load(design.bootstrap);

    // Create Views
    window.livingdocs_elements = []

    $("form").on('submit', function(e) {
        window.livingdocs_elements.forEach(function(lvd) {
            var rendered_html = lvd.toHtml();
            $("#" + lvd.for_id).val(rendered_html);
            $("#" + lvd.for_id + "_json").val(lvd.toJson());
        });
    });

    $('.gridfield').each(function () {
        var t = $(this);
        var c = [];
        t.find("th").each(function (idx, el) {
            c.push({"data": $(el).data('col')})
        });
        c.pop()
        c.push({"data": "edit_url", render: function(data, type, row) {
            return "<a href=\"" + data + "\">Edit</a>"
        }});
        var gf_url = $(this).data('ajax-url');
        t.DataTable({
            ajax: gf_url,
            columns: c,
//            ordering: false,
            "order": [2, "asc"]
        })
        t.rowReordering({
            sURL: $(this).data("sort-url"),
            iIndexColumn: 2,
            fnUpdateAjaxRequest: function(oAjaxRequest, properties, $dataTable) {
                console.log(oAjaxRequest)
            }
        })
    });
});


window.silverflask_angular = angular.module('silverflask', ["ngImgCrop"])


angular.element(document).ready(function() {
    angular.bootstrap(document, ['silverflask']);
});

