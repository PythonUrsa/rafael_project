appRestaurant.controller('NewSectionCtrl', function($scope, $state, $stateParams, $modal, $modalInstance,
	usSpinnerService, SettingService, CategoryService, restaurant, selected){

	$scope.init = function() {
		$scope.restaurant = restaurant;
		if (selected) {
			$scope.section = selected;
		};
	}
    
  	$scope.init()

	$scope.cancel = function () {
    	$modalInstance.dismiss('cancel');
  	};

  	$scope.ok = function () {
  		// If it's a new category, we create it
  		if($scope.section.id == undefined){
	  		var new_section = new CategoryService($scope.section)
			new_section.restaurant = restaurant.resource_uri
			new_section.$save(function(data,headers) {
				$modalInstance.close(data, false);
			}, function (error) {
				// pass
			});
  		// Otherwise we update it
  		} else {
  			CategoryService.update({id: $scope.section.id}, $scope.section, function(data, headers){
		  		$modalInstance.close(data, false);
			}, function (error){
				// pass
			});
  		};
  	};

});