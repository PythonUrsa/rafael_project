app.controller('ModalPayCash', function($scope,$modalInstance, $state, NavigationService, OrderService,
	total, order, restaurant, address, additional_info, rnc, payment_method, order_type){

	$scope.cancel = $scope.$dismiss;

	$scope.total = total;
	$scope.order = order;
	$scope.restaurant = restaurant;
	$scope.address = address;
	$scope.additional_info = additional_info;
	$scope.rnc = rnc;
	$scope.payment_method = payment_method;
	$scope.order_type = order_type;
	$scope.user = NavigationService.getIdentity();
	$scope.saving = false;

	$scope.dismiss = function(){
        $modalInstance.dismiss('cancel');
    };

    $scope.confirm = function(){
    	$scope.saving = true;
    	var change = $scope.amount - $scope.total;
    	if (change >= 0) {
	    	var order = {
	    		restaurant: $scope.restaurant.resource_uri,
	    		user: "/api/v1/auth/user/" + $scope.user.id + "/",
	    		items: $scope.order,
	    		total: $scope.total,
	    		change: change,
	    		delivery_address: $scope.address.resource_uri,
	    		additional_info: $scope.additional_info,
	    		rnc: $scope.rnc,
	    		payment_method: $scope.payment_method,
	    		order_type: $scope.order_type
	    	}
    		var order_selectables = [];
    		var item_selectables = [];
	    	for (var i = 0; i < order.items.length; i++) {
	    		order_selectables = order.items[i].selectables_associated;
		    	for (var j = 0; j < order_selectables.length; j++) {
		    		item_selectables = order.items[i].item.selectable_types[j];
		    		order_selectables[j] = item_selectables.types[order_selectables[j]];
		    		item_selectables = [];
	    		};
	    		order_selectables = [];
	    	};
	    	var new_order = new OrderService(order)
			new_order.$save(function(data,headers) {
				if (data.error){
					$modalInstance.close(data.error, false);
				}else {
					$modalInstance.dismiss('cancel');
					NavigationService.setUserOrder([]);
					$state.go('orderConfirmation', {"order": data.id});
				}
			}, function (error) {
				// pass
			});
    	} else {
    		$scope.saving = false;
    	};
    }
});