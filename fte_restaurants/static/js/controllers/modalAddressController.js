app.controller('ModalAddressCtrl', function($scope,$filter, $http, $state, $stateParams,$timeout,$modal,$modalInstance, NavigationService, CityService, ZoneService, AddressUserService, usSpinnerService, editAddressModal, user){
	

	$scope.user = user;
	$scope.addresses = [];
	$scope.selectedAddr = 0;

	$scope.cities = CityService.query(function(){
    });

	$scope.update_addresses = function() {
		AddressUserService.get({"frontend_user": NavigationService.getIdentity().id}, function(addresses){
			$scope.addresses = addresses.objects
		});
	}

	$scope.update_addresses();

    $scope.zones = ZoneService.query({city: $scope.city});

    $scope.$watch('new_address.city', function (newValue, oldValue) {
        if (newValue == oldValue) { return;}
            usSpinnerService.spin('spinner-1');
            if(newValue == "" || newValue == null){
                $scope.zones = ZoneService.query(function(){
                });
            }else{
                $scope.zones = ZoneService.query({city: newValue});
            }
            
    },true);

	$scope.dismiss = function(){
        $modalInstance.dismiss('cancel');
    };

	$scope.isSelected = function(index){
		return index == $scope.selectedAddr;
	};

	$scope.changeSelected = function(index){
		$scope.selectedAddr = index;
	};

	$scope.openEdit = function(index){
		$scope.selectedAddr = index;
		editAddressModal($scope);
	};

	$scope.addAddress = function(){
		// $scope.new_address.delivery_zone = $scope.new_address.delivery_zone.originalObject.id;
		$scope.new_address.delivery_zone = '/api/v1/zone/' + $scope.new_address.delivery_zone + '/';
		var city = "/api/v1/city/" + $scope.new_address.city + "/";

		var addr = {
			street_name: $scope.new_address.street_name,
			street_number: $scope.new_address.street_number,
			city: city,
			delivery_zone: $scope.new_address.delivery_zone,
			associated_name: $scope.new_address.associated_name,
			reference: $scope.new_address.reference,
			frontend_user: "/api/v1/auth/user/" + NavigationService.getIdentity().id + "/"
		}
		url = '/api/v1/user/address/';
		$http.post(url, addr).success(function(returnedAddress){
			$scope.addresses.push(returnedAddress);
			// Clean scope
			$scope.new_address.street_name = '';
			$scope.new_address.street_number = '';
			$scope.new_address.city = '';
			$scope.new_address.delivery_zone = "";
			$scope.new_address.associated_name = '';
			$scope.new_address.reference = '';
		}).error(function(data){
			// pass
		});
	};

	$scope.delAddress = function(index){
		url = '/api/v1/user/address/' + $scope.addresses[index].id + '/' 
		$http.delete(url,{}).success(function(returnedAddress){
			$scope.addresses.splice(index,1);
		}).error(function(data){
			// pass
		});
	};

	$scope.set_main = function(id){
		AddressUserService.update({ id: id  },{'main': true},function(data, headers){
			$scope.update_addresses()
		}, function(error){
			// pass
		})
	}

	$scope.ok = function () {
		var index = $scope.selectedAddr
		$modalInstance.close($scope.addresses[index]);
	};

});