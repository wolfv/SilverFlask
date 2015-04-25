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
    function _$rapyd$_print() {
        var args, output;
        args = [].slice.call(arguments, 0);
        output = JSON.stringify(args);
        if ("console" in window) console.log(output.substr(1, output.length-2));
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

    function DOMNode() {
        DOMNode.prototype.__init__.apply(this, arguments);
    }
    DOMNode.prototype.__init__ = function __init__(node){
        var self = this;
        self.node = node;
        return self;
    };
    DOMNode.prototype.connect = function connect(event, callback, capture){
        var self = this;
        if (typeof capture === "undefined") capture = false;
        self.node.addEventListener(event, callback, capture);
    };

    function DOM() {
    }
    DOM.select = function select(self, selector, context){
        if (typeof context === "undefined") context = document;
        return new DOMNode(context.querySelector(selector));
    };

    function GridField() {
        GridField.prototype.__init__.apply(this, arguments);
    }
    GridField.render_actions = function render_actions(data, type, row){
        return "<a href=\"" + data + "\">Edit</a>";
    };
    GridField.prototype.__init__ = function __init__(node){
        var self = this;
        var header, renderer, visible;
        self.columns = [];
        self.node = node;
        var _$rapyd$_Iter6 = j("th", node);
        for (var _$rapyd$_Index6 = 0; _$rapyd$_Index6 < _$rapyd$_Iter6.length; _$rapyd$_Index6++) {
            header = _$rapyd$_Iter6[_$rapyd$_Index6];
            header = j(header);
            renderer = null;
            if (header.data("renderer")) {
                renderer = GridField[header.data("renderer")];
            }
            visible = true;
            if (j(header).data("hidden") === "True") {
                visible = false;
            }
            self.columns.append({
                "data": j(header).data("col"),
                "render": renderer,
                "visible": visible
            });
        }
        _$rapyd$_print(self.columns);
        self.table = self.node.DataTable({ajax: self.node.data("ajax-url"), columns: self.columns, ordering: false, order: [ 2, "asc" ]});
        if (self.node.data("sortable")) {
            self.node.dataTable().rowReordering({
                "sURL": self.node.data("sort-url"),
                "iIndexColumn": 2
            });
        }
    };

    function UploadField() {
        UploadField.prototype.__init__.apply(this, arguments);
    }
    UploadField.prototype.__init__ = function __init__(node){
        var self = this;
        var on_add, on_progress, on_done, on_fail, input;
        self.url = "/admin/upload";
        self.node = node;
        self.input = j("input[type='file']", self.node);
        self.button = j(".btn", self.node);
        self.button.on("click", function(e) {
            console.log(self.input);
            self.input.trigger("click", e);
        });
        self.preview_container = j(".preview_image", self.node);
        on_add = j.proxy(self.on_add, self);
        on_progress = j.proxy(self.on_progress, self);
        on_done = j.proxy(self.on_done, self);
        on_fail = j.proxy(self.on_fail, self);
        self.input.fileupload({
            "dataType": "json",
            "url": self.url,
            "dropZone": self.node.children(".dropzone"),
            "progress": on_progress,
            "add": on_add,
            "done": on_done,
            "fail": on_fail
        });
        input = self.input;
        window.input = input;
    };
    UploadField.prototype.on_fail = function on_fail(event, data){
        var self = this;
        console.log("Fail: ", event, data);
    };
    UploadField.prototype.on_add = function on_add(event, data){
        var self = this;
        var reader;
        data.context = j("<p>").text("Uploading ... ");
        self.node.parent().append(data.context);
        if (j("img", self.node).length) {
            self.current_image = j("img", self.node);
        } else {
            self.current_image = j("<img>").addClass("obj");
            self.preview_container.append(self.current_image);
        }
        self.current_image.get(0).file = data.files[0];
        reader = new FileReader();
        reader.onload = function(event) {
            self.current_image.get(0).src = event.target.result;
        };
        reader.readAsDataURL(data.files[0]);
        data.submit();
    };
    UploadField.prototype.on_progress = function on_progress(event, data){
        var self = this;
        _$rapyd$_print("Upload in progress");
    };
    UploadField.prototype.on_done = function on_done(event, data){
        var self = this;
        var url, file;
        console.log(event, data);
        url = "http://" + window.location.host + data.result.files[0].url;
        console.log("Setting val to ", data.result.files[0].id);
        j("input[type='hidden']", self.node).val(data.result.files[0].id);
        var _$rapyd$_Iter7 = data.result.files;
        for (var _$rapyd$_Index7 = 0; _$rapyd$_Index7 < _$rapyd$_Iter7.length; _$rapyd$_Index7++) {
            file = _$rapyd$_Iter7[_$rapyd$_Index7];
            j("<p/>").text(file.name).appendTo(j("body"));
        }
    };

    function init_gridfields() {
        var gridfields, field;
        gridfields = [];
        var _$rapyd$_Iter8 = j(".gridfield");
        for (var _$rapyd$_Index8 = 0; _$rapyd$_Index8 < _$rapyd$_Iter8.length; _$rapyd$_Index8++) {
            field = _$rapyd$_Iter8[_$rapyd$_Index8];
            gridfields.push(new GridField(j(field)));
        }
    }
    function init_uploader() {
        var uploaders, u;
        uploaders = [];
        var _$rapyd$_Iter9 = j(".async-upload-container");
        for (var _$rapyd$_Index9 = 0; _$rapyd$_Index9 < _$rapyd$_Iter9.length; _$rapyd$_Index9++) {
            u = _$rapyd$_Iter9[_$rapyd$_Index9];
            uploaders.push(new UploadField(j(u)));
        }
    }
    function on_ready() {
        var notifications, el;
        j(document).trigger("silverflask:panel_ready");
        init_gridfields();
        init_uploader();
        notifications = [];
        var _$rapyd$_Iter10 = j(".alert");
        for (var _$rapyd$_Index10 = 0; _$rapyd$_Index10 < _$rapyd$_Iter10.length; _$rapyd$_Index10++) {
            el = _$rapyd$_Iter10[_$rapyd$_Index10];
            notifications.push(Notification.init_from_node(j(el)));
        }
    }
    j(document).on("ready", on_ready);
})();