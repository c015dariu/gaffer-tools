'use strict'

angular.module('app').component('graphView', graphView())

function graphView() {

    return {
        templateUrl: 'app/graph/graph.html',
        controller: GraphController,
        controllerAs: 'ctrl'
    }
}


function GraphController($scope, graph, results) {

    var vm = this

    vm.selectedEdges = graph.selectedEdges
    vm.selectedEntities = graph.selectedEntities
    vm.selectedEntitiesCount = Object.keys(graph.selectedEntities).length
    vm.selectedEdgesCount = Object.keys(graph.selectedEdges).length

    results.observeResults().then(null, null, function(results) {
        graph.update(results)
    })

    graph.onSelectedElementsUpdate(function(selectedElements) {
        vm.selectedEdgesCount = Object.keys(selectedElements.edges).length
        vm.selectedEntitiesCount = Object.keys(selectedElements.entities).length
        vm.selectedEdges = selectedElements.edges
        vm.selectedEntities = selectedElements.entities
        $scope.$apply()
    })

    graph.reload(results.results)



}