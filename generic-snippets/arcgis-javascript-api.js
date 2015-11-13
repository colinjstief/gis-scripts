/*

Snippets for ArcGIS online

*/

/*********************/
/*********************/
// Styles
/*********************/
/*********************/

require([
	"esri/symbols/SimpleLineSymbol", "esri/symbols/SimpleFillSymbol"
], function(
	SimpleLineSymbol, SimpleFillSymbol
){...}

var parcel_yellow;

parcel_yellow = new SimpleFillSymbol(
  SimpleFillSymbol.STYLE_SOLID,
  new SimpleLineSymbol(
	SimpleLineSymbol.STYLE_SOLID,
	new Color([225,255,150,1]),
	1.25
  ),
  new Color([0,0,0,0])
);

/*********************/
/*********************/
// Map
/*********************/
/*********************/

require([
	"esri/map"
], function(
	Map
){...}

var map;

map = new Map("mapDiv", {
	basemap: "hybrid",
	center: [-77.5, 37.53],
	zoom: 10
});

/* For window resizing */

$(document).ready(function() {

	// First time
	var viewer_height = $(window).height();
	var map_height = viewer_height - $(".header").height();
	var map_height_string = map_height.toString() + "px";
	$("#mapDiv").css("height", map_height_string);
	
	// On user resize
	$( window ).resize(function() {
		var viewer_height = $(window).height();
		var map_height = viewer_height - $(".header").height();
		var map_height_string = map_height.toString() + "px";
		$("#mapDiv").css("height", map_height_string);
	});
	
});

/*********************/
/*********************/
// Layers
/*********************/
/*********************/

require([
	"esri/layers/ArcGISDynamicMapServiceLayer", "esri/layers/FeatureLayer",
	"esri/InfoTemplate"
], function(
	ArcGISDynamicMapServiceLayer, FeatureLayer,
	InfoTemplate
){...}

var layer;
layer = new esri.layers.FeatureLayer("http://.../MapServer/0", {
	outFields: ["*"]
});

// With info template
var layerInfoTemplate = new InfoTemplate();
layerInfoTemplate.setTitle("<b>My title</b>");
layerInfoTemplate.setContent("Density: ${density_field}<br/>" +
							 "Force: ${force_field}");
var anotherLayer;
anotherLayer = new esri.layers.FeatureLayer("http://.../MapServer/1", {
	outFields: ["*"],
	infoTemplate: layerInfoTemplate
});

map.addLayers([layer, anotherLayer]); // Required for legend update to work properly

/* For switcher */
/*
<li class="list-group-item">
	<span>First Layer</span>
	<input id="first_layer" type="checkbox" class="Toggle" />
</li>
*/

$("input#first_layer").change(function(){
	if ($(this).is(':checked')) {
		layer.show();
	} else {
		layer.hide();
	}
});

						 
/*********************/
/*********************/
// Legend
/*********************/
/*********************/

require([
	"esri/dijit/Legend",
	"dojo/_base/array"
], function(
	Legend,
	arrayUtils
){...}

map.on("layers-add-result", function (evt) {
	
	var legendDijit;
	
	var layerInfo = arrayUtils.map(evt.layers, function (layer, index) {
	  return {layer:layer.layer, title:layer.layer.name};
	});
	if (layerInfo.length > 0) {
	  legendDijit = new Legend({
		map: map,
		layerInfos: layerInfo
	  }, "legendDiv");
	  legendDijit.startup();
	}
	
 });

/*********************/
/*********************/
// Queries
/*********************/
/*********************/

var queryLayer;
var query;

queryLayer = new esri.tasks.QueryTask("http://...MapServer/0");
query = new esri.tasks.Query();
query.returnGeometry = true;
query.outFields = ["*"];
query.spatialRelationship = esri.tasks.Query.SPATIAL_REL_INTERSECTS;

/* On map click */
var mapClick;
var mapClickHandler;

mapClick = function(evt) {
	query.geometry = evt.mapPoint;
    queryLayer.execute(query, resultsFunction);
}


/* 
Handling results from:
(a) Map click --> feature = results.features[0]
(b) Search (Which runs a query and selects a single feature) --> feature = results
(c) I forget --> feature = results.result.feature
*/
var resultsFunction;
resultsFunction = function localResultsFunction(results) {

	if (results.result) {
		feature = results.result.feature;
	} else if (results.features) {
		feature = results.features[0];
	} else {
		feature = results;
	}
	
	if (feature) {
	
		map.graphics.clear();
		
		feature.setSymbol(highlight);
		map.graphics.add(feature);
		
		var parcelExtent = feature.geometry.getExtent().expand(2.5);
        map.setExtent(parcelExtent);
		
	}
}

/*********************/
/*********************/
// Filter
/*********************/
/*********************/

var sql = "";
			
if ($("#user_value").val() == "") {
	sql += "user_value_field >= 0";
} else {
	sql += "user_value_field >= " + $("#user_value").val();
}

if ($("#another_value").val() == "") {
	sql += " AND another_value_field <= 10000";
} else {
	sql += " AND another_value_field <= " + $("#another_value").val();
}

if ($('input.toggle').is(':checked')) {
	sql += " AND toggle_field = 'Yes'";
}

if ($('input.another_toggle').is(':checked')) {
	sql += " AND another_toggle_field = 'Yes'";
}

var filterQuery;
filterQuery = new esri.tasks.Query();

layer.queryCount(filterQuery, function(results) {
	if (features >= 1000) {
		// Too many results
	} else if (features > 0 && features < 1000) {
		layer.queryFeatures(filterQuery, function(results){
			
		});
	} else {
		// No results
	}
}

/*********************/
/*********************/
// Printing
/*********************/
/*********************/
require([
	"esri/tasks/PrintTask", "esri/tasks/PrintParameters"
], function(
	PrintTask, PrintParameters
){...}

var printReportFunction;

printReportFunction = function printReport() {
	printTask.execute(printParams, printComplete, printError);
}






















