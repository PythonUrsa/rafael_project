angular.module('app').factory('RestaurantService', function($resource){
	var restaurant_api_url = '/api/v1/restaurant/'

	return $resource( restaurant_api_url + ':id/', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('app').factory('CityService', function($resource){
	var city_api_url = '/api/v1/city/'

	return $resource( city_api_url + ':id/', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('app').factory('PaymentMethodService', function($resource){
    var payment_api_url = '/api/v1/payment/'

    return $resource( payment_api_url + ':id/', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('app').factory('ZoneService', function($resource){
	var zone_api_url = '/api/v1/zone/'

	return $resource( zone_api_url + ':id/', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('app').factory('FoodTypeService', function($resource){
	var food_type_api_url = '/api/v1/food_type/'

	return $resource( food_type_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('app').factory('CategoryService', function($resource){
	var category_api_url = '/api/v1/category/'

	return $resource( category_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('app').factory('ItemService', function($resource){
	var item_api_url = '/api/v1/item/'

	return $resource( item_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('app').factory('SettingService', function($resource){
	var setting_api_url = '/api/v1/setting/'

	return $resource( setting_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('app').factory('ScheduleService', function($resource){
	var schedule_api_url = '/api/v1/schedule/'

	return $resource( schedule_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});


});


angular.module('app').factory('PhotoService', function($resource){
	var photo_api_url = '/api/v1/photo/'

	return $resource( photo_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('app').factory('SelectableTypeService', function($resource){
	var select_type_api_url = '/api/v1/selectable_type/'

	return $resource( select_type_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('app').factory('SelectableService', function($resource){
	var select_api_url = '/api/v1/selectable/'

	return $resource( select_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});


});


angular.module('app').factory('ExtraService', function($resource){
	var extra_api_url = '/api/v1/extra/'

	return $resource( extra_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('app').factory('FEUserService', function($resource){
	var user_api_url = '/api/v1/auth/user/'

	return $resource( user_api_url + ':id/', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('app').factory('UpdateUser', function($q , $http){
  var user_api_url = '/api/v1/auth/user/'

  return {
  			updateFTEUser: function(form_data, file, callback){
            //var url = '/api/v1/entity/';
            var fd = new FormData();
            for ( var name in form_data ) {
                if ( !form_data.hasOwnProperty( name ) ) {
                    continue;
                }
                var value = form_data[name];
                if(value != null)
                {
                    fd.append(name, form_data[name]);
                }
            }
            fd.append('photo', file);
            $http({
                    url: user_api_url,
                    data: fd,
                    method: 'POST',
                    transformRequest: angular.identity,
                    headers : {'Content-Type': undefined}
                    //headers : {'X-CSRFToken':get_csrftoken(), 'Content-Type': undefined}
                })
                .success(callback)
                .error(function(data, status, headers, config) {
                    // pass
                    });
        	},
        }
});



angular.module('app').factory('RegisterUser', function($q , $http){
  var user_api_url = '/api/v1/create_user/'

  return {
  			registerFTEUser: function(form_data, file, callback){
            //var url = '/api/v1/entity/';
            var fd = new FormData();
            for ( var name in form_data ) {
                if ( !form_data.hasOwnProperty( name ) ) {
                    continue;
                }
                var value = form_data[name];
                if(value != null)
                {
                    fd.append(name, form_data[name]);
                }
            }
            fd.append('photo', file);
            $http({
                    url: user_api_url,
                    data: fd,
                    method: 'POST',
                    transformRequest: angular.identity,
                    headers : {'Content-Type': undefined}
                    //headers : {'X-CSRFToken':get_csrftoken(), 'Content-Type': undefined}
                })
                .success(callback)
                .error(function(data, status, headers, config) {
                    // pass
                    });
        	},
        }
});





angular.module('app').factory('RNCUserService', function($resource){
	var rnc_user_api_url = '/api/v1/user/rnc/'

	return $resource( rnc_user_api_url + ':id/', {}, { 'query': {method: 'GET', isArray: false }, 'delete': { method: 'DELETE'}, 'update': { method: 'PUT'} },{});


});


angular.module('app').factory('AddressUserService', function($resource){
	var address_user_api_url = '/api/v1/user/address/'

	return $resource( address_user_api_url + ':id/', {},/* {headers: { 'Content-Type': 'application/json' }} ,*/ {'query': {method: 'GET', isArray: false }, 'update': { method: 'PATCH'}});


});

angular.module('app').factory('OrderService', function($resource){
	var order_api_url = '/api/v1/order/'

	return $resource( order_api_url + ':id/', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('app').factory('ItemOrderService', function($resource){
	var item_order_api_url = '/api/v1/order_item/'

	return $resource( item_order_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('app').factory('TextSettingsService', function($resource){
	var text_setting_api_url = '/api/v1/text_setting/'

	return $resource( text_setting_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});

});




