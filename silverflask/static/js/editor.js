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
    var str, j, defaultContent;
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
    j = jQuery;
    defaultContent = [ {
        "component": "hero",
        "content": {
            "title": "History Is Water Under The Bridge"
        }
    }, {
        "component": "p",
        "content": {
            "text": "On February 1, 2008, Toshio Suzuki stepped down from the position of Studio Ghibli president, which he had held since 2005, and Koji Hoshino (former president of Walt Disney Japan) took over. Suzuki said he wanted to improve films with his own hands as a producer, rather than demanding this from his employees. Suzuki decided to hand over the presidency to Hoshino because Hoshino has helped Studio Ghibli to sell its videos since 1996, also helping to release the Princess Mononoke film in the United States. Suzuki still serves on the company’s board of directors."
        }
    }, {
        "component": "main-and-sidebar",
        "containers": {
            "main": [ {
                "component": "h2",
                "content": {
                    "title": "Understanding The Present Means Understanding Titles"
                }
            }, {
                "component": "p",
                "content": {
                    "text": "Studio Ghibli has produced nineteen feature films, several short films, television commercials, and a television film. Eight of Studio Ghibli’s films are among the 15 highest-grossing anime films made in Japan, with Spirited Away being the highest, grossing over $274 million worldwide."
                }
            }, {
                "component": "panel"
            } ],
            "sidebar": [ {
                "component": "quote"
            }, {
                "component": "list-group",
                "containers": {
                    "list": [ {
                        "component": "list-group-item"
                    }, {
                        "component": "list-group-box-item"
                    } ]
                }
            } ]
        }
    } ];
    function LivingDocsPropertyPanel() {
        LivingDocsPropertyPanel.prototype.__init__.apply(this, arguments);
    }
    LivingDocsPropertyPanel.prototype.__init__ = function __init__(node, editor){
        var self = this;
        self.node = node;
        self.editor = editor;
        self.livingdoc = editor.livingdoc;
    };
    LivingDocsPropertyPanel.prototype.set_active_component = function set_active_component(component){
        var self = this;
        self.active_component = component;
        self.update_panel();
    };
    LivingDocsPropertyPanel.prototype.on_property_change = function on_property_change(style, event){
        var self = this;
        self.active_component.setStyle(style.name, event.target.value);
    };
    LivingDocsPropertyPanel.prototype.update_panel = function update_panel(){
        var self = this;
        var callback, option, el, _$rapyd$_Unpack, style_name, style;
        self.node.empty();
        if (self.active_component.template.styles.length) {
            self.node.append(j("<h5>").text("Properties"));
        }
        var _$rapyd$_Iter6 = dict.items(self.active_component.template.styles);
        for (var _$rapyd$_Index6 = 0; _$rapyd$_Index6 < _$rapyd$_Iter6.length; _$rapyd$_Index6++) {
            _$rapyd$_Unpack = _$rapyd$_Iter6[_$rapyd$_Index6];
            style_name = _$rapyd$_Unpack[0];
            style = _$rapyd$_Unpack[1];
            callback = j.proxy(self.on_property_change, self, style);
            if (style.type === "select") {
                el = j("<select>");
                var _$rapyd$_Iter7 = style.options;
                for (var _$rapyd$_Index7 = 0; _$rapyd$_Index7 < _$rapyd$_Iter7.length; _$rapyd$_Index7++) {
                    option = _$rapyd$_Iter7[_$rapyd$_Index7];
                    el.append(j("<option>").val(option.value).text(option.caption));
                }
                el.on("change", callback);
            } else if (style.type === "option") {
                el = j("<input>").attr({type: checkbox});
                el.on("change", callback);
            }
            self.node.append(el);
        }
    };

    function LivingDocsImageUploader() {
        LivingDocsImageUploader.prototype.__init__.apply(this, arguments);
    }
    LivingDocsImageUploader.prototype.__init__ = function __init__(snippet, snippet_view, directive){
        var self = this;
        var on_progress, on_add, on_done;
        self.snippet = snippet;
        self.snippet_view = snippet_view;
        self.directive = directive;
        self.input_field = j("<input>", {
            "id": "fileupload",
            "class": "hidden",
            "name": "file",
            "type": "file"
        });
        on_progress = j.proxy(self.on_progress, self);
        on_add = j.proxy(self.on_add, self);
        on_done = j.proxy(self.on_done, self);
        self.input_field.fileupload({
            "dataType": "json",
            "url": "/admin/upload",
            "dropZone": self.snippet_view.$elem,
            "progressall": on_progress,
            "add": on_add,
            "done": on_done
        });
    };
    LivingDocsImageUploader.prototype.on_add = function on_add(event, data){
        var self = this;
        var img, reader;
        self.snippet_view.$elem.innerHTML = "Uploading";
        img = document.createElement("img");
        img.file = data.files[0];
        img.classList.add("obj");
        self.add_progress_bar();
        reader = new FileReader();
        reader.onload = function(event) {
            self.snippet.directives.get("image").setBase64Image(event.target.result);
        };
        reader.readAsDataURL(data.files[0]);
        data.submit();
    };
    LivingDocsImageUploader.prototype.on_progress = function on_progress(){
        var self = this;
    };
    LivingDocsImageUploader.prototype.on_done = function on_done(event, data){
        var self = this;
        var url;
        url = "http://" + window.location.host + data.result.files[0].url;
        console.log(self.snippet, self.snippet_view);
        console.log(self.snippet.directives.get("image"));
        self.snippet.directives.get("image").setContent(url);
        window.snippet = self.snippet;
        self.progress_bar_remove();
    };
    LivingDocsImageUploader.prototype.progress_bar_update = function progress_bar_update(val){
        var self = this;
        self.progress_bar_element.css("width", val + "%");
    };
    LivingDocsImageUploader.prototype.progress_bar_remove = function progress_bar_remove(){
        var self = this;
        self.progress_bar_container.remove();
    };
    LivingDocsImageUploader.prototype.add_progress_bar = function add_progress_bar(){
        var self = this;
        self.progress_bar_container = j("<div>");
    };

    function LivingDocsBlockPanel() {
        LivingDocsBlockPanel.prototype.__init__.apply(this, arguments);
    }
    LivingDocsBlockPanel.prototype.__init__ = function __init__(node, editor){
        var self = this;
        self.node = node;
        self.livingdoc = editor.livingdoc;
        self.editor = editor;
        self.render();
    };
    LivingDocsBlockPanel.prototype.render = function render(){
        var self = this;
        var callback, el, template;
        var _$rapyd$_Iter8 = self.livingdoc.design.components;
        for (var _$rapyd$_Index8 = 0; _$rapyd$_Index8 < _$rapyd$_Iter8.length; _$rapyd$_Index8++) {
            template = _$rapyd$_Iter8[_$rapyd$_Index8];
            callback = j.proxy(self.on_drag, self, template.name);
            el = j("<div class=\"toolbar-entry\">");
            el.html(template.label);
            self.node.append(el);
            el.on("mousedown", callback);
        }
    };
    LivingDocsBlockPanel.prototype.on_drag = function on_drag(component, event){
        var self = this;
        var new_component;
        new_component = self.livingdoc.createComponent(component);
        doc.startDrag({
            "componentModel": new_component,
            "event": event,
            "config": {
                "preventDefault": true,
                "direct": true
            }
        });
    };

    function LivingDocsEditor() {
        LivingDocsEditor.prototype.__init__.apply(this, arguments);
    }
    LivingDocsEditor.prototype.__init__ = function __init__(node, design_name){
        var self = this;
        if (typeof design_name === "undefined") design_name = "boilerplate";
        var callback;
        self.field_name = node.data("name");
        self.selector_json_field = self.field_name + "_json";
        self.selector_html_field = self.field_name;
        self.selector_editor_node = ".livingdocs-editor";
        self.node = node;
        self.design = design_name;
        doc.design.load(design[self.design]);
        self.json_field = j("input[name=" + self.selector_json_field + "]").first();
        self.html_field = j("textarea[name=" + self.selector_html_field + "]").first();
        self.editor_node = j(self.selector_editor_node, node);
        self.load_content();
        self.init_renderer();
        self.property_panel = new LivingDocsPropertyPanel(j(".doc-block-properties", self.node), self);
        self.blocks_panel = new LivingDocsBlockPanel(j(".doc-blocks", self.node), self);
        callback = j.proxy(self.on_submit, self);
        self.node.parents("form").on("submit", callback);
    };
    LivingDocsEditor.prototype.on_view_ready = function on_view_ready(renderer){
        var self = this;
        var on_text_select, on_component_focus, on_snippet_added, view, snippet;
        on_text_select = j.proxy(self.on_text_select, self);
        on_component_focus = j.proxy(self.on_component_focus, self);
        on_snippet_added = j.proxy(self.on_snippet_added, self);
        self.livingdoc.interactiveView.page.editableController.selection.add(on_text_select);
        self.livingdoc.interactiveView.page.focus.componentFocus.add(on_component_focus);
        self.livingdoc.componentTree.componentAdded.add(on_snippet_added);
        var _$rapyd$_Iter9 = self.livingdoc.componentTree.find("image");
        for (var _$rapyd$_Index9 = 0; _$rapyd$_Index9 < _$rapyd$_Iter9.length; _$rapyd$_Index9++) {
            snippet = _$rapyd$_Iter9[_$rapyd$_Index9];
            self.livingdoc.interactiveView.renderer.insertComponent(snippet);
            view = self.livingdoc.interactiveView.renderer.componentViews[snippet.id];
            view.uploader = new LivingDocsImageUploader(snippet, view);
        }
    };
    LivingDocsEditor.prototype.on_snippet_added = function on_snippet_added(snippet_model){
        var self = this;
        var view;
        if (snippet_model.directives.image) {
            self.livingdoc.interactiveView.renderer.insertComponent(snippet_model);
            view = snippet_model.getMainView();
            view.uploader = new LivingDocsImageUploader(snippet_model, view);
        }
        return true;
    };
    LivingDocsEditor.prototype.on_submit = function on_submit(event){
        var self = this;
        self.json_field.val(self.livingdoc.toJson());
        self.html_field.val(self.livingdoc.toHtml());
    };
    LivingDocsEditor.prototype.on_text_select = function on_text_select(event){
        var self = this;
        console.log(event);
        return null;
    };
    LivingDocsEditor.prototype.on_component_focus = function on_component_focus(event){
        var self = this;
        self.property_panel.set_active_component(event.model);
        return null;
    };
    LivingDocsEditor.prototype.init_renderer = function init_renderer(){
        var self = this;
        var ready, on_view_ready;
        ready = self.livingdoc.createView({interactive: true, iframe: true, host: ".editor-section"});
        on_view_ready = j.proxy(self.on_view_ready, self);
        ready.then(on_view_ready);
    };
    LivingDocsEditor.prototype.load_content = function load_content(){
        var self = this;
        var json, parsed_json;
        json = self.json_field.val();
        try {
            parsed_json = JSON.parse(json);
            self.livingdoc = doc.new({data: parsed_json});
        } catch (_$rapyd$_Exception) {
            self.livingdoc = doc.new({
                "data": {
                    "content": defaultContent,
                    "design": {
                        "name": "boilerplate",
                        "version": "0.3.0"
                    }
                }
            });
        }
    };

    function init_editors() {
        var editors, e;
        editors = [];
        doc.config({
            "livingdocsCssFile": "/static/js/bower_components/livingdocs-engine/dist/css/livingdocs.css"
        });
        var _$rapyd$_Iter10 = j(".livingdocs-editor-wrapper");
        for (var _$rapyd$_Index10 = 0; _$rapyd$_Index10 < _$rapyd$_Iter10.length; _$rapyd$_Index10++) {
            e = _$rapyd$_Iter10[_$rapyd$_Index10];
            editors.push(new LivingDocsEditor(j(e)));
        }
    }
    j(document).ready(init_editors);
})();