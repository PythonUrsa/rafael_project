app.controller('CambiarClaveModalCtrl', function($scope, $state, $modalInstance, $http, NavigationService) {

    $scope.cancel = $scope.$dismiss;
    $scope.submit_error = '';

    $scope.credentials ={
        'email': NavigationService.getIdentity().email,
        'password':'',
    };


    $scope.dismiss = function(){
        $modalInstance.dismiss('cancel');
    };

    $scope.ok = function() {
        NavigationService.checkPassword($scope.credentials).then(
            function (user) {
                if ($scope.newPassword == $scope.confirmation){
                    var updatedPassword = {
                        password: $scope.newPassword,
                    }
                    var url = "/api/v1/auth/user/" + NavigationService.getIdentity().id + "/";
                    $http.patch(url, updatedPassword).success(function(returnedUser){
                        if (returnedUser.error){
                            $scope.submit_error = returnedUser.error.message;
                        } else {
                            $scope.$close(user);
                        }
                    }).error(function(data){
                        alert("ERROR: " + JSON.stringify(data));
                    });
                } else {
                    $scope.submit_error = 'La contraseña y la confirmación no coinciden.';
                }
            },
		function(result){
		});
  };

});