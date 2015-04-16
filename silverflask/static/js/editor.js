(function(){
    function _$rapyd$_extends(child, parent) {
        child.prototype = new parent;
        child.prototype.constructor = child;
    }
    var j, defaultContent;
    j = jQuery;
    function StateMachine() {
    }
    StateMachine.prototype.changeState = function changeState(state, snippet){
        var self = this;
        if (typeof snippet === "undefined") snippet = null;
        self.current_state = state;
        if (snippet) {
            self.current_snippet = snippet;
        }
    };
    StateMachine.prototype.register_controller = function register_controller(controller){
        var self = this;
        self.controller_scopes.push(controller);
    };
    StateMachine.prototype.get_current_state = function get_current_state(){
        var self = this;
        return self.current_state;
    };

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
    function Editor() {
        Editor.prototype.__init__.apply(this, arguments);
    }
    Editor.prototype.__init__ = function __init__(node, design_name){
        var self = this;
        if (typeof design_name === "undefined") design_name = "boilerplate";
        self.selector_json_field = ".livingdocs-raw";
        self.selector_html_field = ".livingdocs-field";
        self.selector_editor_node = ".livingdocs-editor";
        self.node = node;
        self.design = design_name;
        doc.design.load(design[self.design]);
        self.json_field = j(self.selector_json_field, node);
        self.html_field = j(self.selector_html_field, node);
        self.editor_node = j(self.selector_editor_node, node);
        self.load_content();
        self.init_renderer();
    };
    Editor.prototype.on_view_ready = function on_view_ready(view){
        var self = this;
        var on_text_select, on_component_focus;
        on_text_select = j.proxy(self.on_text_select, self);
        on_component_focus = j.proxy(self.on_component_focus, self);
        self.livingdoc.interactiveView.page.editableController.selection.add(on_text_select);
        self.livingdoc.interactiveView.page.focus.componentFocus.add(on_component_focus);
    };
    Editor.prototype.on_text_select = function on_text_select(event){
        var self = this;
        console.log(event);
        return null;
    };
    Editor.prototype.on_component_focus = function on_component_focus(event){
        var self = this;
        console.log(event);
        return null;
    };
    Editor.prototype.init_renderer = function init_renderer(){
        var self = this;
        var on_view_ready, ready;
        on_view_ready = j.proxy(self.on_view_ready, self);
        ready = self.livingdoc.createView({interactive: true, iframe: true, host: ".editor-section"});
        ready.then(on_view_ready);
    };
    Editor.prototype.load_content = function load_content(){
        var self = this;
        var json, parsed_json;
        json = j(self.selector_json_field, self.node).first().val();
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
            self.add_default_content();
        }
    };
    Editor.prototype.add_default_content = function add_default_content(){
        var self = this;
        return null;
    };

    function init_editors() {
        var editors, e;
        editors = [];
        var _$rapyd$_Iter0 = j(".livingdocs-editor-wrapper");
        for (var _$rapyd$_Index0 = 0; _$rapyd$_Index0 < _$rapyd$_Iter0.length; _$rapyd$_Index0++) {
            e = _$rapyd$_Iter0[_$rapyd$_Index0];
            editors.push(new Editor(j(e)));
        }
    }
    j(document).ready(init_editors);
})();