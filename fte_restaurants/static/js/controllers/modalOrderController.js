app.controller('ModelOrderController', function($scope,$filter, $state, $stateParams,$timeout,$modal,$modalInstance, RestaurantService, complete_item ,edit_order, selectables_associated){

	$scope.error = false
  $scope.error_text = ''


	$scope.init = function() {
		$scope.item = complete_item;
		if (edit_order == null){
			$scope.order = {
		  		  'item': $scope.item,
		  		  'quantity': 1,
		  		  'extras': $scope.item.extra_types,
		  		  'selectables_associated': selectables_associated,
		  		  'extra_info': '',
		  		  'total_item':$scope.item.price,
  			}
		}else{
			$scope.order = eval('(' + JSON.stringify(edit_order) + ')');
      angular.forEach($scope.order.extras, function(value, type_key){
        angular.forEach(value.types, function(extra, key){
              $scope.item.extra_types[type_key].types[key].selected = extra.selected;
        });
      });
      $scope.order.extras = $scope.item.extra_types;
		}
	}
    
  	$scope.init()
    $scope.detail = $scope.order.item.name + "(" + $scope.order.total_item + ")x" + ($scope.order.quantity)
    
  	$scope.$watch('order', function (newValue, oldValue) {
  		if (newValue == oldValue) {return;}
  		$scope.order.total_item = (function(){
          $scope.detail = $scope.order.item.name;
          total_price = parseInt($scope.order.item.price, 10) * $scope.order.quantity
          angular.forEach($scope.order.extras, function(value, key){
            angular.forEach(value.types, function(extra, key){
              if(extra.selected == true){
                total_price += parseInt(extra.price, 10)
                $scope.detail += "(" + extra.name + ")";
              } else {
                extra.selected = false;
              }
            })
          })
          var selectable = {};
          angular.forEach($scope.order.selectables_associated, function(value, key){
            selectable = $scope.item.selectable_types[key].types[value];
            if(selectable.price != null){
              total_price += parseInt(selectable.price, 10)
            }
            $scope.detail += "(" + selectable.name + ")";
          })
          if ($scope.order.extra_info != "") {
            $scope.detail += "(" + $scope.order.extra_info + ")";
          };
          return total_price
      })()
      $scope.detail += "(" + $scope.order.total_item + ")x" + ($scope.order.quantity);
  	}, true);

  	$scope.cancel = function () {
    	$modalInstance.dismiss('cancel');
  	};

  	$scope.ok = function () {
      if ($scope.order.selectables_associated.length < complete_item.selectable_types.length){
          $scope.error = true
          $scope.error_text = "Debe completar todos los seleccionables"
          return
      }

  		if(edit_order == null){
  			$scope.order.new = true
  			$modalInstance.close($scope.order);	
  		}else{
  			$scope.order.new = false
        for (var prop in edit_order){
          edit_order[prop] = $scope.order[prop];
        }
  			$modalInstance.close($scope.order, false);
  		}
    	
  	};
});