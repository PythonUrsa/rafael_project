appRestaurant.controller('RestaurantEditCtrl', function($scope,$filter, $state, $stateParams,$timeout,$modal,
		RestaurantService, CategoryService, ItemService, CityService, ZoneService, ScheduleService,
		TelephoneService, RestaurantNavigationService, usSpinnerService, SettingService, SelectableTypeService,
		SelectableService, ExtraService, OrderService, ItemOrderService){

	$scope.init = function(){
		$scope.pages = [];
		$scope.currentPage = 1;
		$scope.nextPage = null;
		$scope.offset = 0;
		$scope.totalOrders = 0;
		$scope.getOrders($scope.offset, $scope.filterDate);

	};

	$scope.getPaymentMethods = function(){
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

	};
	
	var splitString = function(string) {
    	location_restaurant = string.split(',');
    	return location_restaurant;
	}

	$('body').addClass("user");
	$('body').addClass("user-admin");
	$('body').removeClass("login");

	$scope.authenticated = RestaurantNavigationService.isAuthenticated()
	$scope.identification = RestaurantNavigationService.getIdentity()


	RestaurantService.get({user:$scope.identification.id}, function(restaurants){
		$scope.total = 0;
		$scope.restaurant = restaurants.objects[0];
		RestaurantNavigationService.setRestaurant($scope.restaurant);
		$scope.location = splitString($scope.restaurant.location);
		$scope.marker = {
	      id: $scope.restaurant.id,
	      coords: {
	        latitude: $scope.location[0],
	        longitude: $scope.location[1]
	      },
	      options: { draggable: true },
	      events: {
	        dragend: function (marker, eventName, args) {
	          $scope.marker.options = {
	            draggable: true,
	            labelContent: "lat: " + $scope.marker.coords.latitude + ' ' + 'lon: ' + $scope.marker.coords.longitude,
	            labelAnchor: "100 0",
	            labelClass: "marker-labels"
	          };
	        }
	      }
	    };

		ScheduleService.query({restaurant:$scope.restaurant.id}, function(schedules){
			for (var i = 0; i < schedules.objects.length; i++) {
				schedules.objects[i].start_time = Date.parse(schedules.objects[i].start_time);
				schedules.objects[i].start_time.addMinutes(
							parseInt(schedules.objects[i].start_time.getTimezoneOffset())*(-1));
				schedules.objects[i].finish_time = Date.parse(schedules.objects[i].finish_time);
				schedules.objects[i].finish_time.addMinutes(
							parseInt(schedules.objects[i].finish_time.getTimezoneOffset())*(-1));
			};
			$scope.schedules = schedules.objects
		});

		TelephoneService.query({restaurant:$scope.restaurant.id}, function(telephones){
			$scope.telephones = telephones.objects
		});
		$scope.filterDate = Date.parse('t').toString('yyyy-MM-dd') + ',' +
						Date.parse('t + 1').toString('yyyy-MM-dd');
		$scope.init();
		$scope.loadMenu();
		$scope.getPaymentMethods();
		
	})

	$scope.getOrders = function(offset, filter){
		OrderService.query({restaurant: $scope.restaurant.id, timestamp__range: filter, offset: offset}, function(orders){
			$scope.pages[$scope.pages.length] = orders.objects;
			$scope.totalOrders = orders.meta.total_count;
			$scope.nextPage = orders.meta.next;
			$scope.orders = $scope.pages[0];
			angular.forEach(orders.objects, function(order, key){
				$scope.total += parseFloat(order.total);
				if (order.payment_method.name == "cash") {
					order.payment_method = "Efectivo";
				} else {
					var payment_methods = ['paypal','mastercard', 'visa', 'american_express'];
					if (payment_methods.indexOf(order.payment_method.name) != -1) {
						order.payment_method = "Tarjeta de credito";
					};
				};
				order.timestamp = new Date(order.timestamp).toString("h:mm tt")
				$scope.orderItems = ItemOrderService.query(angular.extend({},{"order": order.id}), function(items){
			      	$scope.orders[key].items = items.objects;
				});
			})
			if ($scope.nextPage != null) {
				$scope.offset = $scope.nextPage.split('offset=')[1].split('&')[0];
				$scope.getOrders($scope.offset, $scope.filterDate);
			};
		})
	}


	$scope.loadMenu = function(){
		CategoryService.query({restaurant:$scope.restaurant.id}, function(categories){
			$scope.categories = categories.objects;
			angular.forEach($scope.categories, function(value, key){
				ItemService.query({"category": value.id, deleted: false}, function(items){
					value['items'] = items.objects;
				})
			})
		})
	}

	
	$scope.map = { center: { latitude: 18.472413, longitude: -69.9403285 }, 
					zoom: 17, 
					events: {
            					'tilesloaded': function(map, eventName, arguments) {
            							$timeout(function(){
            										google.maps.event.trigger(map, 'resize');
            										map.setCenter(new google.maps.LatLng($scope.marker.coords.latitude, $scope.marker.coords.longitude));
            										}, 1000)
              							
            					} 	
            				},
            		options: {scrollwheel: false},
         		 }

	$scope.showSearch = function(){
		return true;
	}



	$scope.newSection = function(selected) {
		 var modalInstance = $modal.open({
	      templateUrl: '/static/partials/modal-crear-seccion.html',
	      controller: 'NewSectionCtrl',
	      resolve: {
	        restaurant: function() {
	        	return $scope.restaurant;
	        },
	        selected: function() {
	        	return selected;
	        }
	      }
	    });

    modalInstance.result.then(function () {
		$scope.loadMenu();
    }, function() {
		// pass    	
    });
  	};

  	$scope.newProduct = function(selected) {
		 var modalInstance = $modal.open({
	      templateUrl: '/static/partials/modal-crear-producto.html',
	      controller: 'NewProductCtrl',
	      resolve: {
	      	selected: function() {
	      		return selected;
	      	}
	      }
	    });

    modalInstance.result.then(function () {
    	$scope.loadMenu();
    }, function () {
      //$log.info('Modal dismissed at: ' + new Date());
    });
  	};

  	$scope.deleteProduct = function(item) {
  		item.deleted = true;
  		var product = new ItemService(item);
		product.$save(function(data,headers) {
			$scope.loadMenu();
		}, function (error) {
			// pass
		});
  	};

  	$scope.editExtra = function() {
		 var modalInstance = $modal.open({
	      templateUrl: '/static/partials/modal-editar-extras.html',
	      controller: 'EditExtraCtrl',
	    });

    modalInstance.result.then(function () {
    	// pass
    }, function () {
      //$log.info('Modal dismissed at: ' + new Date());
    });
  	};

  	$scope.editSelectable = function() {
		 var modalInstance = $modal.open({
	      templateUrl: '/static/partials/modal-editar-selectable.html',
	      controller: 'EditSelectableCtrl',
	    });

    modalInstance.result.then(function () {
    	// pass
    }, function () {
      //$log.info('Modal dismissed at: ' + new Date());
    });
  	};

  	$scope.enable = function(target, isProduct){
		target.enabled = true;
  		if (isProduct) {
  			ItemService.update({id: target.id},{'enabled':true},function(data, headers){
  				// pass
			}, function(error){
				// pass
			})
  		} else {
  			CategoryService.update({id: target.id},{'enabled':true},function(data, headers){
  				// pass
			}, function(error){
				// pass
			})
  		};
	};

	$scope.disable = function(target, isProduct){
		target.enabled = false;
  		if (isProduct) {
  			ItemService.update({id: target.id},{'enabled':false},function(data, headers){
  				// pass
			}, function(error){
				// pass
			})
  		} else {
  			CategoryService.update({id: target.id},{'enabled':false},function(data, headers){
  				// pass
			}, function(error){
				// pass
			})
  		};
  	};

  	$scope.editAddress = function() {
		 var modalInstance = $modal.open({
	      templateUrl: '/static/partials/modal-editar-direccion-restaurant.html',
	      controller: 'EditInfoCtrl',
	      resolve: {
	      	restaurant: function() {
	        	return $scope.restaurant;
	        },
	      	address: function(){
	      		return $scope.restaurant.address;
	      	},
	      	schedules: function() {
	      		return $scope.schedules;
	      	},
	      	telephones: function () {
	      		$scope.telephones;
	      	}
	      }
	    });

    modalInstance.result.then(function (data) {
		if (data != false) {
			$scope.restaurant.address = data.address;
			RestaurantService.get({user:$scope.identification.id}, function(restaurants){
				$scope.total = 0;
				$scope.restaurant = restaurants.objects[0];
				RestaurantNavigationService.setRestaurant($scope.restaurant);
			});
		};
    }, function () {
      //$log.info('Modal dismissed at: ' + new Date());
    });
  	};

  	$scope.editSchedule = function() {
		 var modalInstance = $modal.open({
	      templateUrl: '/static/partials/modal-editar-horarios.html',
	      controller: 'EditInfoCtrl',
	      resolve: {
	      	restaurant: function() {
	        	return $scope.restaurant;
	        },
	      	address: function(){
	      		return $scope.restaurant.address;
	      	},
	      	schedules: function() {
	      		return $scope.schedules;
	      	},
	      	telephones: function () {
	      		$scope.telephones;
	      	}
	      }
	    });

    modalInstance.result.then(function (data) {
		if (data != false) {
			$scope.schedules = data;
		}
    }, function () {
      //$log.info('Modal dismissed at: ' + new Date());
    });
  	};

  	$scope.editPhones = function() {
		 var modalInstance = $modal.open({
	      templateUrl: '/static/partials/modal-editar-telefonos.html',
	      controller: 'EditInfoCtrl',
	      resolve: {
	      	restaurant: function() {
	        	return $scope.restaurant;
	        },
	      	address: function(){
	      		return $scope.restaurant.address;
	      	},
	      	schedules: function() {
	      		return $scope.schedules;
	      	},
	      	telephones: function () {
	      		return $scope.telephones;
	      	}
	      }
	    });

    modalInstance.result.then(function () {
		TelephoneService.query({restaurant:$scope.restaurant.id}, function(telephones){
			$scope.telephones = telephones.objects
		});
    }, function () {
      //$log.info('Modal dismissed at: ' + new Date());
    });
  	};

  	$scope.editPayment = function() {
		 var modalInstance = $modal.open({
	      templateUrl: '/static/partials/modal-editar-metodos-pago.html',
	      controller: 'EditInfoCtrl',
	      resolve: {
	      	restaurant: function() {
	        	return $scope.restaurant;
	        },
	      	address: function(){
	      		return $scope.restaurant.address;
	      	},
	      	schedules: function() {
	      		return $scope.schedules;
	      	},
	      	telephones: function () {
	      		return $scope.telephones;
	      	}
	      }
	    });

    modalInstance.result.then(function (data) {
		if (data){
			$scope.restaurant = data;
			$scope.getPaymentMethods();
		}
    }, function () {
      //$log.info('Modal dismissed at: ' + new Date());
    });
  	};

  	$scope.saveMarker = function() {
  		var new_marker = {
  			location: $scope.marker.coords.latitude.toString() + ',' +
  						$scope.marker.coords.longitude.toString()
  		}
  		RestaurantService.update({id: $scope.restaurant.id}, new_marker, function(data, headers){
  			// pass
		}, function (error){
			// pass
		});
  	};


  	$(function(){
	  $("#filters>li>a").click(function(){
	    
	    $("#filterName").text($(this).text() + ' ').append($('<span></span>')
        .addClass('caret')
    	);
	    $("filterName").val($(this).text());
	  });

	});


  	$scope.filter = function(filter) {
  		$scope.filterDate = Date.parse('t').toString('yyyy-MM-dd');
  		switch (filter) {
  			case 1:
  				// Today
  				$scope.filterDate = Date.parse('t').toString('yyyy-MM-dd') + ',' +
  							Date.parse('t + 1').toString('yyyy-MM-dd');
				break;
			case 2:
				// Yesterday
				$scope.filterDate = Date.parse('t - 1').toString('yyyy-MM-dd') + ',' +
  							Date.parse('t').toString('yyyy-MM-dd');
  				break;
			case 3:
				// Last week
				$scope.filterDate = Date.parse('t - 7').toString('yyyy-MM-dd') + ',' +
  							Date.parse('t').toString('yyyy-MM-dd');
				break;
		}
		$scope.pages = [];
		$scope.currentPage = 1;
		$scope.nextPage = null;
		$scope.offset = 0;
		$scope.total = 0;
		$scope.totalOrders = 0;
		$scope.getOrders($scope.offset, $scope.filterDate);
  	};

  	$scope.changeStatus = function(target, status, processed){
  		var newStatus = {};
  		if (processed){
  			newStatus.processed = status;
  		} else {
  			newStatus.delivered = status;
  		}
  		OrderService.update({id: target.id}, newStatus,function(data, headers){
  			// pass
		}, function(error){
			// pass
		})
  	};

  	$scope.pageChanged = function(){
		$scope.orders = $scope.pages[$scope.currentPage - 1];
	}

});