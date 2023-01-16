var vans = { "H": 0, "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8  };
var Maps = [];
var markers = [];

function initialize() {
    var myLatLng = new google.maps.LatLng(53, -1);
    myOptions = {
        zoom: 13,
        center: myLatLng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    Maps[0] = new google.maps.Map(document.getElementById("map0"), myOptions);
    Maps[1] = new google.maps.Map(document.getElementById("map1"), myOptions);
    Maps[2] = new google.maps.Map(document.getElementById("map2"), myOptions);
    Maps[3] = new google.maps.Map(document.getElementById("map3"), myOptions);
    addPoint(Maps[0], 53, -1, "A");
    addPoint(Maps[1], 53, -1, "B");
    addPoint(Maps[2], 53, -1, "C");
    addPoint(Maps[3], 53, -1, "D");
    addPoint(Maps[0], 53, -1, "E");
    addPoint(Maps[1], 53, -1, "F");
    addPoint(Maps[2], 53, -1, "G");
    addPoint(Maps[3], 53, -1, "H");
    movePoint(53.5, -2, "A");
    movePoint(53, 0, "B");
    movePoint(53.5, -1, "C");
    movePoint(53, -2, "D");
}
function movePoint(lat, lng, name) {
    var thisLatlng = new google.maps.LatLng(lat, lng);
    markers[vans[name]].setPosition(thisLatlng);
}

function addPoint(thismap, lat, lng, name) {
    var thisLatlng = new google.maps.LatLng(lat, lng);
    var marker = new google.maps.Marker({
        position: thisLatlng
    });
    marker.setMap(thismap);
    markers[vans[name]] = marker;
}
initialize();