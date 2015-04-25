(function(){
    function range(start, stop, step) {
        if (arguments.length <= 1) {
            stop = start || 0;
            start = 0;
        }
        step = arguments[2] || 1;
        var length = Math.max (Math.ceil ((stop - start) / step) , 0);
        var idx = 0;
        var range = new Array(length);
        while (idx < length) {
            range[idx++] = start;
            start += step;
        }
        return range;
    }
    function _$rapyd$_in(val, arr) {
        if (arr instanceof Array || typeof arr === "string") return arr.indexOf(val) != -1;
        else {
            if (arr.hasOwnProperty(val)) return true;
            return false;
        }
    }
    function dir(item) {
        var arr = [];
        for (var i in item) {
            arr.push(i);
        }
        return arr;
    }
    function _$rapyd$_extends(child, parent) {
        child.prototype = new parent;
        child.prototype.constructor = child;
    }
    var j, str;
    j = jQuery;
            if (!JSON.stringify) {
        
    JSON.stringify = function(obj) {
        var t = typeof (obj);
        if (t != "object" || obj === null) {
            // simple data type
            if (t == "string")
                obj = '"' + obj + '"';
            if (t == "function")
                return; // return undefined
            else
                return String(obj);
        } else {
            // recurse array or object
            var n, v, json = []
            var arr = (obj && obj.constructor == Array);
            for (n in obj) {
                v = obj[n];
                t = typeof (v);
                if (t != "function" && t != "undefined") {
                    if (t == "string")
                        v = '"' + v + '"';
                    else if ((t == "object" || t == "function") && v !== null)
                        v = JSON.stringify(v);
                    json.push((arr ? "" : '"' + n + '":') + String(v));
                }
            }
            return (arr ? "[" : "{") + String(json) + (arr ? "]" : "}");
        }
    };
    ;
    }
    str = JSON.stringify;
    function kwargs(f) {
        var argNames;
        argNames = f.toString().match(/\(([^\)]+)/)[1];
        argNames = argNames ? argNames.split(",").map(function(s) {
            return s.trim();
        }) : [];
        return function() {
            var args, kw, i;
            args = [].slice.call(arguments);
            if (args.length) {
                kw = args.pop();
                if (typeof kw === "object") {
                    for (i = 0; i < argNames.length; i++) {
                        if (_$rapyd$_in(argNames[i], dir(kw))) {
                            args[i] = kw[argNames[i]];
                        }
                    }
                } else {
                    args.push(kw);
                }
            }
            return f.apply(this, args);
        };
    }
    function IndexError() {
        IndexError.prototype.__init__.apply(this, arguments);
    }
    _$rapyd$_extends(IndexError, Error);
    IndexError.prototype.__init__ = function __init__(message){
        var self = this;
        if (typeof message === "undefined") message = "list index out of range";
        self.name = "IndexError";
        self.message = message;
    };

    function TypeError() {
        TypeError.prototype.__init__.apply(this, arguments);
    }
    _$rapyd$_extends(TypeError, Error);
    TypeError.prototype.__init__ = function __init__(message){
        var self = this;
        self.name = "TypeError";
        self.message = message;
    };

    function ValueError() {
        ValueError.prototype.__init__.apply(this, arguments);
    }
    _$rapyd$_extends(ValueError, Error);
    ValueError.prototype.__init__ = function __init__(message){
        var self = this;
        self.name = "ValueError";
        self.message = message;
    };

    function AssertionError() {
        AssertionError.prototype.__init__.apply(this, arguments);
    }
    _$rapyd$_extends(AssertionError, Error);
    AssertionError.prototype.__init__ = function __init__(message){
        var self = this;
        if (typeof message === "undefined") message = "";
        self.name = "AssertionError";
        self.message = message;
    };

    if (!Array.prototype.map) {
        
	Array.prototype.map = function(callback, thisArg) {
		var T, A, k;
		if (this == null) {
			throw new TypeError(" this is null or not defined");
		}
		var O = Object(this);
		var len = O.length >>> 0;
		if ({}.toString.call(callback) != "[object Function]") {
			throw new TypeError(callback + " is not a function");
		}
		if (thisArg) {
			T = thisArg;
		}
		A = new Array(len);
		for (var k = 0; k < len; k++) {
			var kValue, mappedValue;
			if (k in O) {
				kValue = O[k];
				mappedValue = callback.call(T, kValue);
				A[k] = mappedValue;
			}
		}
		return A;
	};
	;
    }
    function map(oper, arr) {
        return list(arr.map(oper));
    }
    if (!Array.prototype.filter) {
        
	Array.prototype.filter = function(filterfun, thisArg) {
		"use strict";
		if (this == null) {
			throw new TypeError(" this is null or not defined");
		}
		var O = Object(this);
		var len = O.length >>> 0;
		if ({}.toString.call(filterfun) != "[object Function]") {
			throw new TypeError(filterfun + " is not a function");
		}
		if (thisArg) {
			T = thisArg;
		}
		var A = [];
		var thisp = arguments[1];
		for (var k = 0; k < len; k++) {
			if (k in O) {
				var val = O[k]; // in case fun mutates this
				if (filterfun.call(T, val))
					A.push(val);
			}
		}
		return A;
	};
	;
    }
    function filter(oper, arr) {
        return list(arr.filter(oper));
    }
    function sum(arr, start) {
        if (typeof start === "undefined") start = 0;
        return arr.reduce(function(prev, cur) {
            return prev + cur;
        }, start);
    }
    function deep_eq(a, b) {
        var i;
        "\n    Equality comparison that works with all data types, returns true if structure and\n    contents of first object equal to those of second object\n\n    Arguments:\n        a: first object\n        b: second object\n    ";
        if (a === b) {
            return true;
        }
        if (a instanceof Array && b instanceof Array || a instanceof Object && b instanceof Object) {
            if (a.constructor !== b.constructor || a.length !== b.length) {
                return false;
            }
            var _$rapyd$_Iter0 = dict.keys(a);
            for (var _$rapyd$_Index0 = 0; _$rapyd$_Index0 < _$rapyd$_Iter0.length; _$rapyd$_Index0++) {
                i = _$rapyd$_Iter0[_$rapyd$_Index0];
                if (b.hasOwnProperty(i)) {
                    if (!deep_eq(a[i], b[i])) {
                        return false;
                    }
                } else {
                    return false;
                }
            }
            return true;
        }
        return false;
    }
    String.prototype.find = String.prototype.indexOf;
    String.prototype.strip = String.prototype.trim;
    String.prototype.lstrip = String.prototype.trimLeft;
    String.prototype.rstrip = String.prototype.trimRight;
    String.prototype.join = function(iterable) {
        return iterable.join(this);
    };
    String.prototype.zfill = function(size) {
        var s;
        s = this;
        while (s.length < size) {
            s = "0" + s;
        }
        return s;
    };
    function list(iterable) {
        if (typeof iterable === "undefined") iterable = [];
        var result, i;
        result = [];
        var _$rapyd$_Iter1 = iterable;
        for (var _$rapyd$_Index1 = 0; _$rapyd$_Index1 < _$rapyd$_Iter1.length; _$rapyd$_Index1++) {
            i = _$rapyd$_Iter1[_$rapyd$_Index1];
            result.append(i);
        }
        return result;
    }
    Array.prototype.append = Array.prototype.push;
    Array.prototype.find = Array.prototype.indexOf;
    Array.prototype.index = function(index) {
        var val;
        val = this.find(index);
        if (val === -1) {
            throw new ValueError(str(index) + " is not in list");
        }
        return val;
    };
    Array.prototype.insert = function(index, item) {
        this.splice(index, 0, item);
    };
    Array.prototype.pop = function(index) {
        if (typeof index === "undefined") index = this.length - 1;
        return this.splice(index, 1)[0];
    };
    Array.prototype.extend = function(array2) {
        this.push.apply(this, array2);
    };
    Array.prototype.remove = function(item) {
        var index;
        index = this.find(item);
        this.splice(index, 1);
    };
    Array.prototype.copy = function() {
        return this.slice(0);
    };
    function dict(iterable) {
        var result, key;
        result = {};
        var _$rapyd$_Iter2 = iterable;
        for (var _$rapyd$_Index2 = 0; _$rapyd$_Index2 < _$rapyd$_Iter2.length; _$rapyd$_Index2++) {
            key = _$rapyd$_Iter2[_$rapyd$_Index2];
            result[key] = iterable[key];
        }
        return result;
    }
    if (typeof Object.getOwnPropertyNames !== "function") {
        dict.keys = function(hash) {
            var keys;
            keys = [];
            
        for (var x in hash) {
            if (hash.hasOwnProperty(x)) {
                keys.push(x);
            }
        }
        ;
            return keys;
        };
    } else {
        dict.keys = function(hash) {
            return Object.getOwnPropertyNames(hash);
        };
    }
    dict.values = function(hash) {
        var vals, key;
        vals = [];
        var _$rapyd$_Iter3 = dict.keys(hash);
        for (var _$rapyd$_Index3 = 0; _$rapyd$_Index3 < _$rapyd$_Iter3.length; _$rapyd$_Index3++) {
            key = _$rapyd$_Iter3[_$rapyd$_Index3];
            vals.append(hash[key]);
        }
        return vals;
    };
    dict.items = function(hash) {
        var items, key;
        items = [];
        var _$rapyd$_Iter4 = dict.keys(hash);
        for (var _$rapyd$_Index4 = 0; _$rapyd$_Index4 < _$rapyd$_Iter4.length; _$rapyd$_Index4++) {
            key = _$rapyd$_Iter4[_$rapyd$_Index4];
            items.append([key, hash[key]]);
        }
        return items;
    };
    dict.copy = dict;
    dict.clear = function(hash) {
        var key;
        var _$rapyd$_Iter5 = dict.keys(hash);
        for (var _$rapyd$_Index5 = 0; _$rapyd$_Index5 < _$rapyd$_Iter5.length; _$rapyd$_Index5++) {
            key = _$rapyd$_Iter5[_$rapyd$_Index5];
            delete hash[key];
        }
    };
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

    function Request() {
    }
    Request.send_json = function send_json(url, request_data, success_handler, error_handler){
        if (typeof success_handler === "undefined") success_handler = null;
        if (typeof error_handler === "undefined") error_handler = null;
        if (!success_handler) {
            success_handler = Request.flash_handler;
        }
        if (!error_handler) {
            error_handler = Request.flash_handler;
        }
        return j.ajax({
            "type": "POST",
            "url": url,
            "dataType": "json",
            "contentType": "application/json; charset=utf-8",
            "data": JSON.stringify(request_data),
            "success": success_handler,
            "error": error_handler
        });
    };
    Request.flash_handler = function flash_handler(response){
        var t;
        if (response["message"]) {
            if (response["type"]) {
                t = response["type"];
            } else {
                t = null;
            }
            new Notification(response["message"], t);
        } else {
            new Notification(response);
        }
    };

    function SiteTree() {
        SiteTree.prototype.__init__.apply(this, arguments);
    }
    SiteTree.prototype.get_url = function get_url(node){
        var self = this;
        if (node.id === "#") {
            return "/admin/get_sitetree";
        } else {
            return "/admin/get_sitetree/" + node.id;
        }
    };
    SiteTree.prototype.get_data = function get_data(node){
        var self = this;
        return {
            "id": node.id
        };
    };
    SiteTree.prototype.add_child_page = function add_child_page(){
        var self = this;
        return null;
    };
    SiteTree.prototype.delete_page = function delete_page(){
        var self = this;
        return null;
    };
    SiteTree.prototype.get_menu_items = function get_menu_items(){
        var self = this;
        return {
            "renameItem": {
                "label": "Add Child Page",
                "action": self.add_child_page
            },
            "deleteItem": {
                "label": "Delete Page",
                "action": self.delete_page
            }
        };
    };
    SiteTree.prototype.on_dblclick = function on_dblclick(event, data){
        var self = this;
        var clicked_node;
        clicked_node = j(event.target).closest("a");
        window.location.href = clicked_node.attr("href");
    };
    SiteTree.prototype.on_move_node = function on_move_node(event, data){
        var self = this;
        var new_parent_id, node_id, request_data;
        if (data.parent !== "#") {
            new_parent_id = j("#" + data.parent).data("pageid");
        } else {
            new_parent_id = null;
        }
        node_id = data.node.li_attr["data-pageid"];
        request_data = {
            "id": node_id,
            "new_parent": new_parent_id,
            "new_position": data.position
        };
        Request.send_json(self.sort_url, request_data);
    };
    SiteTree.prototype.__init__ = function __init__(node){
        var self = this;
        var types, key;
        self.node = node;
        self.properties = node.data("properties");
        types = {};
        var _$rapyd$_Iter6 = dict.keys(self.properties);
        for (var _$rapyd$_Index6 = 0; _$rapyd$_Index6 < _$rapyd$_Iter6.length; _$rapyd$_Index6++) {
            key = _$rapyd$_Iter6[_$rapyd$_Index6];
            types[key] = {
                "valid_children": self.properties[key].allowed_children,
                "icon": self.properties[key].icon
            };
        }
        self.tree = node.jstree({
            "core": {
                "check_callback": true,
                "data": {
                    "url": self.get_url,
                    "data": self.get_data
                }
            },
            "plugins": [ "contextmenu", "dnd", "types", "wholerow" ],
            "contextmenu": {
                "items": self.get_menu_items
            },
            "dnd": {
                "copy": false
            },
            "types": types
        });
        self.sort_url = self.node.data("sort_url");
        self.node.on("dblclick.jstree", j.proxy(self.on_dblclick, self));
        self.node.on("move_node.jstree", j.proxy(self.on_move_node, self));
    };

    function init() {
        if (document.querySelector("#tree")) {
            new SiteTree(j("#tree"));
        }
    }
    j(document).on("silverflask:panel_ready", init);
})();