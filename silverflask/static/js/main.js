$(document).ready(function() {
//    function customMenu(node) {
//        // The default set of all items
//        var items = {
//            renameItem: { // The "rename" menu item
//                label: "Add Child Page",
//                action: function () {
//                },
//                submenu: {
//                    create_file: {
//                        label: "Add Page",
//                        action: function(context_node, node_id) {
//                            console.log(node.li_attr["data-pageid"])
//                            window.location.href = "/admin/add_page/Page?parent=" + node.li_attr["data-pageid"]
//                        }
//                    }
//                }
//            },
//            deleteItem: { // The "delete" menu item
//                label: "Delete",
//                action: function () {
//                }
//            }
//        };
//
//        if ($(node).hasClass("folder")) {
//            // Delete the "delete" menu item
//            delete items.deleteItem;
//        }
//
//        return items;
//    }
//
//
//    $('#tree').jstree({
//        'core': {
//            data: {
//                'url': function (node) {
//                    return node.id === '#' ?
//                        '/admin/get_sitetree' :
//                        '/admin/get_sitetree/' + node.id;
//                },
//                'data': function (node) {
//                    return { 'id': node.id };
//                }
//            }
//        },
//        'plugins': ['contextmenu'],
//        'contextmenu': {
//            "items": customMenu
//        }
//    }).on('dblclick.jstree', function(e, data) {
//        var node = $(e.target).closest("a");
//        window.location.href = node.attr("href")
//    });
//
//
//
//    /// Upload
//
//    var uploader = new plupload.Uploader({
//        runtimes: 'html5',
//        browse_button: 'pickfiles', // you can pass in id...
//        container: $('container')[0], // ... or DOM Element itself
//        max_file_size: '10mb',
//
//        // Fake server response here
//        // url : '../upload.php',
//        url: "/admin/upload",
//
//        filters: [
//            {title: "Image files", extensions: "jpg,gif,png"},
//            {title: "Zip files", extensions: "zip"}
//        ],
//
//        init: {
//            PostInit: function () {
//                document.getElementById("filelist").innerHTML = "";
//                $('#uploadfiles').click(function () {
//                    uploader.start();
//                    return false;
//                });
//            },
//
//            FilesAdded: function (up, files) {
//                console.log(files)
//                plupload.each(files, function (file) {
//                    document.getElementById("filelist").innerHTML += '<div id="' + file.id + '">' + file.name + ' (' + plupload.formatSize(file.size) + ') <b></b></div>';
//                });
//            },
//
//            UploadProgress: function (up, file) {
//                document.getElementById(file.id).getElementsByTagName('b')[0].innerHTML = '<span>' + file.percent + "%</span>";
//            },
//
//            Error: function (up, err) {
//                $('console')[0].innerHTML += "\nError #" + err.code + ": " + err.message;
//            }
//        }
//    });
//
//    uploader.init();

    // Setup the design and the document
    doc.design.load(design.bootstrap);
    var lvd = doc.new({
        design: 'bootstrap'
    });

    // Add some content
    addDefaultContent(lvd);

    // Create Views
    viewReady = lvd.createView('.editor-section', { interactive: true });
    previewReady = lvd.createView('.editor-preview');

    // Create Snippets
    var $toolbar = $('.doc-toolbar');
    for (var i = 0; i < lvd.design.templates.length; i++) {
        var template = lvd.design.templates[i];
        $entry = $('<div class="toolbar-entry">');
        $entry.html(template.title);
        $toolbar.append($entry);
        draggableSnippet(lvd, template.id, $entry);
    }


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

});