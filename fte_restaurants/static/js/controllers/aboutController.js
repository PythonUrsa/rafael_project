var AboutUsController = appRestaurant.controller('AboutUsController', function($scope, $http, $state,
	$stateParams, $window, TextSettingsService){

	$scope.about = ""
	TextSettingsService.get({key: 'ABOUT_US'}, function(data){
			$scope.about = data.objects[0].value;
	})


});

var ContactController = appRestaurant.controller('ContactController', function($scope,$http,$state,$stateParams,$window, TextSettingsService){

$scope.contact = ""
TextSettingsService.get({key: 'CONTACT'}, function(data){
		$scope.contact = data.objects[0].value;
	})


});

var EmploymentController = appRestaurant.controller('EmploymentController', function($scope,$http,$state,$stateParams,$window, TextSettingsService){

$scope.employment = ""
TextSettingsService.get({key: 'EMPLOYMENT'}, function(data){
		$scope.employment = data.objects[0].value;
	})


});