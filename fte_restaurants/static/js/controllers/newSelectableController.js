appRestaurant.controller('NewSelectableCtrl', function($scope, $state, $stateParams, $modal, $modalInstance,
	usSpinnerService, RestaurantNavigationService, SettingService, SelectableTypeService, SelectableService,
	CategoryService, selected){

	CategoryService.query({restaurant:RestaurantNavigationService.getRestaurant().id}, function(categories){
			$scope.categories = categories.objects;
	})

	$scope.addOption = function () {
		var selectable = {
			name: "",
			price: ""
		};
		$scope.selectables.push(selectable);
	};

	$scope.init = function () {
		$scope.deleted = [];
		if (!selected){
			$scope.selectables = [];
			$scope.addOption();
		} else {
			$scope.selectable_type = selected;
			$scope.selectable_type.category = selected.category;
			SelectableService.query({selectable_type:selected.id}, function(selectables){
				$scope.selectables = selectables.objects;
			})
		}
	};

	$scope.init();

	$scope.delOption = function (index) {
		if ($scope.selectables[index].id == undefined) {
			$scope.selectables.splice(index,1);
		} else {
			$scope.deleted.push($scope.selectables[index])
			$scope.selectables.splice(index,1);
		};
	};


	$scope.cancel = function () {
    	$modalInstance.dismiss('cancel');
  	};

  	$scope.ok = function () {
  		// If it's a new SelectableType we create it
		if ($scope.selectable_type.id == undefined) {
	  		var selectable_type = {
	  			category: $scope.selectable_type.category,
	  			name: $scope.selectable_type.name
	  		};
	  		var new_selectable_type = new SelectableTypeService(selectable_type);

			new_selectable_type.$save(function(data,headers) {
				for (var i = 0; i < $scope.selectables.length; i++) {
					$scope.selectables[i].selectable_type = data.resource_uri;
					if ($scope.selectables[i].price == ''){
						$scope.selectables[i].price = 0;
					}
					var new_selectable = new SelectableService($scope.selectables[i]);
					new_selectable.$save(function(data, header) {
						// pass
					}, function (error) {
						// pass
					});
				};
				$modalInstance.close(data, false);
			}, function (error) {
				// pass
			});
		} else {
			SelectableTypeService.update({ id: $scope.selectable_type.id  },$scope.selectable_type,function(data, headers){
				for (var i = 0; i < $scope.selectables.length; i++) {
					if ($scope.selectables[i].id == undefined) {
						$scope.selectables[i].selectable_type = data.resource_uri;
						if ($scope.selectables[i].price == ''){
							$scope.selectables[i].price = 0;
						}
						var new_selectable_option = new SelectableService($scope.selectables[i]);
						new_selectable_option.$save(function(data, header) {
							// pass
						}, function (error) {
							// pass
						});
					} else {
						if ($scope.selectables[i].price == ''){
							$scope.selectables[i].price = 0;
						}
						SelectableService.update({id: $scope.selectables[i].id}, $scope.selectables[i],
							function(data, headers){
								// pass
						}, function (error){
							// pass
						});
					};
				};
				for (var i = 0; i < $scope.deleted.length; i++) {
					SelectableService.delete({id: $scope.deleted[i].id}, function(data, headers){
						// pass
					}, function (error){
						// pass
					});
				}
				$modalInstance.close(data, false);
			}, function(error){
				// pass
			})
		}
  	};

});