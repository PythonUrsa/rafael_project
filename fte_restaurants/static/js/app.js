var app = angular.module('app', ['ui.router', 'ui.bootstrap', 'ngResource','ngCookies','angucomplete-alt', 'angularSpinner', 'uiGmapgoogle-maps', 'imageupload', 'ngSanitize', 'socialLinks']);

app.constant('urls', {
  "password_reset": "http://127.0.0.1:8000/user/reset/"
})

app.config( function( $httpProvider, $stateProvider, $urlRouterProvider){
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  

  $stateProvider
    .state('home', {
      url: '/',           
      controller: "HomeController",
      templateUrl: 'static/partials/home.html',
      authenicate: false,
    })
    .state('politics', {
      url: '/politics',
      controller: "PoliticsController",
      templateUrl: 'static/partials/politics.html',
      authenicate: false,
    })
    .state('terms', {
      url: '/terms',
      controller: "TermsController",
      templateUrl: 'static/partials/terms.html',
      authenicate: false,
    })
    .state('about', {
      url: '/about',
      controller: "AboutUsController",
      templateUrl: 'static/partials/about.html',
      authenicate: false,
    })
    .state('contact', {
      url: '/contact',
      controller: "ContactController",
      templateUrl: 'static/partials/contact.html',
      authenicate: false,
    })
    .state('employment', {
      url: '/employment',
      controller: "EmploymentController",
      templateUrl: 'static/partials/employment.html',
      authenicate: false,
    })
    .state('search', {
      url: '/search/?zones&city&preference',           
      controller: "SearchController",
      templateUrl: 'static/partials/search.html',
      authenicate: false,
    })
    .state('detail', {
      url: '/detail/?restaurant',           
      controller: "DetailController",
      templateUrl: 'static/partials/detail.html',
      authenicate: false,
    })
    .state('check_order', {
      url: '/check_order/',           
      controller: "CheckOrderController",
      templateUrl: 'static/partials/check_order.html',
      authenicate: true,
    })
    .state('register', {
      url: '/register',           
      controller: "RegisterCtrl",
      templateUrl: 'static/partials/register.html',
      authenicate: false,
    })
    .state('profile', {
      url: '/perfil/',           
      controller: "UserProfileCtrl",
      templateUrl: 'static/partials/user-perfil.html',
      authenicate: true,  
    })
    .state('profileEdit', {
      url: '/perfil/edit/',
      controller: "UserProfileEditCtrl",
      templateUrl: 'static/partials/user-perfil-edit.html',
      authenicate: true,
    })
    .state('userAddresses', {
      url: '/perfil/edit/mis-direcciones/',
      controller: "UserAddressesCtrl",
      templateUrl: 'static/partials/user-mis-direcciones.html',
      authenicate: true,
    })
    .state('userOrders', {
      url: '/perfil/mis-ordenes/',
      controller: "UserOrdersCtrl",
      templateUrl: 'static/partials/user-mis-pedidos.html',
      authenicate: true,
    })
    .state('orderConfirmation', {
      url: '/order_confirmation/?order',
      controller: "ConfirmationCtrl",
      templateUrl: 'static/partials/orden-confirmacion.html',
      authenicate: true,
    })
    
    $urlRouterProvider.otherwise('/');
});

app.config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);


/*app.config(['$httpProvider', function ($httpProvider) {

  $httpProvider.interceptors.push(function ($timeout, $q, $injector) {
    var loginModal, $http, $state;

    // this trick must be done so that we don't receive
    // `Uncaught Error: [$injector:cdep] Circular dependency found`
    $timeout(function () {
      loginModal = $injector.get('loginModal');
      $http = $injector.get('$http');
      $state = $injector.get('$state');
    });

    return {
      responseError: function (rejection) {
        if (rejection.status !== 401) {
          return rejection;
        }

        var deferred = $q.defer();

        loginModal()
          .then(function () {
            deferred.resolve( $http(rejection.config) );
          })
          .catch(function () {
            $state.go('home');
            deferred.reject(rejection);
          });
        

        return deferred.promise;
      }
    };
   }); 
  }]);*/



app.run(function( $rootScope, $location,$state ,$http, $cookies, NavigationService, loginModal) {
  //$http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
  // enumerate routes that don't need authentication

  $rootScope.$on('$stateChangeStart', function (event, to, toParams, from, fromParams) {
    
    if (to.authenicate && !NavigationService.isAuthenticated()) { 
      event.preventDefault();
      loginModal()
              .then(function() {
                  
                  return $state.go(to.name, toParams)
              })
              .catch(function () {
                  
                  return true;
              });
    }
  });
});



