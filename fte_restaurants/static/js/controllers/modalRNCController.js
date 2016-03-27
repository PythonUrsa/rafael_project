app.controller('ModalRNCController', function($scope,$filter, $state, $stateParams,$timeout,$modal,$modalInstance, RNCUserService, user){

	$scope.update_rncs = function() {
		RNCUserService.get({frontend_user:user.id}, function(rncs){
		$scope.rncs = rncs.objects
		})
	}
	$scope.cancel = function () {
    	$modalInstance.close('cancel');
  	};

	$scope.update_rncs()
	$scope.show_add_button= true
	$scope.editable_rnc = ''
	$scope.submit_error = '';

	$scope.new_rnc = {
		"rnc_number": '',
		"description": '',
	}

	$scope.clear_input_fields = function(){
		$scope.new_rnc.rnc_number = ''
		$scope.new_rnc.description = ''
		$scope.rnc_form.$setUntouched();
	}

	$scope.isNumber = function () {
		if (isNaN($scope.new_rnc.rnc_number)){
			$scope.rnc_form.rnc_number.$error.number = true;
			$scope.rnc_form.rnc_number.$validate();
			$scope.rnc_form.$invalid = true;
		} else {
			delete $scope.rnc_form.rnc_number.$error.number
			$scope.rnc_form.rnc_number.$validate();
		}
	}

	$scope.delete = function(rnc){
		RNCUserService.delete({ id: rnc.id  },function(data, headers){
			$scope.update_rncs()
		}, function(error){
			// pass
		})
	}

	$scope.load = function(rnc){
		$scope.show_add_button = false
		$scope.editable_rnc = rnc
		$scope.new_rnc.rnc_number = rnc.rnc_number
		$scope.new_rnc.description = rnc.description
	}

	$scope.edit = function(){
		RNCUserService.update({ id: $scope.editable_rnc.id  },$scope.new_rnc,function(data, headers){
			if (data.error) {
				$scope.rnc_form.rnc_number.$error.number = true;
				$scope.rnc_form.rnc_number.$validate();
				$scope.rnc_form.$invalid = true;
			} else {
				$scope.update_rncs()
				$scope.editable_rnc = ''
				$scope.show_add_button = true
				$scope.clear_input_fields()
			}
		}, function(error){
			$scope.editable_rnc = ''
			$scope.show_add_button = true
			$scope.clear_input_fields()
		})
	}

	$scope.set_main = function(id){
		RNCUserService.update({ id: id  },{'main': true},function(data, headers){
			$scope.update_rncs()
			
		}, function(error){
			// pass			
		})
	}

	$scope.add = function(){
		var new_rnc = new RNCUserService($scope.new_rnc)
		new_rnc.frontend_user = user.resource_uri
		new_rnc.$save(function(data,headers) {
			if (data.error) {
				$scope.submit_error = data.error.message;
				$scope.rnc_form.rnc_number.$error.number = true;
				$scope.rnc_form.rnc_number.$validate();
				$scope.rnc_form.$invalid = true;
			} else {
				$scope.update_rncs()
				$scope.clear_input_fields()
			}

		}, function (error) {
			// pass
		});
		
	}

});