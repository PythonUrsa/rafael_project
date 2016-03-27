app.controller('UserOrdersCtrl', function($scope, $state, $stateParams, NavigationService, OrderService, usSpinnerService, SettingService){

	$('body').addClass("user");
	$('body').removeClass("home");
	$('body').removeClass("search");

	$scope.goToProfile = function(){
		$state.go("profile");
	}

	$scope.goAddr = function(){
		$state.go("userAddresses");
	};

	$scope.getOrders = function(offset){
		OrderService.query({user: NavigationService.getIdentity().id, offset: offset}, function(orders){
			$scope.pages[$scope.pages.length] = orders.objects;
			$scope.totalItems = orders.meta.total_count;
			$scope.nextPage = orders.meta.next;
			$scope.orders = $scope.pages[0];
			angular.forEach(orders.objects, function(order, key){
				order.timestamp = new Date(order.timestamp).toString("dddd dd, MMMM, yyyy, h:mm tt")
				// dddd dd' de' MMMM, yyyy, h:mm tt
				order.timestamp = order.timestamp.replace(",", " de");
				// dddd dd' de' MMMM' de' yyyy, h:mm tt
				order.timestamp = order.timestamp.replace(",", " de");
				// dddd dd' de' MMMM' de' yyyy' a las' h:mm tt
				order.timestamp = order.timestamp.replace(",", " a las");
			})
			if ($scope.nextPage != null) {
				$scope.offset = $scope.nextPage.split('offset=')[1].split('&')[0];
				$scope.getOrders($scope.offset);
			};
		})
	}

	$scope.init = function(){
		$scope.pages = [];
		$scope.currentPage = 1;
		$scope.nextPage = null;
		$scope.offset = 0;
		$scope.getOrders($scope.offset);

	};

	$scope.init();

	$scope.goToDetail = function(id){
		$state.go("detail", {"restaurant": id});
	}

	$scope.goToOrder = function(id){
		$state.go('orderConfirmation', {"order": id});
	}

	$scope.pageChanged = function(){
		$scope.orders = $scope.pages[$scope.currentPage - 1];
	}


});