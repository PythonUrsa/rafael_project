appRestaurant.controller('NewExtraCtrl', function($scope, $state, $stateParams, $modal, $modalInstance,
	usSpinnerService, RestaurantNavigationService, SettingService, ExtraTypeService, ExtraService,
	selected){

	$scope.addOption = function () {
		var extra = {
			name: "",
			price: ""
		};
		$scope.extras.push(extra);
	};

	$scope.init = function () {
		$scope.deleted = [];
		if (!selected){
			$scope.extras = [];
			$scope.addOption();
		} else {
			$scope.extra_type = selected;
			ExtraService.query({extra_type:selected.id}, function(extras){
				$scope.extras = extras.objects;
			})
		}
	};

	$scope.init();

	$scope.delOption = function (index) {
		if ($scope.extras[index].id == undefined) {
			$scope.extras.splice(index,1);
		} else {
			$scope.deleted.push($scope.extras[index])
			$scope.extras.splice(index,1);
		};
	};


	$scope.cancel = function () {
    	$modalInstance.dismiss('cancel');
  	};

  	$scope.ok = function () {
  		$scope.restaurant = RestaurantNavigationService.getRestaurant();
  		// If it's a new ExtraType we create it
		if ($scope.extra_type.id == undefined) {
	  		var extra_type = {
	  			restaurant: $scope.restaurant.resource_uri,
	  			name: $scope.extra_type.name
	  		};
	  		var new_extra_type = new ExtraTypeService(extra_type);

			new_extra_type.$save(function(data,headers) {
				for (var i = 0; i < $scope.extras.length; i++) {
					$scope.extras[i].extra_type = data.resource_uri;
					if ($scope.extras[i].price == ''){
						$scope.extras[i].price = 0;
					}
					var new_extra_option = new ExtraService($scope.extras[i]);
					new_extra_option.$save(function(data, header) {
						// pass
					}, function (error) {
						// pass
					});
				};
				$modalInstance.close(data, false);
			}, function (error) {
				// pass
			});
		// Otherwise we update it
		} else {
			ExtraTypeService.update({ id: $scope.extra_type.id  },$scope.extra_type,function(data, headers){
				for (var i = 0; i < $scope.extras.length; i++) {
					if ($scope.extras[i].id == undefined) {
						$scope.extras[i].extra_type = data.resource_uri;
						if ($scope.extras[i].price == ''){
							$scope.extras[i].price = 0;
						}
						var new_extra_option = new ExtraService($scope.extras[i]);
						new_extra_option.$save(function(data, header) {
							// pass
						}, function (error) {
							// pass
						});
					} else {
						if ($scope.extras[i].price == ''){
							$scope.extras[i].price = 0;
						}
						ExtraService.update({id: $scope.extras[i].id}, $scope.extras[i],
							function(data, headers){
								// pass								
						}, function (error){
							// pass
						});
					};
				};
				for (var i = 0; i < $scope.deleted.length; i++) {
					ExtraService.delete({id: $scope.deleted[i].id}, function(data, headers){
						// pass
					}, function (error){
						// pass
					});
				}
				$modalInstance.close(data, false);
			}, function(error){
				// pass
			})
		};
  	};

});