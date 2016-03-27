app.controller('CheckOrderController', function($scope,$filter, $state, $stateParams,$timeout,$modal,
	RestaurantService, CategoryService, ItemService,CityService, ZoneService, ScheduleService,
	NavigationService, usSpinnerService, SettingService, SelectableTypeService, SelectableService,
	ExtraService, FEUserService, RNCUserService, AddressUserService){

	$scope.subTotal = 0;
	$scope.selectedAddress = '';
	$scope.error_address_zone = false;
	$scope.checkout_error = '';

	NavigationService.getUserOrder().then(function(order){
		$scope.restaurant = NavigationService.getRestaurant();
		$scope.user_order = order
		$scope.order_type = 'DELIVERY';
		var subTotal = 0;
		var to_delete = [];
		for (var i = 0; i < order.length; i++) {
			if (order[i].item.category.restaurant == $scope.restaurant.resource_uri){
				subTotal += parseInt(order[i].total_item);
			} else {
				to_delete.push(i);
			}
		};
		to_delete.reverse();
		for (var i = 0; i < to_delete.length; i++) {
			order.splice(to_delete[i],1);
		};
		$scope.subTotal = subTotal;
	}, function(order){
		//$state.go("home")
	});

	$scope.user = NavigationService.getIdentity();

	FEUserService.get({"id": NavigationService.getIdentity().id}, function(user){
		$scope.user = user;
	})

	$scope.selectedAddress = NavigationService.getAddress();
	if (!$scope.selectedAddress) {
		AddressUserService.get({"frontend_user": NavigationService.getIdentity().id}, function(addresses){
			$scope.addresses = addresses.objects;
			$scope.selectedAddress = $scope.addresses[0];
			NavigationService.setAddress($scope.selectedAddress);
		})
	};


	RNCUserService.get({frontend_user:NavigationService.getIdentity().id, main: true}, function(rncs){
		$scope.rncs = rncs.objects
	})

	SettingService.get({key: 'ITBIS'}, function(itbis){
    	itbis = itbis.objects[0];
		$scope.itbis_value = itbis.value;
	})
	SettingService.get({key: 'LEGAL_TIP'}, function(legal_tip){
		legal_tip = legal_tip.objects[0];
		$scope.tip_value = legal_tip.value;
	})

	$scope.back = function(){
		$state.go("detail", {"restaurant": $scope.restaurant.id})
	}

	$scope.open_rnc = function() {
		 var modalInstance = $modal.open({
	      templateUrl: '/static/partials/modal_edit_rnc.html',
	      controller: 'ModalRNCController',
	      resolve: {
	      	user: function(){
	      			return $scope.user
	      	},
	      }
	    });

    modalInstance.result.then(function () {
     	RNCUserService.get({frontend_user:NavigationService.getIdentity().id, main: true}, function(rncs){
		$scope.rncs = rncs.objects	
		})
      });
    }

    $scope.open_addr = function() {
		 var modalInstance = $modal.open({
	      templateUrl: '/static/partials/modal-admin-direccion.html',
	      controller: 'ModalAddressCtrl',
	      resolve: {
	      	user: function(){
      			return $scope.user;
	      	}
	      }
	    });

    modalInstance.result.then(function (selected) {
     	$scope.selectedAddress = selected;
     	NavigationService.setAddress(selected);
      });
    }

    $scope.getTotal = function(subTotal, deliveryFee){
		var total = 0;
		var itbis = 0;
		var tip = 0;
		total = parseInt(subTotal) + parseInt(deliveryFee);
		$scope.itbis = total * ($scope.itbis_value / 100);
		$scope.tip = total * ($scope.tip_value / 100);
		return (total + $scope.itbis + $scope.tip);
	};

	$scope.accepts_cash = function(){
		for (var i = 0; i < $scope.restaurant.payment_methods.length; i++) {
			if ($scope.restaurant.payment_methods[i].name == 'cash') {
				return true;
			};
		};
		return false;
	};
	$scope.accepts_card = function(){
		var payment_methods = ['mastercard', 'visa', 'american_express'];
		for (var i = 0; i < $scope.restaurant.payment_methods.length; i++) {
			if (payment_methods.indexOf($scope.restaurant.payment_methods[i].name) != -1) {
				return true;
			};
		};
		return false;
	};

    $scope.open_pay_cash = function() {
    	if ($scope.getTotal($scope.subTotal, $scope.restaurant.delivery_cost) <
    			parseInt($scope.restaurant.order_minimum)
    			&& $scope.order_type == 'DELIVERY') {
    		$scope.checkout_error = "Valor del pedido menor a valor minimo para delivery";
    	} else {
    		 $scope.checkout_error = '';
			 var modalInstance = $modal.open({
		      templateUrl: '/static/partials/modal_pay_cash.html',
		      controller: 'ModalPayCash',
		      resolve: {
		      	total : function(){
		      		return $scope.getTotal($scope.subTotal, $scope.restaurant.delivery_cost)
		      	},
		      	order : function(){
		      		return $scope.user_order;
		      	},
		      	restaurant : function(){
		      		return $scope.restaurant;
		      	},
		      	address : function(){
		      		return $scope.selectedAddress;
		      	},
		      	additional_info : function() {
		      		if ($scope.additional_info == undefined) {
		      			$scope.additional_info = '';
		      		};
		      		return $scope.additional_info;
		      	},
		      	rnc : function() {
		      		if ($scope.rncs[0] != undefined) {
			      		return $scope.rncs[0];
		      		} else {
		      			return '';
		      		};
		      	},
		      	payment_method : function() {
		      		for (var i = 0; i < $scope.restaurant.payment_methods.length; i++) {
						if ($scope.restaurant.payment_methods[i].name == 'cash') {
							return $scope.restaurant.payment_methods[i].resource_uri;
						};
					};
		      	},
		      	order_type: function(){
		      		return $scope.order_type;
		      	}
		      }
		    });

	    modalInstance.result.then(function (result) {
	     	if (result.code == "does_not_belong") {
	     		$scope.error_address_zone = true;
	     	};
	     	if (result.code) {
	     		$scope.checkout_error = result.message;
	     	};
		})
    	}
	}


    $scope.open_pay_card = function() {
    	if ($scope.getTotal($scope.subTotal, $scope.restaurant.delivery_cost) <
    			parseInt($scope.restaurant.order_minimum)
    			&& $scope.order_type == 'DELIVERY') {
    		$scope.checkout_error = "Valor del pedido menor a valor minimo para delivery";
    	} else {
    		 $scope.checkout_error = '';
			 var modalInstance = $modal.open({
		      templateUrl: '/static/partials/modal_pay_card.html',
		      controller: 'ModalPayCard',
		      resolve: {
		      	phone: function(){
		      	 	return $scope.user.telephone
		      	},
		      	total : function(){
		      		return $scope.getTotal($scope.subTotal, $scope.restaurant.delivery_cost)
		      	},
		      	order : function(){
		      		return $scope.user_order;
		      	},
		      	restaurant : function(){
		      		return $scope.restaurant;
		      	},
		      	address : function(){
		      		return $scope.selectedAddress;
		      	},
		      	additional_info : function() {
		      		if ($scope.additional_info == undefined) {
		      			$scope.additional_info = '';
		      		};
		      		return $scope.additional_info;
		      	},
		      	rnc : function() {
		      		if ($scope.rncs[0] != undefined) {
			      		return $scope.rncs[0];
		      		} else {
		      			return '';
		      		};
		      	},
		      	payment_method : function() {
		      		/*for (var i = 0; i < $scope.restaurant.payment_methods.length; i++) {
						if ($scope.restaurant.payment_methods[i].name == 'card') {
							return $scope.restaurant.payment_methods[i].resource_uri;
						};
					};*/
					return '';
		      	},
		      	order_type: function(){
		      		return $scope.order_type;
		      	}
		      }
		    });

	    modalInstance.result.then(function (result) {
	     	if (result.code == "does_not_belong") {
	     		$scope.error_address_zone = true;
	     	};
	     	if (result.code) {
	     		$scope.checkout_error = result.message;
	     	};
		})
	};
	}
    

	$scope.remove = function( idx ) {
		$scope.subTotal -= parseInt($scope.user_order[idx].total_item); 
  		$scope.user_order.splice(idx, 1);
  	}

	$scope.open = function(item, edit_order) {
		 var modalInstance = $modal.open({
	      templateUrl: '/static/partials/modal_order.html',
	      controller: 'ModelOrderController',
	      resolve: {
	        complete_item: function() {
	          if(edit_order == null){
	          	 angular.forEach(item.selectable_types, function(value, key){
	          		SelectableService.query({selectable_type: value.id}, function(items){
						value['types'] = items.objects
					})
	          	})
	          	 return item
	          }else{
	          	return edit_order.item
	          }
	        },
	        edit_order: function(){
	        	return edit_order
	        },
	        selectables_associated: function() {
	        	var selectables = [];
	        	for (var i = 0; i < item.selectable_types.length; i++) {
	        		selectables[i] = 0;
	        	};
	          	return selectables;
	        }
	      }
	    });

    modalInstance.result.then(function (item_order) {
      if (item_order.new == true){
      	$scope.user_order.push(item_order);
      	$scope.subTotal += parseInt(item_order.total_item);
      } else {
      	var subTotal = 0;
      	for (var i = 0; i < $scope.user_order.length; i++) {
      		subTotal += parseInt($scope.user_order[i].total_item);
      	};
      	$scope.subTotal = subTotal;
      }
    }, function () {
      //$log.info('Modal dismissed at: ' + new Date());
    });
  	};

});