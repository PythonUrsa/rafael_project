appRestaurant.controller('EditInfoCtrl', function($scope, $state, $stateParams, $modal, $modalInstance,
	usSpinnerService, SettingService, RestaurantService, TelephoneService, ScheduleService,
	PaymentMethodService, restaurant, address, schedules, telephones){

	$scope.init = function() {
		$scope.deleted_phones = [];
		$scope.deleted_schedules = [];
		$scope.restaurant = restaurant;
		if (address) {
			$scope.address = address;
		};
		if (telephones) {
			$scope.telephones = eval('(' + JSON.stringify(telephones) + ')');
		};
		if (schedules) {
			$scope.schedules = eval('(' + JSON.stringify(schedules) + ')');
		};
		PaymentMethodService.query({}, function (methods){
			$scope.payment_methods = methods.objects;
			for (var j = 0; j < $scope.payment_methods.length; j++) {
				for (var i = 0; i < $scope.restaurant.payment_methods.length; i++) {
					if ($scope.payment_methods[j].name
							== $scope.restaurant.payment_methods[i].name) {
						$scope.payment_methods[j].selected = true;
						break;
					} else {
						$scope.payment_methods[j].selected = false;
					};
				};
			};
		});
	}
    
  	$scope.init()

	$scope.cancel = function () {
    	$modalInstance.close(false);
  	};

  	$scope.saveAddr = function () {
  		var new_address = {
  			address: $scope.address
  		};
  		RestaurantService.update({id: $scope.restaurant.id}, new_address, function(data, headers){
	  		$modalInstance.close(data, true);
		}, function (error){
			// pass
		});
  	}

  	$scope.newPhone = function () {
  		var new_phone = {
  			number: '',
  			description: ''
  		};
  		$scope.telephones.push(new_phone);
  	}
  	$scope.removePhone = function (index) {
  		if ($scope.telephones[index].id == undefined) {
			$scope.telephones.splice(index,1);
		} else {
			$scope.deleted_phones.push($scope.telephones[index])
			$scope.telephones.splice(index,1);
		};
  	}

  	$scope.saveTelephones = function () {
  		for (var i = 0; i < $scope.telephones.length; i++) {
  			if ($scope.telephones[i].id == undefined){
  				$scope.telephones[i].restaurant = $scope.restaurant.resource_uri;
	  			var new_phone = new TelephoneService($scope.telephones[i]);

				new_phone.$save(function(data,headers) {
					$modalInstance.close(data, true);
				}, function (error) {
					// pass
				});
  			} else {
	  			TelephoneService.update({id: $scope.telephones[i].id}, $scope.telephones[i],
	  				function(data, headers){
				  		$modalInstance.close(data, true);
				}, function (error){
					// pass
				});
  			};
  		};
  		for (var i = 0; i < $scope.deleted_phones.length; i++) {
  			TelephoneService.delete({id: $scope.deleted_phones[i].id}, function(data, headers){
		  		$modalInstance.close(data, true);
			}, function (error){
				// pass
			});
  		};
  	}

  	$scope.removeSchedule = function (index) {
  		if ($scope.schedules[index].id == undefined) {
			$scope.schedules.splice(index,1);
		} else {
			$scope.deleted_schedules.push($scope.schedules[index])
			$scope.schedules.splice(index,1);
		};
  	};

  	$scope.newSchedule = function() {
  		var new_schedule = {
  			start_time: '',
  			finish_time: ''
  		};
  		$scope.schedules.push(new_schedule);
  	};

  	$scope.saveSchedules = function () {
  		for (var i = 0; i < $scope.schedules.length; i++) {
  			if ($scope.schedules[i].id == undefined){
  				$scope.schedules[i].restaurant = $scope.restaurant.resource_uri;
	  			var new_schedule = new ScheduleService($scope.schedules[i]);

				new_schedule.$save(function(data,headers) {
				}, function (error) {
					// pass
				});
  			} else {
	  			ScheduleService.update({id: $scope.schedules[i].id}, $scope.schedules[i],
	  				function(data, headers){
	  					// pass
				}, function (error){
					// pass
				});
  			};
  		};
  		for (var i = 0; i < $scope.deleted_schedules.length; i++) {
  			ScheduleService.delete({id: $scope.deleted_schedules[i].id}, function(data, headers){
  				// pass
			}, function (error){
				// pass
			});
  		};
  		ScheduleService.query({restaurant:$scope.restaurant.id}, function(schedules){
			$scope.schedules = schedules.objects
		});
  		$modalInstance.close($scope.schedules, true);
  	}

  	$scope.savePayment = function () {
  		var selected_methods = {
  			payment_methods: []};
  		for (var i = 0; i < $scope.payment_methods.length; i++) {
  			if ($scope.payment_methods[i].selected){
  				selected_methods.payment_methods.push($scope.payment_methods[i].resource_uri);
  			}
  		};
  		RestaurantService.update({id: $scope.restaurant.id}, selected_methods, function(data, headers){
	  		$modalInstance.close(data, true);
		}, function (error){
			// pass
		});
  	};

});