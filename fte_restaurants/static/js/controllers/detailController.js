app.controller('DetailController', function($scope,$filter, $state, $stateParams,$timeout,$modal, RestaurantService, CategoryService, ItemService,CityService, ZoneService, ScheduleService,NavigationService, usSpinnerService, SettingService, SelectableTypeService, SelectableService, ExtraService, AddressUserService){

	(function(){
		NavigationService.setHomeForm($stateParams)
	})()

	$scope.checkout_error = '';

	$scope.selected = "menu"



	

	$scope.authenticated = NavigationService.isAuthenticated()
	$scope.identification = NavigationService.getIdentity()

	if ($scope.authenticated) {
		$scope.selectedAddress = NavigationService.getAddress(); 
		if (!$scope.selectedAddress) {
			AddressUserService.get({"frontend_user": NavigationService.getIdentity().id}, function(addresses){
				$scope.addresses = addresses.objects;
				$scope.selectedAddress = $scope.addresses[0];
				NavigationService.setAddress($scope.selectedAddress);
			})
		};
	};


	RestaurantService.get({id:$stateParams['restaurant']}, function(restaurant){
		$scope.restaurant = restaurant
		NavigationService.setRestaurant($scope.restaurant)
		$scope.location = splitString(restaurant.location)
		$scope.marker = { id: restaurant.id, 
						  coords: {
						  	latitude: $scope.location[0],
						  	longitude: $scope.location[1],
						  }	
						}

		ScheduleService.query({restaurant:$stateParams['restaurant']}, function(schedules){
			for (var i = 0; i < schedules.objects.length; i++) {
				schedules.objects[i].start_time = Date.parse(schedules.objects[i].start_time);
				schedules.objects[i].start_time.addMinutes(
							parseInt(schedules.objects[i].start_time.getTimezoneOffset())*(-1));
				schedules.objects[i].finish_time = Date.parse(schedules.objects[i].finish_time);
				if (schedules.objects[i].finish_time.getHours() >= 0) {
					schedules.objects[i].finish_time.add(1).days();
				};
				schedules.objects[i].finish_time.addMinutes(
							parseInt(schedules.objects[i].finish_time.getTimezoneOffset())*(-1));
			};
			$scope.schedule = schedules.objects[0];
			var now = new Date.now();
			if (!now.between($scope.schedule.start_time, $scope.schedule.finish_time)){
				$scope.checkout_error = "El restaurante se encuentra cerrado y no es posible realizar órdenes.";
			}
		})

		$scope.mastercard = false;
		$scope.visa = false;
		$scope.american_express = false;
		$scope.paypal = false;
		for (var i = 0; i < $scope.restaurant.payment_methods.length; i++) {
			if ($scope.restaurant.payment_methods[i].name == 'mastercard') {
				$scope.mastercard = true;
			} else if ($scope.restaurant.payment_methods[i].name == 'visa') {
				$scope.visa = true;
			} else if ($scope.restaurant.payment_methods[i].name == 'american_express') {
				$scope.american_express = true;
			} else if ($scope.restaurant.payment_methods[i].name == 'paypal') {
				$scope.paypal = true;
			};
		};

		NavigationService.getUserOrder().then(function(order){
			$scope.current_order = order
			var subTotal = 0;
			var to_delete = [];
	      	for (var i = 0; i < $scope.current_order.length; i++) {
	      		if (order[i].item.category.restaurant == $scope.restaurant.resource_uri){
					subTotal += parseInt(order[i].total_item);
				} else {
					to_delete.push(i);
				}
	      	};
	      	to_delete.reverse();
	      	for (var i = 0; i < to_delete.length; i++) {
				$scope.current_order.splice(to_delete[i],1);
			};
	      	$scope.subTotal = subTotal;
		}, function(order){
			$scope.current_order = []
			$scope.subTotal = 0;
		});
	})

	CategoryService.query({restaurant:$stateParams['restaurant'], enabled: true}, function(categories){
		$scope.categories = categories.objects;
		angular.forEach($scope.categories, function(value, key){
			ItemService.query({"category": value.id, enabled: true, deleted: false}, function(items){
				value['items'] = items.objects;
			})
		})
	})
	
	$scope.map = { center: { latitude: 18.472413, longitude: -69.9403285 }, 
					zoom: 17, 
					events: {
            					'idle': function(map, eventName, arguments) {
            							
            							$timeout(function(){
            										
            										google.maps.event.trigger(map, 'resize');
            										map.setCenter(new google.maps.LatLng($scope.marker.coords.latitude, $scope.marker.coords.longitude));
            										map.setZoom(map.getZoom());
            										}, 500)
              							
            					},
            					'tilesloaded': function(map, eventName, arguments) {

            							
            							$timeout(function(){
            										google.maps.event.trigger(map, 'resize');
            										map.setCenter(new google.maps.LatLng($scope.marker.coords.latitude, $scope.marker.coords.longitude));
            										map.setZoom(map.getZoom());
            										}, 500)
              							
            					}, 	
            				},
            		options: {scrollwheel: false},
         		 }

    SettingService.get({key: 'ITBIS'}, function(itbis){
    	itbis = itbis.objects[0];
		$scope.itbis_value = itbis.value;
	})
	SettingService.get({key: 'LEGAL_TIP'}, function(legal_tip){
		legal_tip = legal_tip.objects[0];
		$scope.tip_value = legal_tip.value;
	})

	$scope.showSearch = function(){
		return true;
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
	
	$scope.checkOrder =  function(){
		NavigationService.setUserOrder($scope.current_order)
		NavigationService.setRestaurant($scope.restaurant)
		NavigationService.setAddress($scope.selectedAddress)
		$state.transitionTo("check_order")
	}

	var splitString = function(string) {
    	location_restaurant = string.split(',');
    	return location_restaurant;
	}

	$scope.remove = function( idx ) {
		$scope.subTotal -= parseInt($scope.current_order[idx].total_item); 
  		$scope.current_order.splice(idx, 1);
  		NavigationService.setUserOrder($scope.current_order)
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
	          	angular.forEach(item.extra_types, function(value, key){
	          		ExtraService.query({extra_type: value.id}, function(items){
						value.types = items.objects
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
      	$scope.current_order.push(item_order);
      	NavigationService.setUserOrder($scope.current_order);
      	$scope.subTotal += parseInt(item_order.total_item);
      } else {
      	var subTotal = 0;
      	for (var i = 0; i < $scope.current_order.length; i++) {
      		subTotal += parseInt($scope.current_order[i].total_item);
      	};
      	$scope.subTotal = subTotal;
      }
    }, function () {
    	// pass
    });
  	};


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
      });
    }



});