angular
  .module("demoApp", ["ngMaterial", "md.data.table"])

  .config([
    "$mdThemingProvider",
    function($mdThemingProvider) {
      "use strict";

      $mdThemingProvider.theme("default").primaryPalette("blue");
    }
  ])

  .controller("nutritionController", [
    "$mdEditDialog",
    "$q",
    "$scope",
    "$timeout",
    "$http",
    "$sce",
    function($mdEditDialog, $q, $scope, $timeout, $http, $sce) {
      "use strict";
      var bookmark;
      $scope.selected = [];
      $scope.limitOptions = [5, 10, 15];
      $scope.getStocks = getStocks;
      $scope.searchStocks = searchStocks;

      $scope.query = {
        order: "name",
        limit: 10,
        page: 1,
        filter: ""
      };
      $scope.highlight = function(text, search) {
        if (!search) {
          return $sce.trustAsHtml(text);
        }
        return $sce.trustAsHtml(
          text.replace(
            new RegExp(search, "gi"),
            '<span class="highlightedText">$&</span>'
          )
        );
      };

      $scope.filter = {
        options: {
          debounce: 500
        }
      };

      $scope.toggleLimitOptions = function() {
        $scope.limitOptions = $scope.limitOptions ? undefined : [5, 10, 15];
      };

      activate();

      // Methods
      function activate() {
        var promises = [getStocks()];
        return $q.all(promises);
      }

      function searchStocks(query) {
        if (query) {
          $scope.promise = $http
            .get("/stocks/search", {
              params: { q: query }
            })
            .then(function(data) {
              $scope.stocks = data;
            });
        }
      }

      function getStocks() {
        $scope.promise = $http.get("/stocks").then(function(data) {
          $scope.stocks = data;
        });
      }

      $scope.removeFilter = function() {
        $scope.filter.show = false;
        $scope.query.filter = "";

        if ($scope.filter.form.$dirty) {
          $scope.filter.form.$setPristine();
        }
        getStocks();
      };

      $scope.$watch("query.filter", function(newValue, oldValue) {
        if (!oldValue) {
          bookmark = $scope.query.page;
        }

        if (newValue !== oldValue) {
          $scope.query.page = 1;
        }

        if (!newValue) {
          $scope.query.page = bookmark;
        }
        if (newValue || oldValue) {
          $scope.searchStocks($scope.query.filter);
        }
      });
    }
  ]);
