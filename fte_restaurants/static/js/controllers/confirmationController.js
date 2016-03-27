app.controller('ConfirmationCtrl', function($scope, $stateParams, $state, NavigationService, OrderService, ItemOrderService, SettingService){

	$scope.init = function(){

		OrderService.get({id:$stateParams['order']}, function(order){
			$scope.order = order;

			var subTotal = 0;
			$scope.orderItems = ItemOrderService.query(angular.extend({},{"order": $scope.order.id}), function(items){
		      	for (var i = 0; i < items.objects.length; i++) {
		      		subTotal += parseInt(items.objects[i].total_item);
		      	};
		      	$scope.subTotal = subTotal;
		      	$scope.itbis = ($scope.subTotal + parseInt($scope.order.restaurant.delivery_cost)) * ($scope.itbis_value / 100);
		      	$scope.tip = ($scope.subTotal + parseInt($scope.order.restaurant.delivery_cost)) * ($scope.tip_value / 100);
			});
		})

		SettingService.get({key: 'ITBIS'}, function(itbis){
	    	itbis = itbis.objects[0];
			$scope.itbis_value = itbis.value;
		})
		SettingService.get({key: 'LEGAL_TIP'}, function(legal_tip){
			legal_tip = legal_tip.objects[0];
			$scope.tip_value = legal_tip.value;
		})

	};

	$scope.init();

	$scope.goHome = function(){
		$state.go("home");
	}

});