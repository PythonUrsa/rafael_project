app.controller('LoginModalCtrl', function($scope, $state, $modalInstance, urls, NavigationService, AddressUserService) {

  $scope.cancel = $scope.$dismiss;
  
  
  $scope.credentials ={
        'email':'',
        'password':'',
  };

  $scope.password_reset = urls.password_reset;

  $scope.dismiss = function(){
    $modalInstance.dismiss('cancel');
  };
  
  $scope.ok = function() {
        NavigationService.authenticate($scope.credentials).then(
        	function (user) {
            AddressUserService.get({frontend_user:NavigationService.getIdentity().id, main: true}, function(addresses){
              NavigationService.setAddress(addresses.objects[0]);
            })
      			$scope.$close(user);
    		},
    		function(result){
          $scope.login_form.failed = true;
    		});
  };

  $scope.goToRegister = function(){
    $state.go("register", {})
    $modalInstance.dismiss('cancel');
  }

});