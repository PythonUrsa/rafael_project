appRestaurant.controller('RestaurantLoginCtrl', function($scope,$filter, $state, urls, RestaurantNavigationService){
	
  $('body').addClass("user");
  $('body').addClass("user-admin");
  $('body').addClass("login");
	
	$scope.credentials ={
		'email':'',
		'password':'',
	};

  $scope.password_reset = urls.password_reset;

	$scope.ok = function() {
        RestaurantNavigationService.authenticate($scope.credentials).then(
        	function (user) {
      			$state.go("restaurant", {});
    		},
    		function(result){ 
          // pass
    		});
  };
});