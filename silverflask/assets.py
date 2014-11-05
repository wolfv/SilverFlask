from flask_assets import Bundle

common_css = Bundle(
    'css/vendor/flexboxgrid.css',
    'css/vendor/helper.css',
    'js/vendor/tree/themes/default/style.min.css',
    'js/vendor/livingdocs-engine/dist/css/livingdocs.css',
    'js/vendor/livingdocs-engine/public/assets/css/normalize.css',
    'js/vendor/livingdocs-engine/public/assets/css/livingdocs.css',
    'js/vendor/livingdocs-engine/public/assets/css/main.css',
    'css/main.css',
    filters='cssmin',
    output='public/css/common.css'
)

common_js = Bundle(
    'js/vendor/livingdocs-engine/components/jquery/jquery.js',
    'js/vendor/bootstrap.min.js',
    'js/vendor/jquery.dataTables.js',
    'js/vendor/jquery-ui.js',
    'js/vendor/jquery.dataTables.rowReordering.js',
    'js/vendor/tree/jstree.min.js',
    'js/vendor/jQuery-File-Upload-9.8.0/js/vendor/jquery.ui.widget.js',
    'js/vendor/jQuery-File-Upload-9.8.0/js/jquery.iframe-transport.js',
    'js/vendor/jQuery-File-Upload-9.8.0/js/jquery.fileupload.js',
    'js/vendor/jQuery-File-Upload-9.8.0/js/jquery.fileupload-process.js',
    'js/vendor/jQuery-File-Upload-9.8.0/js/jquery.fileupload-image.js',
    'js/vendor/livingdocs-engine/components/editable/editable.js',
    'js/vendor/livingdocs-engine/public/designs/bootstrap/design.js',
    'js/vendor/livingdocs-engine/dist/livingdocs-engine.js',
    Bundle(
        'js/main.js',
        filters='jsmin'
    ),
    output='public/js/common.js'
)
