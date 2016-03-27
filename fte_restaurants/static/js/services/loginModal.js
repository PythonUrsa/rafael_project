app.service('loginModal', function($modal, $rootScope, NavigationService){

	function currentuser(user) {
		return NavigationService.isAuthenticated();
	}

	return function() {
    	var instance = $modal.open({
	      templateUrl: '/static/partials/modal_login.html',
	      controller: 'LoginModalCtrl',
	      controllerAs: 'LoginModalCtrl',
	      size: 'sm'
	    })
	    return instance.result.then(currentuser);
  };

});