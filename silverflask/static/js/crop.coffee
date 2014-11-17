silverflask_angular.controller "imageCropController", ($scope, EditorState) ->
  $scope.myImage = '/static/uploads/IMG_0297.JPG'
  $scope.myCroppedImage = ''
  $scope.$on "editorStateChanged", () ->
    if EditorState.currentState == 'crop'

      $scope.myImage = EditorState.currentSnippet.model.get('image')
      $("#cropModal").modal('show')

  $scope.$watch 'myCroppedImage', () ->
    if EditorState.currentState = 'crop'
      EditorState.currentSnippet?.model.directives.get("image").setBase64Image($scope.myCroppedImage)

  EditorState.registerController($scope)
