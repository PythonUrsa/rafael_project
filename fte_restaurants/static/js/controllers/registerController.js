app.controller('RegisterCtrl', function($scope, $filter, $state, $http, RegisterUser, CityService, ZoneService, PhotoService, NavigationService, usSpinnerService, SettingService, AddressUserService){

	$('body').addClass("user");
	$('body').removeClass("search");
	$('body').removeClass("home");


	$scope.submit_error = '';
	$scope.profile_picture = '';
	$scope.saving = false;

	$scope.today = function() {
		$scope.dt = new Date();
	};
	$scope.today();

	$scope.clear = function () {
		$scope.dt = null;
	};

	$scope.open = function($event) {
		$event.preventDefault();
		$event.stopPropagation();

		$scope.opened = true;
	};

	$scope.dateOptions = {
    	formatYear: 'yyyy',
    	startingDay: 0
  	};
  	$scope.format = 'dd/MM/yyyy';

	$scope.cities = CityService.query(function(){
	});

	$scope.zones = ZoneService.query(function(){
		// pass
	});

	$scope.submit = function(){
		$scope.saving = true;
		if ($scope.user.gender == undefined){
			$scope.user.gender = 'M';
		};
		if ($scope.user.password == $scope.user.confirmation){
			$scope.address.delivery_zone = '/api/v1/zone/' + $scope.address.delivery_zone + '/'

			var url = '/api/v1/auth/user/';
			var newUser = {
				first_name: $scope.user.first_name,
				last_name: $scope.user.lastname,
				telephone: $scope.user.phone,
				email: $scope.user.email,
				gender: $scope.user.gender,
				password: $scope.user.password,
				date_of_birth: $scope.user.birthday,
			}

			RegisterUser.registerFTEUser(newUser, $scope.profile_picture.file, function(returnedUser){
				if (returnedUser.error){
					$scope.submit_error = returnedUser.error.message;
					$scope.saving = false;
				} else {
					var credentials = {
						'email': newUser.email,
						'password': newUser.password,
					};
					NavigationService.authenticate(credentials).then(
			        	function (user) {
							var new_address = new AddressUserService($scope.address)
							new_address.frontend_user = '/api/v1/auth/user/' + returnedUser.id + '/';
							new_address.city = "/api/v1/city/" + $scope.address.city + "/";

							new_address.$save(function(data,headers) {
								// pass								
							}, function (error) {
								$scope.saving = false;
							});
				            AddressUserService.get({frontend_user:NavigationService.getIdentity().id, main: true}, function(addresses){
				              NavigationService.setAddress(addresses.objects[0]);
				            })
				            NavigationService.getUserOrder().then(function(order){
								if (order.length) {
									$state.transitionTo("check_order");
								} else {
									$state.go("profile", {"user": NavigationService.getIdentity().id});
								};
							}, function(order){
								$scope.saving = false;
							});
							$state.go("profile", {"user": NavigationService.getIdentity().id})
			    		},
		    		function(result){
			    			$scope.saving = false;
		    		});
				
				}
			})
			$scope.submit_error = "Password y confirmacion no coinciden"
			$scope.saving = false;
		}
	};


	$scope.onFileSelect = function(element) {
		$scope.$apply(function(scope) {
			// Turn the FileList object into an Array
			for (var i = 0; i < element.files.length; i++) {
				$scope.dataMedia.push(element.files[i])
	        }
      	});
    };

	$scope.$watch('address.city', function (newValue, oldValue) {
 	    if (newValue == oldValue) { return;}
 	    	usSpinnerService.spin('spinner-1');
 	    	if(newValue == "" || newValue == null){
 	    		$scope.zones = ZoneService.query(function(){
				});
 	    	}else{
				$scope.zones = ZoneService.query({city: newValue});
 	    	}
        	
    },true);
});