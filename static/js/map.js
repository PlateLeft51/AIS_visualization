let map,geocoder;
let markers = [];
let lines = [];
let dt = [];
let keyMap = {};
let track_def;
let data = document.getElementById('aisData').getAttribute('d');
let time_data = document.getElementById('aisData').getAttribute('tm');
let type_data = document.getElementById('aisData').getAttribute('tp');
let shiptype = document.getElementById('aisData').getAttribute('ship_info');
let outliers = document.getElementById('aisData').getAttribute('outliers');
let track = document.getElementById('aisData').getAttribute('track');
console.log(type_data);
function initialize() {
    var mapProp = {
        center: new google.maps.LatLng(1.25333, 103.65),
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        disableDefaultUI: true,
        styles: [
            {
                "featureType": "administrative",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "lightness": 33
                    }
                ]
            },
            {
                "featureType": "landscape",
                "elementType": "all",
                "stylers": [
                    {

                        "color": "#f2e5d4"
                    }
                ]
            },
            {
                "featureType": "poi",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },

            {
                "featureType": "road",
                "elementType": "all",
                "stylers": [
                    {
                        "lightness": 20
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "off",
                    },
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#c5c6c6"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#e4d7c6"
                    }
                ]
            },
            {
                "featureType": "road.local",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#fbfaf7"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "color": "#acbcc9"
                    }
                ]
            }
        ]
    };
    map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

    if (type_data.length === 0) {

    }
    else if (type_data === "static") {
        jsonify();
        setTime();

        createMarkers();
        document.getElementById('res_num').innerHTML = data.length + " results are found.";
    }
    else if (type_data === "dynamic") {
        jsonify();
        setTime();

        getKeyMap();
        play();
    }
    else if (type_data === "trajectory") {
        // console.log("traj")
        jsonify();
        setTime();

        createMarkers();
        getKeyMap();
        drawLines(track_def);

    }
    else if (type_data === "outliers") {
        // console.log("outliers");
        jsonify();
        setTime();

        outliers = outliers.substr(0, outliers.length-1);
        outliers = outliers.substr(1)
        outliers = outliers.split(" ").join("");
        outliers = outliers.split(",");
        getKeyMap();

        createMarkers();
        drawLines(track_def);
    }
}
function createMarkers(){
    for(let i=0; i<data.length; i++) {

        // const latlng = {
        //     lat: parseFloat(data[i].lat),
        //     lng: parseFloat(data[i].lon),
        // };
        // geocoder = new google.maps.Geocoder();
        // geocoder
        //     .geocode({location:latlng})
        //     .then((response) =>{
        //         console.log(response.results[0].formatted_address);
        //     })
        let type_info = shiptype.find(x => x.mmsi === data[i].mmsi)
        markers.push(new google.maps.Marker({
            position: new google.maps.LatLng(data[i].lat,data[i].lon),
            map: map,
            animation: google.maps.Animation.DROP,
            content: "name: " + type_info['name'] + '<br>'
                +"type: " + type_info['type'] + '<br>'
                +"width: " + type_info['width'] + '<br>'
                +"length: " + type_info['length'] + '<br>'
                +"mmsi: " + data[i].mmsi + '<br>'
                +"time: " + calTime(data[i].time) + '<br>'
                +"lat: " + data[i].lat + '<br>'
                +"lon: " + data[i].lon,
            icon: getIcon(data[i].heading,data[i].mmsi)
        }));

        // shiptype = JSON.stringify(shiptype);
        // // shiptype = JSON.parse(shiptype.replace(/'/g,'"'));
        // console.log(typeof shiptype)

        let infowindow =new google.maps.InfoWindow({})
        markers[i].addListener('click', function(){
            populateInfoWindow(this, infowindow);
            infowindow.open(map,this);
        })
    }
    // import {createRequire} from 'module';
    // const require = createRequire(import.meta.url);

    // const spawner = require('child_process').spawn;
    // const data_to_pass_in = 'Send this to python';
    // const python_process = spawner('python',['./poly.py', data_to_pass_in]);

    // python_process.stdout.on('data', data => {
    //     console.log('Data received', data.toString());
    // })
}

function populateInfoWindow(marker, info){
    if(info.marker !== marker){
        info.setContent('');
        info.setContent(marker.content);
    }
}

//trajectory functions
function getKeyMap(){
    for (let j = 0; j < data.length; j++) {
        let elemKey = data[j].mmsi;
        if (elemKey in keyMap) {
            dt[keyMap[elemKey]].value.push(data[j]);
        }
        else {
            dt.push({
                "mmsi": data[j].mmsi,
                "time": data[j].time,
                "value": [data[j]]
            });
            keyMap[elemKey] = dt.length - 1;
        }
    }

    for(let i=0;i<dt.length;i++){
        for(let j=0;j<dt[i].value.length;j++){
            dt[i].value[j].lat = parseFloat(dt[i].value[j].lat);
            dt[i].value[j].lon = parseFloat(dt[i].value[j].lon);
        }
    }
}

