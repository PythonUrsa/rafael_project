angular.module('appRestaurant').factory('RestaurantNavigationService', function($q , $http, $timeout, $window){
  var user_auth_api_url = '/user/api/restaurant_login/'
  var user_logout_api_url = '/user/api/user_logout/'

  var current_restaurant = []

  var _identity = undefined;
  var _authenticated = false;
  function init() {
        if ($window.localStorage["RestaurantUserInfo"]){
            _identity = JSON.parse($window.localStorage["RestaurantUserInfo"]);
            _authenticated = true;
            
        }else{
            
        }
    }
  init();

  return {
        setRestaurant: function(object){
          restaurant = object
        },
        getRestaurant: function(){
          return restaurant
        },
        getIdentity: function() {
          return _identity
        },
        isIdentityResolved: function() {
        return angular.isDefined(_identity);
        },
        isAuthenticated: function() {
          return _authenticated;
        },
        isInRole: function(role) {
          if (!_authenticated || !_identity.roles) return false;

          return _identity.roles.indexOf(role) != -1;
        },
        isInAnyRole: function(roles) {
          if (!_authenticated || !_identity.roles) return false;

          for (var i = 0; i < roles.length; i++) {
            if (this.isInRole(roles[i])) return true;
          }

          return false;
        },
        logout: function() {
          var deferred = $q.defer();

            $http.get(user_logout_api_url)
            .success(function(data, status){
              _identity = undefined
              _authenticated = false
              delete $window.localStorage["RestaurantUserInfo"];
              deferred.resolve(true);
            })
            .error(function(data, status){
              _identity = undefined
              _authenticated = false
              delete $window.localStorage["RestaurantUserInfo"];
              deferred.resolve(true);
            })
            return deferred.promise

        },
        authenticate: function(credentials) {
          //_identity = identity;
          //_authenticated = identity != null;
            var deferred = $q.defer();

             if (angular.isDefined(_identity) && $window.localStorage["RestaurantUserInfo"]) {
                deferred.resolve(_identity);
                return deferred.promise;
            }else{
                $http.post(user_auth_api_url, credentials)
                .success(function(data, status){
                  _identity = data
                  _authenticated = true
                  $window.localStorage["RestaurantUserInfo"] = JSON.stringify(data);
                  deferred.resolve(data);
                })
                .error(function(data, status){
                  _identity = undefined;
                  _authenticated = false;
                  deferred.reject(status);
                })
                return deferred.promise
            }
          },
          checkPassword: function(credentials) {
            var deferred = $q.defer();

            $http.post(user_auth_api_url, credentials)
            .success(function(data, status){
              deferred.resolve(data);
            })
            .error(function(data, status){
              deferred.reject(status);
            })
            return deferred.promise
          },
        /*
        identity: function(force) {
          var deferred = $q.defer();

          if (force === true) _identity = undefined;

          // check and see if we have retrieved the identity data from the server. if we have, reuse it by immediately resolving
          if (angular.isDefined(_identity)) {
            deferred.resolve(_identity);

            return deferred.promise;
          }

          // otherwise, retrieve the identity data from the server, update the identity object, and then resolve.
                             $http.post(user_auth_api_url, { ignoreErrors: true })
                                  .success(function(data) {
                                      _identity = data;
                                      _authenticated = true;
                                      deferred.resolve(_identity);
                                  })
                                  .error(function () {
                                      _identity = null;
                                      _authenticated = false;
                                      deferred.resolve(_identity);
                                  });

          // for the sake of the demo, fake the lookup by using a timeout to create a valid
          // fake identity. in reality,  you'll want something more like the $http request
          // commented out above. in this example, we fake looking up to find the user is
          // not logged in
          

          return deferred.promise;
        }*/
      };
});