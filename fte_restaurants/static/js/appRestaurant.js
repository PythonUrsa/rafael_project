var appRestaurant = angular.module('appRestaurant', ['ui.router', 'ui.bootstrap', 'ngResource','ngCookies','angucomplete-alt', 'angularSpinner', 'uiGmapgoogle-maps', 'ngSanitize']);

appRestaurant.constant('urls', {
  "password_reset": "http://127.0.0.1:8000/user/reset/"
})

appRestaurant.config( function( $httpProvider, $stateProvider, $urlRouterProvider){
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  

  $stateProvider
    .state('home', {
      url: '/',
      controller: "RestaurantLoginCtrl",
      templateUrl: '/static/partials/user-login.html',
      authenicate: false,
    })
    .state('restaurant', {
      url: '/edit',
      controller: "RestaurantEditCtrl",
      templateUrl: '/static/partials/user-edit-menu.html',
      authenicate: true,
    })
    .state('about', {
      url: '/about',           
      controller: "AboutUsController",
      templateUrl: '/static/partials/about.html',
      authenicate: false,
    })
    .state('contact', {
      url: '/contact',
      controller: "ContactController",
      templateUrl: '/static/partials/contact.html',
      authenicate: false,
    })
    .state('employment', {
      url: '/employment',
      controller: "EmploymentController",
      templateUrl: '/static/partials/employment.html',
      authenicate: false,
    })
    
    $urlRouterProvider.otherwise('/');
});

appRestaurant.config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

appRestaurant.config(function ($httpProvider) {

  $httpProvider.interceptors.push(function ($timeout, $q, $injector) {
    var $http, $state;

    // this trick must be done so that we don't receive
    // `Uncaught Error: [$injector:cdep] Circular dependency found`
    $timeout(function () {
      $http = $injector.get('$http');
      $state = $injector.get('$state');
    });

    return {
      responseError: function (rejection) {
        if (rejection.status !== 401) {
          return rejection;
        }
          $state.go('home');
        }
    };
  });

});

appRestaurant.run(function( $rootScope, $location,$state ,$http, $cookies, RestaurantNavigationService) {
  //$http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
  // enumerate routes that don't need authentication

  $rootScope.$on('$stateChangeStart', function (event, to, toParams, from, fromParams) {
    if (to.authenicate && !RestaurantNavigationService.isAuthenticated()) { 
        event.preventDefault();
        return $state.go('home')
    }else{
        return;
    }

  });
});