// execute get_spline_points() before this function
function drawLines(tracks){
    for(const key in tracks){
        let len = tracks[key].length;
        if(cal_distance(tracks[key][0][0],tracks[key][0][1],tracks[key][len-1][0],tracks[key][len-1][1])>1e-3){
            let route = []
            for(let k=0; k<tracks[key].length; k++)
                route.push(new google.maps.LatLng(tracks[key][k][0],tracks[key][k][1]))
            var lineSymbol ={
                path:'M 0,-1 0,1',
                strokeOpacity: 1,
                scale:3
            };
            lines.push(new google.maps.Polyline({
                path:route,
                map: map,
                strokeColor:"#ffff66",
                strokeOpacity:0,
                strokeWeight:2,
                icons: [{
                    icon: lineSymbol,
                    offset: '0',
                    repeat: '20px'
                }]
            }));

        }

    }
}
function get_linear(){
    while(lines.length){
        lines.pop().setMap(null);
    }
    drawLines(track['slinear']);
}
function get_quadratic(){
    while(lines.length){
        lines.pop().setMap(null);
    }
    drawLines(track['quadratic']);
}
function get_cubic(){
    while(lines.length){
        lines.pop().setMap(null);
    }
    drawLines(track['cubic']);
}

// dynamic functions
var numDeltas = 75;
var delay = 66; //milliseconds
let pause_btn = false;
// execute get_spline_points() before this function
function movement(cur){
    while(markers.length){
        markers.pop().setMap(null);
    }
    let i = 0;

    for(const key in track_def){
        if(track_def[key].length>=75){
            setTimeout("transition("+key+", "+i+", "+cur+")", 5);
            i = i + 1;
        }
    }
}


function transition(key,i,cur){
    let id = keyMap[key];
    markers.push(new google.maps.Marker({
        position: new google.maps.LatLng(track_def[key][0][0], track_def[key][0][1]),
        map: map,
        content: "mmsi: " + dt[id].value[0].mmsi + '<br>'
            +"time: " + calTime(dt[id].value[0].time),
        icon: getIcon(dt[id].value[0].course,dt[id].value[0].mmsi),
        mmsi: key
    }));

    let infowindow =new google.maps.InfoWindow({})
    markers[i].addListener('click', function(){
        populateInfoWindow(this, infowindow);
        infowindow.open(map,this);
    })
    let len=dt[id].value.length;
    let start_time = time_interval(time_data.st, dt[id].value[0].time);
    let moving_time = time_interval(dt[id].value[0].time, dt[id].value[len-1].time);
    let query_time = time_interval(time_data.st, time_data.ed)

    let delay_move = Math.round(delay*moving_time/query_time);
    let delay_st = Math.round(delay_move*numDeltas*start_time/moving_time) - cur * 50;
    delay_st = delay_st>0?delay_st:0;
    // console.log(start_time, moving_time, query_time, delay_move, delay_st)
    // console.log(Math.round(cur*3/4));
    let cr = Math.round(cur*3/4);
    setTimeout("moveMarker("+key+","+i+","+cr+","+delay_move+")", delay_st);
    // moveMarker(key, i, 0);
}

function moveMarker(key,i,num,delay_move){
    let latlng = new google.maps.LatLng(track_def[key][num][0], track_def[key][num][1]);

    markers[i].setPosition(latlng);

    if(num<numDeltas-1&&!pause_btn){
        // console.log(markers[i].icon.replace("5", icon_dir));
        // str.substring(0, index) + char + str.substring(index + 1);   .slice(0, -1) + '0';
        if(cal_distance(track_def[key][num][1],track_def[key][num][0],track_def[key][num+1][1],track_def[key][num+1][0])>1e-4){
            let course = calc_angle(track_def[key][num][1],track_def[key][num][0],track_def[key][num+1][1],track_def[key][num+1][0]);
            markers[i].setIcon(markers[i].icon.slice(0,-5)+course+markers[i].icon.slice(-4));
        }

        num++;
        setTimeout("moveMarker("+key+","+i+","+num+","+delay_move+")", delay_move);
    }
}
function setMarker(cur){
    let num = Math.round(3 * cur / 4);
    for(let i = 0;i<markers.length;i++){
        var key = markers[i].mmsi;
        var latlng = new google.maps.LatLng(track_def[key][num][0], track_def[key][num][1]);
        markers[i].setPosition(latlng);
    }
}

function play_forward(){
    let cur = getProgress() + 5;
    cur = (cur>100?100:cur);
    $("#probar").css("width",cur + "%");
    $("#probar").text(cur + "%");
    setMarker(cur);
}

