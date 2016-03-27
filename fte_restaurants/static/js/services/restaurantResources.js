angular.module('appRestaurant').factory('RestaurantService', function($resource){
	var restaurant_api_url = '/api/v1/restaurant/'

	return $resource( restaurant_api_url + ':id/', {}, {'query': {method: 'GET', isArray: false },
		'update': { method: 'PATCH'}});


});

angular.module('appRestaurant').factory('CityService', function($resource){
	var city_api_url = '/api/v1/city/'

	return $resource( city_api_url + ':id/', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('appRestaurant').factory('PaymentMethodService', function($resource){
	var payment_api_url = '/api/v1/payment/'

	return $resource( payment_api_url + ':id/', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('appRestaurant').factory('ZoneService', function($resource){
	var zone_api_url = '/api/v1/zone/'

	return $resource( zone_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('appRestaurant').factory('FoodTypeService', function($resource){
	var food_type_api_url = '/api/v1/food_type/'

	return $resource( food_type_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('appRestaurant').factory('CategoryService', function($resource){
	var category_api_url = '/api/v1/category/'

	return $resource( category_api_url + ':id/', {}, { 'query': {method: 'GET', isArray: false },
		'update': { method: 'PUT'} },{});


});

angular.module('appRestaurant').factory('ItemService', function($resource){
	var item_api_url = '/api/v1/item/'

	return $resource( item_api_url + ':id/', {}, { 'query': {method: 'GET', isArray: false }, 'update': { method: 'PATCH'} },{});

});

angular.module('appRestaurant').factory('SettingService', function($resource){
	var setting_api_url = '/api/v1/setting/'

	return $resource( setting_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('appRestaurant').factory('ScheduleService', function($resource){
	var schedule_api_url = '/api/v1/schedule/'

	return $resource( schedule_api_url + ':id/', {}, {'query': {method: 'GET', isArray: false },
		'update': { method: 'PATCH'},
		'delete': { method: 'DELETE'}});


});

angular.module('appRestaurant').factory('TelephoneService', function($resource){
	var telephone_api_url = '/api/v1/telephone/'

	return $resource( telephone_api_url + ':id/', {}, {'query': {method: 'GET', isArray: false },
		'update': { method: 'PATCH'},
		'delete': { method: 'DELETE'}},{});


});


angular.module('appRestaurant').factory('PhotoService', function($resource){
	var photo_api_url = '/api/v1/photo/'

	return $resource( photo_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('appRestaurant').factory('SelectableTypeService', function($resource){
	var select_type_api_url = '/api/v1/selectable_type/'

	return $resource( select_type_api_url + ':id/', {}, {
		'query': {method: 'GET', isArray: false },
		'update': { method: 'PATCH'},
		'delete': { method: 'DELETE'}});


});

angular.module('appRestaurant').factory('SelectableService', function($resource){
	var select_api_url = '/api/v1/selectable/'

	return $resource( select_api_url + ':id/', {}, {
		'query': {method: 'GET', isArray: false },
		'update': { method: 'PATCH'},
		'delete': { method: 'DELETE'}});


});


angular.module('appRestaurant').factory('ExtraTypeService', function($resource){
	var extra_api_url = '/api/v1/extra_type/'

	return $resource( extra_api_url + ':id/', {}, {
		'query': {method: 'GET', isArray: false },
		'update': { method: 'PATCH'},
		'delete': { method: 'DELETE'} });


});

angular.module('appRestaurant').factory('ExtraService', function($resource){
	var extra_api_url = '/api/v1/extra/'

	return $resource( extra_api_url + ':id/', {}, {
		'query': {method: 'GET', isArray: false },
		'update': { method: 'PATCH'},
		'delete': { method: 'DELETE'}});


});

angular.module('appRestaurant').factory('OrderService', function($resource){
	var order_api_url = '/api/v1/order/'

	return $resource( order_api_url + ':id/', {}, {'query': {method: 'GET', isArray: false }, 'update': { method: 'PATCH'}});


});

angular.module('appRestaurant').factory('ItemOrderService', function($resource){
	var item_order_api_url = '/api/v1/order_item/'

	return $resource( item_order_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});


});

angular.module('appRestaurant').factory('TextSettingsService', function($resource){
	var text_setting_api_url = '/api/v1/text_setting/'

	return $resource( text_setting_api_url + ':id', {}, {'query': {method: 'GET', isArray: false }});

});


