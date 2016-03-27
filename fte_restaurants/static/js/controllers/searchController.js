app.controller('SearchController', function($scope, $state,$stateParams,RestaurantService, CityService, ZoneService, FoodTypeService, NavigationService){
	
	$('body').addClass("search");
	$('body').removeClass("home");
	$('body').removeClass("user");

	(function(){
		NavigationService.setHomeForm($stateParams)
	})()

	$scope.zone = ZoneService.get({id:$stateParams['zones']}, function(zone){
	})

	$scope.new_search = ""


	$scope.restaurants = RestaurantService.query(angular.extend({},NavigationService.getHomeForm(), {order_by: 'name', limit: '5'}), function(){
		// pass		
	})

	$scope.foodTypes = FoodTypeService.get({}, function(){
	})

	$scope.goToDetail = function(id){
		$state.go("detail", {"restaurant": id})
	}


	$scope.doSearch = function(){
		var homeForm = NavigationService.getHomeForm();
		homeForm.preference = $scope.filter.foodType;
		homeForm.ord_min = $scope.filter.ord_min;
		homeForm.est_time = $scope.filter.est_time;
		NavigationService.setHomeForm(homeForm);
		$scope.restaurants = RestaurantService.query(angular.extend({},NavigationService.getHomeForm(), {order_by: 'name', limit: '5'}), function(){
			// pass
		})
	}

	$scope.clean = function(){
		$scope.filter.foodType = '';
		$scope.filter.ord_min = '';
		$scope.filter.est_time = '';
	};

});