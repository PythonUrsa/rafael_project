app.controller('BaseCtrl', function($scope, $state, CityService, ZoneService, NavigationService, usSpinnerService, SettingService, loginModal){

	$scope.open = function () {
		loginModal();
	};

	$scope.showSearch = function(){
		switch($state.current.name){
			case "home":
				return false;
				break;
			case "search":
				return false;
				break
			default:
				return true;
		}
	}

	$scope.isAuthenticated = function() {
		if (NavigationService.isAuthenticated()) {
			var userIdentity = NavigationService.getIdentity();
			$scope.authenticatedUser = userIdentity;
		};
		return NavigationService.isAuthenticated();
	};

	$scope.search = function(){
		$scope.params = {
			'zones': '',
			'city': '',
			'preference': '',
		}
		$scope.zone = '';
		NavigationService.setZoneName($scope.params.zones);
		$scope.params.preference = $scope.searchParam;
		$scope.searchParam = "";
		NavigationService.setHomeForm($scope.params);
		$state.go("search", $scope.params);
	};

	$scope.goToProfile = function(){
		$state.go("profile")
	}

	$scope.goHome = function(){
		$state.go("home");
	}
	$scope.logout = function(){
		NavigationService.logout();
		NavigationService.setUserOrder([]);
		NavigationService.setAddress([]);
		$scope.isAuthenticated()
		if($state.current.authenicate == true){
			$state.go("home")
		}
	}
});


