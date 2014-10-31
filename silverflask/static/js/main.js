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
            data: {
                'url': function (node) {
                    return node.id === '#' ?
                        '/admin/get_sitetree' :
                        '/admin/get_sitetree/' + node.id;
                },
                'data': function (node) {
                    return { 'id': node.id };
                }
            }
        },
        'plugins': ['contextmenu'],
        'contextmenu': {
            "items": customMenu
        }
    }).on('dblclick.jstree', function(e, data) {
        var node = $(e.target).closest("a");
        window.location.href = node.attr("href")
    });



    /// Upload

    var uploader = new plupload.Uploader({
        runtimes: 'html5',
        browse_button: 'pickfiles', // you can pass in id...
        container: $('container')[0], // ... or DOM Element itself
        max_file_size: '10mb',

        // Fake server response here
        // url : '../upload.php',
        url: "/admin/upload",

        filters: [
            {title: "Image files", extensions: "jpg,gif,png"},
            {title: "Zip files", extensions: "zip"}
        ],

        init: {
            PostInit: function () {
                document.getElementById("filelist").innerHTML = "";
                $('#uploadfiles').click(function () {
                    uploader.start();
                    return false;
                });
            },

            FilesAdded: function (up, files) {
                console.log(files)
                plupload.each(files, function (file) {
                    document.getElementById("filelist").innerHTML += '<div id="' + file.id + '">' + file.name + ' (' + plupload.formatSize(file.size) + ') <b></b></div>';
                });
            },

            UploadProgress: function (up, file) {
                document.getElementById(file.id).getElementsByTagName('b')[0].innerHTML = '<span>' + file.percent + "%</span>";
            },

            Error: function (up, err) {
                $('console')[0].innerHTML += "\nError #" + err.code + ": " + err.message;
            }
        }
    });

    uploader.init();

    // Setup the design and the document
//    doc.config({livingDocsCss: "static/js/vendor/livingdocs-engine/public/assets/css/livingdocs.css"})
    doc.design.load(design.bootstrap);




    // Create Views
    window.lvds = []
    $(".editor-section").each(function(index) {
        var data_json = $("#" + $(this).data('for') + "_json").val();
        var lvd;
        IS_JSON = true;
        var parsed_json = null;
        try {
            parsed_json = jQuery.parseJSON(data_json);
        }
        catch(err) {
            IS_JSON = false;
        }
        console.log(doc.config)
        if(IS_JSON) {
            lvd = doc.new({
                data: parsed_json,
                design: 'bootstrap'
            });
        } else {
            lvd = doc.new({
                design: 'bootstrap'
            });
            addDefaultContent(lvd);
        }

        lvd.for_id = $(this).data('for');
        lvd.on('change', function(ctx){console.log("super"), console.log(ctx)})
        // Add some content
        window.lvds.push(lvd);

        function addUploadField(snippet, view) {
            var ip = $("<input>", {
                'id': '#fileupload',
                'class': 'hidden',
                'name': "file",
                'type': 'file'
            });
            $("body").append(ip);

            ip.fileupload({
                dataType: 'json',
                url: '/admin/upload',
                dropZone: view.$elem,
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
                    url = "http://" + window.location.host + data.result.files[0].url
                    snippet.setContent('image', {"url": url});
                    $.each(data.result.files, function (index, file) {
                        $('<p/>').text(file.name).appendTo(document.body);
                    });
                }
            });

        }

        window.viewReady = lvd.createView('.editor-section', { interactive: true });
        window.viewReady.done(function(ret) {
            ret.renderer.readySemaphore.callbacks.push(function(cb) {
                var snippetViews = ret.renderer.snippetViews;
                var snippetTree = ret.renderer.snippetTree;
                snippetTree.find("image").each(function (snippet) {
                    var view = snippetViews[snippet.id];
                    addUploadField(snippet, view);
                });
            });
        });
        lvd.interactiveView.page.focus.snippetFocus.add(function(cursor){
            console.log("snippet focus yaddayadda", cursor);
//            cursor.setImage('image', "http://" + window.location.host + "/static/uploads/spiderman.jpg")
        });

        lvd.interactiveView.page.editableController.selection.add(function(view, element, selection) {
            console.log("This selection has changed.", view, element, selection);
            window.current_selection = selection;
        });
        window.view_document = lvd.interactiveView.page.$body;
        $("body").keydown(function (e) {
//            e.preventDefault();
        });
        $("body").keypress(function (e) {
//            console.log(e)
//            e.preventDefault();
        });

        view_document.keydown(function(e) {
            if (e.keyCode == 73 && e.ctrlKey) {
                e.preventDefault();
                if(current_selection)
                    current_selection.toggleEmphasis();
                return false;
            }
            else if (e.keyCode == 66 && e.ctrlKey) {
                e.preventDefault();
                if (current_selection)
                    current_selection.toggleBold();
                return false;
            }
        })
        function browserDrop(event, snippetDrag) {
            console.log("What did you drop")
            console.log(event)
            console.log(snippetDrag)
        }
        function dragCallback(event) {
            lvd.interactiveView.page.startDrag({
                'event': event,
                'config': {
                    'preventDefault': true,
                    'direct': true,
                    'onDrop': browserDrop
                }
            });
        }

        lvd.interactiveView.page.readySemaphore.callbacks.push(function() {
            lvd.snippetTree.each(function(snippet) {
                el = snippet.$elem
                console.log("adding a filuploads")
            });
            console.log($("#fileupload", view_document))

        });


        view_document.on("click", ".img-polaroid", function() {
            console.log("alter krass");
        });

        view_document.ready(function(){
            console.log("Shit is ready");
            $("div", view_document).on("click", function() {
                $(this).css("background", "red")
            })
        })

        var $toolbar = $('.doc-toolbar');
        for (var i = 0; i < lvd.design.templates.length; i++) {
            var template = lvd.design.templates[i];
            $entry = $('<div class="toolbar-entry">');
            $entry.html(template.title);
            $toolbar.append($entry);
            draggableSnippet(lvd, template.id, $entry);
        }
    });

    function draggableSnippet(lvd, id, $elem) {
        $elem.on('mousedown', function (event) {
            var newSnippet = lvd.model.createModel(id);
            console.log("Dragging started")
            doc.startDrag({
                snippetModel: newSnippet,
                event: event,
                config: {
                    preventDefault: true,
                    direct: true
                }
            });
        });
    }

    function addDefaultContent(lvd) {
        lvd.model.append('mainAndSidebar');
        var snippet = lvd.model.createSnippet('hero');
        lvd.model.first().append('main', snippet);
        var text = lvd.model.createSnippet('text');
        snippet.after(text);
    }

    $("form").on('submit', function(e) {
        window.lvds.forEach(function(lvd) {
            var rendered_html = lvd.toHtml();
            console.log($("#" + lvd.for_id))
            console.log("#" + lvd.for_id)
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
        var gf_url = "/admin/gridfield/" + t.attr("id");
        t.DataTable({
            ajax: gf_url,
            "columns": c
        })
    });

});