/* Controllers */
var dmhyBotCtrls = angular.module('dmhyBotCtrls', ['ngCookies', 'ui.bootstrap']);

dmhyBotCtrls.run(function($http){
    $http.defaults.xsrfCookieName = 'csrftoken';//auto get the value of 'csrftoken' in the cookie
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';//auto add csrf token into the post header 
});

dmhyBotCtrls.service('verificateService', function($http){
    var isLogin = false;
    var login= function( user ){
        var login_data = {'username':user.username, 'password':user.password};
        $http.post('/dmhy/login/', angular.toJson( login_data )).
        success(function( data ){
            if( data['status'] == true ){
                isLogin = true;
            }else{
                isLogin = false;
            }
        }).
        error(function(){});
    };
    var logout= function(){
        request = $http.get('/dmhy/logout');
        isLogin = false;
    };

    return {
        login: login,
        logout: logout,
        isLogined: function(){ return isLogin; }
    };
});

dmhyBotCtrls.controller('homeCtrl', ['$scope', '$http',
    function($scope, $http) {
        $scope.reverse = true;
        $scope.column  = 'last_update';
        $scope.tasks = { "tasklist":[] };
        $http.get('/dmhy/api/tasklist/').
        success(function( data, status, header, config ){
            if( status == 200 ){
                $scope.tasks = data['tasklist'];
                angular.forEach( data['tasklist'], function( val, idx ){
                    $scope.tasks[idx]['last_update'] = val['last_update'].substr(0,19);
                });
            }
        }).
        error( function( data, status, header, config ){
            $scope.tasks = { "error": status, "tasklist":[] };
        }); 
    }]);

dmhyBotCtrls.controller('historyCtrl', ['$scope','$http',
    function($scope, $http) {
        $http.get('/dmhy/api/history/').
        success( function( data, status, header, config){
            $scope.records = data;
            angular.forEach( data, function( val, idx ){
                $scope.records[idx]['date'] = val['date'].substr(0,19);
            });
        }).
        error( function( data, status, header, config){
    
        });
        
}]);

dmhyBotCtrls.controller('searchingCtrl', ['$scope', '$http',
    function( $scope, $http ){
        $scope.keywords = '';
        $scope.result = {};
        $scope.addTask = true;
        $scope.sendKeyword = function(k){
            request = $http.get('/dmhy/api/search/',{ "params":{ "keyword":k }});
            request.success(function( data ){
                $scope.result = data;
            });
            request.error(function(e){
                $scope.result = "An error occured <br>" + e;
            });

        };
        $scope.addToQueue = function( alias, keywords ){
            $http.post('/dmhy/api/tasklist/', angular.toJson({"alias":alias,"keywords":keywords}) )
            .success(function(data){
                $scope.addTask = true;
            })
            .error(function(){});
        };
}]);

dmhyBotCtrls.controller('loginCtrl', ['$scope', '$http', '$location', '$cookies', 'verificateService',
    function( $scope, $http, $location, $cookies, verificateService){
        $scope.user={};
        $scope.user.username = $scope.user.password = '';           
        $scope.login = function( user ){
            verificateService.login( user );
        };
}]);

dmhyBotCtrls.controller('logoutCtrl', ['$scope', '$http', '$location', 'verificateService',
    function( $scope, $http, $location, verificateService){
        verificateService.logout();
        $location.path('/home').replace();
}]);

dmhyBotCtrls.controller('navCtrl', ['$scope', '$location', 'verificateService',
    function($scope, $location, verificateService ){
        $scope.navbarActive = function(nowPage){
            path = $location.path().substr(1);
            if( nowPage == path  )return 'active';
            else return '';
        };
        $scope.isLogined = function(){
            return verificateService.isLogined();
        };
}]);
    
