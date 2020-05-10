var application = angular.module("PhysicsTerminology", ["ngRoute", "ngSanitize"]);

application.config(function ($routeProvider) {
    $routeProvider
        .when("/", { templateUrl: "search.html", controller: "SearchController" });
});

application.directive("mathematics", function () {
    return {
        restrict: "E",
        link: function (scope, element, attributes) {
            var contentType = attributes.contentType;
            var content = attributes.content;
            if (typeof (katex) === "undefined") {
                require(["katex"], function (katex) {
                    katex.render(content, element[0]);
                });
            }
            else {
                katex.render(content, element[0]);
            }
        }
    }
});

application.directive("compile", ["$compile", function ($compile) {
    return function (scope, element, attributes) {
        scope.$watch(function (scope) {
            return scope.$eval(attributes.compile);
        }, function (value) {
            element.html(value);
            $compile(element.contents())(scope);
        });
    };
}]);

class Database {
    constructor(data) {
        this._data = data;
    }
}

application.factory("dataService", ["$http", function ($http) {
    var dataService = {
        data: null,
        database: null,
        getData: function () {
            var that = this;

            if (this.database != null) {
                return new Promise(function (resolve, reject) { return resolve(that.database); });
            }

            return $http.get("terminology.json").then(function (response) {
                that.data = response.data;
                that.database = new Database(that.data);

                return that.database;
            });
        }
    };

    return dataService;
}]);


application.controller("SearchController", ["$scope", "dataService", "$location", function SearchController($scope, dataService, $location) {

    dataService.getData().then(function (database) {
        $scope.terms = database._data.Terms;
    });

}]);