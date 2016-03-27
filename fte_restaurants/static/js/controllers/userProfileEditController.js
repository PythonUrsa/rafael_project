app.controller('UserProfileEditCtrl', function($scope, $state, $stateParams, $http, $modal, FEUserService,
	UpdateUser, PhotoService, NavigationService, usSpinnerService, SettingService, changePassModal){

	$('body').addClass("user");
	$('body').removeClass("search");
	$('body').removeClass("home");

	FEUserService.get({id:NavigationService.getIdentity().id}, function(user){
		$scope.user = user;
	})
	
	$scope.error = false
  	$scope.error_text = ''
  	$scope.updating = false;
  	$scope.profile_picture = '';

	$scope.today = function() {
		$scope.dt = new Date();
	};
	$scope.today();

	$scope.clear = function () {
		$scope.dt = null;
	};

	$scope.open = function($event) {
		$event.preventDefault();
		$event.stopPropagation();

		$scope.opened = true;
	};

	$scope.dateOptions = {
		formatYear: 'yyyy',
		startingDay: 0
	};
	$scope.format = 'dd/MM/yyyy';

	$scope.updateProfile = function(){
		$scope.updating = true;
		var url = '/api/v1/auth/user/' + NavigationService.getIdentity().id + '/';
		if($scope.user.date_of_birth != undefined && typeof($scope.user.date_of_birth) != 'string'){
			var date = $scope.user.date_of_birth;
			var month = date.getMonth() + 1;
			formatted_date = date.getFullYear() + '-' + month + '-' + date.getDate();
		} else {
			formatted_date = $scope.user.date_of_birth;
		}
		var updatedUser = {
			first_name: $scope.user.first_name,
			last_name: $scope.user.last_name,
			telephone: $scope.user.telephone,
			email: $scope.user.email,
			gender: $scope.user.gender,
			date_of_birth: formatted_date,
			// photo: $scope.dataMedia
		}
		$http.patch(url, updatedUser).success(function(returnedUser){
			if (returnedUser.error) {
				$scope.updating = false;
				$scope.error = true;
				$scope.error_text = returnedUser.error.message;
			} else {
				$state.go("profile", {"user": returnedUser.id})
				if ($scope.profile_picture) {
					UpdateUser.updateFTEUser(returnedUser, $scope.profile_picture.file, function(returnedUser){
					})
				};
			};
		}).error(function(data){
			$scope.updating = false;
			$scope.error = true;
          	$scope.error_text = "Error al actualizar los datos";
		});
	};

	$scope.openPass = function(){
		changePassModal($scope);
	};

	$scope.open_rnc = function() {
		 var modalInstance = $modal.open({
	      templateUrl: '/static/partials/modal_edit_rnc.html',
	      controller: 'ModalRNCController',
	      resolve: {
	      	user: function(){
	      			return $scope.user
	      	},
	      }
	    });

    modalInstance.result.then(function () {
     	// Pass
      });
    }

    $scope.confirmEmail = function(){
    	var confirmation_url = '/user/api/send_confirmation_key/'
    	$http.post(confirmation_url, $scope.user).success(function(returnedData){
    		// pass
    	}).error(function(data){
    		// pass
    	});
    }

	$scope.goAddr = function(){
		$state.go("userAddresses")
	};

	$scope.goToProfile = function(){
		$state.go("profile");
	}

	$scope.goToOrders = function() {
		$state.go("userOrders")
	};

});