appRestaurant.controller('EditSelectableCtrl', function($scope, $state, $stateParams, $modal, $modalInstance,
	usSpinnerService, RestaurantNavigationService, SettingService, CategoryService, SelectableTypeService){

	$scope.init = function () {
		CategoryService.query({restaurant:RestaurantNavigationService.getRestaurant().id}, function(categories){
			$scope.categories = categories.objects;
			$scope.selectable_types = [];
			for (var i = 0; i < $scope.categories.length; i++) {
				SelectableTypeService.query({category:$scope.categories[i].id},
					function(selectable_types){
						$scope.selectable_types = $scope.selectable_types.concat(selectable_types.objects);
				})
			};
		})
	};

	$scope.init();

	$scope.delSelectableType = function (index) {
		SelectableTypeService.delete({id: $scope.selectable_types[index].id}, function(data, headers){
			$scope.selectable_types.splice(index,1);
		}, function (error){
			// pass
		});
	};


	$scope.cancel = function () {
    	$modalInstance.dismiss('cancel');
  	};

  	$scope.newSelectable = function(selected) {
		var modalInstance = $modal.open({
       	  templateUrl: '/static/partials/modal-crear-selectable.html',
	      controller: 'NewSelectableCtrl',
	      resolve: {
	      	selected: function() {
	      		return selected;
	      	}
	      }
	    });

    modalInstance.result.then(function () {
		$scope.init();
    }, function () {
      //$log.info('Modal dismissed at: ' + new Date());
    });
  	};

});