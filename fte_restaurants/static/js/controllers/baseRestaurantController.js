appRestaurant.controller('BaseRestaurantCtrl', function($scope, $state, RestaurantNavigationService ){

	$scope.isAuthenticated = function() {
		if (RestaurantNavigationService.isAuthenticated()) {
			var userIdentity = RestaurantNavigationService.getIdentity();
			$scope.authenticatedUser = userIdentity;
		};
		return RestaurantNavigationService.isAuthenticated();
	};

	$scope.logout = function(){
		RestaurantNavigationService.logout()
		$scope.isAuthenticated()
		if($state.current.authenicate == true){
			$state.go("home")
		}
	}
});