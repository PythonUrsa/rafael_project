app.controller('EditAddressModalCtrl', function($scope, $state, $modalInstance, $http, NavigationService, CityService, ZoneService, usSpinnerService, addresses, selectedAddr) {

    $scope.cancel = $scope.$dismiss;

    $scope.addresses = addresses;
    $scope.selectedAddr = selectedAddr;

    // Set current address values
    var addressList = $scope.addresses;
    $scope.street_name = addressList[selectedAddr].street_name;
    $scope.street_number = addressList[selectedAddr].street_number;
    $scope.city = addressList[selectedAddr].city.id;
    $scope.delivery_zone = addressList[selectedAddr].delivery_zone.id;
    $scope.associated_name = addressList[selectedAddr].associated_name;
    $scope.reference = addressList[selectedAddr].reference;


    $scope.cities = CityService.query(function(){
    });

    $scope.zones = ZoneService.query({city: $scope.city});

    $scope.$watch('city', function (newValue, oldValue) {
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

    $scope.ok = function() {
        $scope.delivery_zone = '/api/v1/zone/' + $scope.delivery_zone + '/';
        var city = "/api/v1/city/" + $scope.city + "/";

        var addr = {
            street_name: $scope.street_name,
            street_number: $scope.street_number,
            city: city,
            delivery_zone: $scope.delivery_zone,
            associated_name: $scope.associated_name,
            reference: $scope.reference,
            frontend_user: "/api/v1/auth/user/" + NavigationService.getIdentity().id + "/"
        }
        var current = $scope.addresses[selectedAddr];
        url = '/api/v1/user/address/' + current.id + '/';
        $http.patch(url, addr).success(function(returnedAddress){
            // Change local address data
            current.street_name = returnedAddress.street_name;
            current.street_number = returnedAddress.street_number;
            current.city = returnedAddress.city;
            current.delivery_zone = returnedAddress.delivery_zone;
            current.associated_name = returnedAddress.associated_name;
            current.reference = returnedAddress.reference;
            $scope.$close();
        }).error(function(data){
            // pass
        });
    };

});