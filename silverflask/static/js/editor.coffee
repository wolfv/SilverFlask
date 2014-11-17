class StateMachine
  currentState: ["nostate"]
  currentSnippet: null
  controllerScopes: []
  changeState: (state, snippet=null) ->
    @.currentState = state
    if snippet
      @.currentSnippet = snippet
    for c in @.controllerScopes
      c.$emit("editorStateChanged")
  registerController: (controller) ->
    @.controllerScopes.push(controller)
  getCurrentState: ->
    return @.currentState

silverflask_angular.factory('EditorState', ($rootScope) ->
    window.statemachine = new StateMachine()
    return window.statemachine
)

class Uploader

  addProgressBar: () ->
    @.progressBarContainer = $("<div>").addClass("progress").css("width", @.snippetView.$elem.width())
    @.progressBarElement = $("<div>").addClass("progress-bar").css("width", "60%")
    @.progressBarContainer.append(@.progel)
    $(@.snippetView.$elem).append(@.progressBarContainer)

  progressBarUpdate: (val) ->
    @.progressBarElement.css("width", val + "%")

  progressBarRemove: () ->
    @.progressBarContainer.remove()

  constructor: (snippet, snippetView) ->
    @.snippetView = snippetView
    inputField = $ "<input>", {
      'id': '#fileupload',
      'class': 'hidden',
      'name': "file",
      'type': 'file'
    }
    self = @
    inputField.fileupload
      dataType: 'json',
      url: '/admin/upload',
      dropZone: snippetView.$elem,

      progressall: (e, data) ->
        progress = parseInt(data.loaded / data.total * 100, 10);
        self.progressBarUpdate(progress)

      add: (e, data) ->
        snippetView.$elem.innerHTML = "Uploading"
        img = document.createElement("img")
        img.file = data.files[0]
        img.classList.add("obj");

        self.addProgressBar()

        reader = new FileReader
        reader.onload =  (e) ->
          snippet.directives.get("image").setBase64Image(e.target.result)

        reader.readAsDataURL(data.files[0])
        data.submit()

      done: (e, data) ->
        url = "http://" + window.location.host + data.result.files[0].url
        snippet.setContent('image', {url: url})
        self.progressBarRemove()


editorController = silverflask_angular.controller("EditorController", ($scope, $element, EditorState) ->

    addDefaultContent = (lvd) ->
      lvd.model.append('mainAndSidebar')
      snippet = lvd.model.createSnippet('hero')
      lvd.model.first().append('main', snippet)
      text = lvd.model.createSnippet('text')
      snippet.after(text)

    $scope.$on("editorStateChanged", ->
      console.log("State Changed, fantastic!", EditorState.currentSnippet)
    )

    doc.design.load(design.bootstrap);

    editorElement = $element.children(".editor-section").first()

    # find json
    jsonField = $("#" + editorElement.data("for") + "_json")
    jsonValue = jsonField.val()

    # add living docs editor
    try
      jsonParsed = JSON.parse(jsonValue)
      lvd = doc.new
        data: jsonParsed,
        design: 'bootstrap'
    catch
      lvd = doc.new
        design: 'bootstrap'
      addDefaultContent(lvd)

    lvd.for_id = editorElement.data("for")
    window.livingdocs_elements.push(lvd)

    renderer = null
    viewReady = lvd.createView editorElement[0], {interactive: true}
    viewReady.done (returnValue) ->
      returnValue.renderer.readySemaphore.callbacks.push (cb) ->
        snippetViews = returnValue.renderer.snippetViews
        snippetTree = returnValue.renderer.snippetTree
        snippetTree.find("image").each (snippet) ->
          view = snippetViews[snippet.id]
          view.uploader = new Uploader(snippet, view)
      renderer = returnValue.renderer
      lvd.interactiveView.page.focus.snippetFocus.add (snippet) ->
        EditorState.changeState('selected', snippet)

      viewBody = lvd.interactiveView.page.$body

      lvd.interactiveView.page.imageClick.add () ->
        console.log("an image was clicked!")


      lvd.interactiveView.snippetTree.snippetAdded.add (snippetModel) ->
        if snippetModel.directives.image
          view = renderer.snippetViewForSnippet(snippetModel)
          view.uploader = new Uploader(snippetModel, view)

      lvd.interactiveView.snippetTree.snippetHtmlChanged.add (snippet) ->
        console.log("After change", snippet)

      lvd.interactiveView.page.htmlElementClick.add () ->
        console.log("HTML ELEMENT Clicked")

    $scope.lvd = lvd
    EditorState.registerController($scope)
    return null
)

class FormBuilder
  build: (snippet, snippetTemplate) ->
    styles = snippetTemplate.styles
    console.log(@.parentElement)
    $(".lvd-form").empty()
    for prop of styles
      switch styles[prop].type
        when 'select'
          el = $("<select>").addClass("form-element")
          for val in styles[prop].options
            el.append($("<option>").text(val.caption).val(val.value))
          el.change (e) ->
            v = el.val()
            console.log(styles[prop], "changed!")
            snippet.model.setStyle(prop, v)


      $(".lvd-form").append(el)
    if snippet.directives.image
      btn = $("<button>").addClass("btn").text("Crop Image")
      $(".lvd-form").append(btn)
      btn.click () ->
        statemachine.changeState("crop")

silverflask_angular.controller("EditPane", ($scope, $element, EditorState) ->
  $scope.elementSelected = false
  formbuilder = new FormBuilder()
  $scope.$on "editorStateChanged", () ->
    $scope.elementSelected = true
    currentSnippet = EditorState.currentSnippet
    formbuilder.build(currentSnippet, currentSnippet.model.template)
    $scope.$apply()

  $scope.design = $scope.$parent.lvd.design
  $scope.templates = $scope.design.templates
  $scope.newSnippetMousedownHandler = (id) ->
    newSnippet = $scope.$parent.lvd.model.createModel(id);
    doc.startDrag
      snippetModel: newSnippet,
      event: event,
      config: {
        preventDefault: true,
        direct: true
      }


  $scope.deleteSnippet = ->
    EditorState.currentSnippet.model.remove()
    $scope.elementSelected = false
    $scope.$apply()


  EditorState.registerController($scope)
)