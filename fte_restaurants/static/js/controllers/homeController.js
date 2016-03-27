app.controller('HomeController', function($scope,$filter, $state, RestaurantService, CityService, ZoneService, PhotoService ,NavigationService, usSpinnerService, SettingService){
	
	$('body').addClass("home");
	$('body').removeClass("search");
	$('body').removeClass("user");
	
	$scope.search = {
		'zones': '',
		'city': '',
		'preference': '',
	}

	$scope.zones = ZoneService.query(function(){
		// pass
	});

	$scope.cities = CityService.query(function(){
		$scope.main_city = SettingService.get({key: 'MAIN_CITY'}, function(){
			$scope.search.city = parseInt($scope.main_city.objects[0].value);
			$scope.featured_city = $filter('getById')($scope.cities.objects, $scope.main_city.objects[0].value)
			usSpinnerService.spin('spinner-1');
			$scope.restaurants = RestaurantService.query({city: $scope.main_city.objects[0].value, featured: 'True', order_by: 'name', limit: '12'}, function(){
				usSpinnerService.stop('spinner-1');
			})
		})
	})

	$scope.featured_city = "Santo Domingo"
	$scope.home_photos = []
	$scope.myInterval = 3000;

	PhotoService.query({}, function(photos){
		$scope.home_photos = photos.objects
	})


	$scope.filter_restaurants = function(){		
		if($scope.home_search_form.$valid){
			NavigationService.setHomeForm($scope.search)
			$state.go("search", $scope.search)

		}else{
			$scope.error = true;
			$scope.error_title = "Missing fields";
			$scope.error_content = "There are missing fields. Please check."
		}	
	}


	$scope.goToDetail = function(id){
		$state.go("detail", {"restaurant": id})
	}
	
	
	$scope.$watch('search.city', function (newValue, oldValue) {
 	    if (newValue == oldValue) { return;}
 	    	usSpinnerService.spin('spinner-1');
 	    	if(newValue == "" || newValue == null){
 	    		$scope.restaurants = RestaurantService.query({city: $scope.main_city.objects[0].value ,featured: 'True', order_by: 'name', limit: '12'}, function(){
					$scope.featured_city = $filter('getById')($scope.cities.objects, $scope.main_city.objects[0].value)
					usSpinnerService.stop('spinner-1');
				})
 	    	}else{
     	    	$scope.restaurants = RestaurantService.query({city: newValue ,featured: 'True', order_by: 'name', limit: '12'}, function(){
					$scope.featured_city = $filter('getById')($scope.cities.objects, newValue)
					usSpinnerService.stop('spinner-1');
				})
				$scope.zones = ZoneService.query({city: newValue});
 	    	}
        	
    },true);


});