(function(){
    function _$rapyd$_extends(child, parent) {
        child.prototype = new parent;
        child.prototype.constructor = child;
    }
    function Notification() {
        Notification.prototype.__init__.apply(this, arguments);
    }
    Notification.prototype.__init__ = function __init__(text, type, timeout){
        var self = this;
        if (typeof timeout === "undefined") timeout = 2e3;
        self.noty = noty({
            "text": text,
            "layout": "topRight",
            "theme": "relax",
            "type": type,
            "animation": {
                "open": "animated fadeInRight",
                "close": "animated fadeOutRight",
                "easing": "swing",
                "speed": 500
            },
            "timeout": timeout,
            "buttons": false
        });
    };
    Notification.init_from_node = function init_from_node(node){
        node.hide();
        return new Notification(node.text(), node.data("type"));
    };

})();