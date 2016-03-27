var TermsController = app.controller('TermsController', function($scope,$http,$state,$stateParams,$window, TextSettingsService){

$scope.terms = ""
TextSettingsService.get({key: 'TERMS'}, function(data){
		$scope.terms = data.objects[0].value;
	})


});

var PoliticsController = app.controller('PoliticsController', function($scope,$http,$state,$stateParams,$window, TextSettingsService){

$scope.politics = ""
TextSettingsService.get({key: 'POLITICS'}, function(data){
		$scope.politics = data.objects[0].value;
	})


});

var ConditionsController = app.controller('conditionsController', function($scope,$http,$state,$stateParams,$window){
	$scope.politics = function() {
		$state.go('politics')
	}
	$scope.terms = function() {
		$state.go('terms')
	}
	$scope.about = function() {
		$state.go('about')
	}

});

var AboutUsController = app.controller('AboutUsController', function($scope,$http,$state,$stateParams,$window, TextSettingsService){

$scope.about = ""
TextSettingsService.get({key: 'ABOUT_US'}, function(data){
		$scope.about = data.objects[0].value;
	})


});

var ContactController = app.controller('ContactController', function($scope,$http,$state,$stateParams,$window, TextSettingsService){

$scope.contact = ""
TextSettingsService.get({key: 'CONTACT'}, function(data){
		$scope.contact = data.objects[0].value;
	})


});

var EmploymentController = app.controller('EmploymentController', function($scope,$http,$state,$stateParams,$window, TextSettingsService){

$scope.employment = ""
TextSettingsService.get({key: 'EMPLOYMENT'}, function(data){
		$scope.employment = data.objects[0].value;
	})


});