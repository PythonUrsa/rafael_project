app.controller('UserProfileCtrl', function($scope, $state, $stateParams, $http, FEUserService, PhotoService, NavigationService, usSpinnerService, SettingService){

	$('body').addClass("user");
	$('body').removeClass("home");
	$('body').removeClass("search");

	FEUserService.get({id:NavigationService.getIdentity().id}, function(user){
		$scope.user = user;
		$scope.user.date_joined = new Date($scope.user.date_joined).toString("dd , MMMM , yyyy");
		$scope.user.date_joined = $scope.user.date_joined.replace(',', 'de');
		$scope.user.date_joined = $scope.user.date_joined.replace(',', 'del');

	})

	$scope.editProfile = function(){
		$state.go("profileEdit");
	};

	$scope.goAddr = function(){
		$state.go("userAddresses")
	};

	$scope.goToOrders = function() {
		$state.go("userOrders")
	};

});