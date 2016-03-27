app.service('changePassModal', function($modal, $rootScope, NavigationService){

	function currentuser(user) {
		return NavigationService.isAuthenticated();
	}

	return function() {
    	var instance = $modal.open({
	      templateUrl: '/static/partials/modal-cambiar-clave.html',
	      controller: 'CambiarClaveModalCtrl',
	      controllerAs: 'CambiarClaveModalCtrl',
	      size: 'md'
	    })
  };

});