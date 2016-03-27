appRestaurant.controller('NewProductCtrl', function($scope, $state, $stateParams, $modal, $modalInstance,
	usSpinnerService, SettingService, RestaurantNavigationService, CategoryService, ItemService,
	SelectableTypeService, ExtraTypeService, selected){

	$scope.init = function(){
		CategoryService.query({restaurant:RestaurantNavigationService.getRestaurant().id}, function(categories){
			$scope.categories = categories.objects;
			if (selected) {
				$scope.new_product = selected;
				SelectableTypeService.query({restaurant:RestaurantNavigationService.getRestaurant().id,
		  			category: selected.category.id},
					function(selectable_types){
						$scope.selectable_types = selectable_types.objects;
						selected.category = selected.category.resource_uri;
						// $scope.new_product.category = selected.category.resource_uri;
						for (var i = 0; i < $scope.new_product.selectable_types.length; i++) {
							for (var j = 0; j < $scope.selectable_types.length; j++) {
								if ($scope.selectable_types[j].id == $scope.new_product.selectable_types[i].id){
									$scope.selectable_types[j].selected = true;
									break;
								}
							};
						};
				});
				ExtraTypeService.query({restaurant:RestaurantNavigationService.getRestaurant().id}, function(extra_types){
					$scope.extra_types = extra_types.objects;
					for (var i = 0; i < $scope.new_product.extra_types.length; i++) {
						for (var j = 0; j < $scope.extra_types.length; j++) {
							if ($scope.extra_types[j].id == $scope.new_product.extra_types[i].id){
								$scope.extra_types[j].selected = true;
								break;
							}
						};
					};
				});
			} else {
				$scope.new_product = {};
				$scope.new_product.category = $scope.categories[0].resource_uri;
				var category_id = $scope.new_product.category.split('/') 
				category_id = category_id[category_id.length - 2];
				SelectableTypeService.query({category: category_id},
					function(selectable_types){
						$scope.selectable_types = selectable_types.objects;
				});
				ExtraTypeService.query({restaurant:RestaurantNavigationService.getRestaurant().id}, function(extra_types){
					$scope.extra_types = extra_types.objects;
				});
			};
		});
	};

	$scope.init();

	$scope.$watch('new_product.category', function (newValue, oldValue) {
  		if (newValue == oldValue || typeof(oldValue) != 'string') {return;}
  		var category_id = newValue.split('/') 
  		category_id = category_id[category_id.length - 2];
  		SelectableTypeService.query({restaurant:RestaurantNavigationService.getRestaurant().id,
  			category: category_id},
			function(selectable_types){
				$scope.selectable_types = selectable_types.objects;
		});
  	}, true);

	$scope.cancel = function () {
    	$modalInstance.close(false);
  	};

  	$scope.ok = function () {
  		$scope.new_product.selectable_types = [];
  		for (var i = 0; i < $scope.selectable_types.length; i++) {
  			if ($scope.selectable_types[i].selected){
  				$scope.new_product.selectable_types.push($scope.selectable_types[i].resource_uri);
  			}
  		};
  		$scope.new_product.extra_types = [];
  		for (var i = 0; i < $scope.extra_types.length; i++) {
  			if ($scope.extra_types[i].selected){
  				$scope.new_product.extra_types.push($scope.extra_types[i].resource_uri);
  			}
  		};
  		var new_product = new ItemService($scope.new_product);
		new_product.$save(function(data,headers) {
			$modalInstance.close(data, false);
		}, function (error) {
			// pass
		});
  	};

});