appRestaurant.controller('EditExtraCtrl', function($scope, $state, $stateParams, $modal, $modalInstance,
	usSpinnerService, RestaurantNavigationService, SettingService, ExtraTypeService){

	$scope.init = function () {
		ExtraTypeService.query({restaurant:RestaurantNavigationService.getRestaurant().id}, function(extra_types){
			$scope.extra_types = extra_types.objects;
		})
	};

	$scope.init();

	$scope.delExtraType = function (index) {
		ExtraTypeService.delete({id: $scope.extra_types[index].id}, function(data, headers){
			$scope.extra_types.splice(index,1);
		}, function (error){
			// pass
		});
	};


	$scope.cancel = function () {
    	$modalInstance.dismiss('cancel');
  	};

  	$scope.newExtra = function(selected) {
		var modalInstance = $modal.open({
	      templateUrl: '/static/partials/modal-crear-extra.html',
	      controller: 'NewExtraCtrl',
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