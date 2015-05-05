from flask_assets import Bundle

common_css = Bundle(
    'js/bower_components/bootstrap/dist/css/bootstrap.css',
    'css/vendor/helper.css',
    'js/vendor/tree/themes/default/style.min.css',
    'js/bower_components/livingdocs-engine/dist/css/livingdocs.css',
    'js/bower_components/Plugins/integration/bootstrap/3/dataTables.bootstrap.css',
    # 'js/bower_components/ngImgCrop/compile/unminified/ng-img-crop.css',
    'js/bower_components/animate.css/animate.css',
    'css/main.css',
    filters='cssmin',
    output='public/css/common.css'
)

common_js = Bundle(
    'js/bower_components/jquery/dist/jquery.js',
    'js/bower_components/bootstrap/dist/js/bootstrap.js',
    'js/bower_components/datatables/media/js/jquery.dataTables.js',
    'js/bower_components/Plugins/integration/bootstrap/3/dataTables.bootstrap.js',
    'js/bower_components/jquery-ui/jquery-ui.js',
    'js/bower_components/jstree/dist/jstree.min.js',
    'js/bower_components/noty/js/noty/packaged/jquery.noty.packaged.js',
    'js/bower_components/noty/js/noty/themes/bootstrap.js',
    'js/bower_components/blueimp-file-upload/js/vendor/jquery.ui.widget.js',
    'js/bower_components/blueimp-file-upload/js/jquery.iframe-transport.js',
    'js/bower_components/blueimp-file-upload/js/jquery.fileupload.js',
    'js/bower_components/blueimp-file-upload/js/jquery.fileupload-process.js',
    'js/bower_components/blueimp-file-upload/js/jquery.fileupload-image.js',
    'js/bower_components/editable/editable.js',
    'js/bower_components/livingdocs-design-boilerplate/dist/design.js',
    'js/bower_components/livingdocs-engine/dist/livingdocs-engine.js',
    'css/mui/dist/js/mui.js',
    'js/vendor/jquery.dataTables.rowReordering.js',
    Bundle(
        'js/rapyd.js',
        'js/SiteTree.js',
        'js/editor.js',
        # 'js/crop.js',
        filters='jsmin'
    ),
    output='public/js/common.js'
)





