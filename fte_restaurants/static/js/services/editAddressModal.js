app.service('editAddressModal', function($modal, $rootScope, NavigationService){

	function currentuser(user) {
		return NavigationService.isAuthenticated();
	}


	return function(scope, index) {
    	var instance = $modal.open({
	      templateUrl: '/static/partials/modal-editar-direccion.html',
	      controller: 'EditAddressModalCtrl',
	      controllerAs: 'EditAddressModalCtrl',
	      size: 'lg',
	      resolve: {
	      	addresses: function(){
	      		return scope.addresses;
	      	},
	      	selectedAddr: function(){
	      		return scope.selectedAddr;
	      	}
	      }
	    })
  };

});