function play_back(){
    let cur = getProgress() - 5;
    cur = (cur<0?0:cur);
    $("#probar").css("width",cur + "%");
    $("#probar").text(cur + "%");
    setMarker(cur);
}

function play(){
    pb = $("#probar")
    play_btn = $("#play")
    if(play_btn.val()==="play"){
        pause_btn = false;
        if(getProgress()===100)
            pb.css('width','0%')
        if(type_data.length !== 0){
            movement(getProgress());
        }
        play_btn.attr({"value": "pause"});
        pb.css('transition','none')
        pb.animate({
            width:"100%"
        },{
            duration: 5 * 10 * (100- getProgress()) ,
            easing: 'linear',
            step:function(now, fx){
                var current_percent = Math.round(now);
                pb.attr('aria-valuenow', current_percent);
                pb.text(current_percent + '%');
            },
            complete: function(){
                play_btn.attr({"value": "play"});
            }
        })

    }
    else if(play_btn.val()==="pause"){
        pause_btn = true;
        $("#probar").stop();
        // setMarker(getProgress());
        play_btn.attr({"value": "play"});
        // console.log(markers[0].mmsi, track[markers[0].mmsi]);
    }


}
function getProgress(){
    let total = $("#bar").css("width");
    let progress = $("#probar").css("width");
    total = total.replace("px","");
    progress = progress.replace("px","");
    return Math.round(progress/total*100);
}

// Tool functions
function calTime(time){
    return time.substring(0,4)+"-"+time.substring(4,6)+"-"+time.substring(6,8)
        +" "+time.substring(8,10)+":"+time.substring(10,12)+":"+time.substring(12,14);
}


let temp
let iconSrc = "/static/img/bulk/5.png"
let type_list = {"Bulk Carrier":"bulk","Cargo":"cargo","Container Ship":"container","Passenger":"passenger",
                "Special Purpose Ship":"special","Tanker":"tanker","Tug":"tug","None":"unknown"}
function getIcon(heading, mmsi){
    if(type_data !== "outliers"){
        // console.log(heading, mmsi)
        let icon_color = type_list[shiptype.find(x => x.mmsi === mmsi).type];
        let icon_size = shiptype.find(x => x.mmsi === mmsi).width;
        let icon_dir = heading==='None'?5:parseInt(heading / 45)

        if (icon_color === undefined){
            icon_color = "bulk"
        }
        // console.log(icon_color, icon_dir)
        temp = iconSrc.replace("bulk", icon_color)
        icon_size = icon_size==='None'?0:Math.floor(parseInt(icon_size)/30);
        if(icon_color!=="tug" && icon_color!=="unknown"){
            temp = temp.replace("5", icon_size.toString()+icon_dir.toString());
            // console.log(icon_color,temp)
        }

        else
            temp = temp.replace("5", icon_dir);
        return temp
    }
    else{
        temp = iconSrc.replace("bulk", "tug")
        if(outliers.includes(mmsi)){
            temp = iconSrc.replace("bulk", "unknown")
        }

        let icon_dir = heading==='None'?5:parseInt(heading / 45)
        temp = temp.replace("5", icon_dir)
        return temp
    }

}

function setTime(){
    // console.log(time_data);
    // console.log(time_data.length);
    if(JSON.stringify(time_data)!=="{}"){

        document.getElementById('start').value = time_data.st;
        document.getElementById('end').value = time_data.ed;
        // console.log(document.getElementById('end').value);
    }
}

function jsonify(){
    data = JSON.parse(data.replace(/'/g,'"'));
    shiptype = JSON.parse(shiptype.replace(/'/g,'"'));
    time_data =JSON.parse(time_data.replace(/'/g,'"'));
    if(track.length>0){
        track = JSON.parse(track.replace(/'/g,'"'));
        track_def = track['quadratic'];
    }
}

function time_interval(start, end){
    let st = parseInt(start);
    let ed = parseInt(end);
    let res = to_second(ed) - to_second(st);
    return res>=0?res:0;
}
function to_second(t){
    s = Math.round(t%100)
    m = Math.round(Math.round(t/100)%100)
    h = Math.round(Math.round(t/10000)%100)
    d = Math.round(Math.round(t/1000000)%100)
    return s+60*m+3600*h+86400*d;
}
function calc_angle(x1,y1,x2,y2){
    let angle = 90-Math.atan2(y2-y1,x2-x1)*(180/Math.PI);
    angle = angle>0?angle:angle+360;
    return Math.round(Math.round(angle/45)%8);
}
function cal_distance(x1,y1,x2,y2){
    return Math.sqrt((x2-x1) * (x2-x1) + (y2-y1) * (y2-y1));
}
function DrawImage(ImgD)
{
    var image=new Image();
    image.src=ImgD.src;
    image.width = image.width *2;
    image.height = image.height * 2;
    return image;

}
google.maps.event.addDomListener(window, 'load', initialize);
