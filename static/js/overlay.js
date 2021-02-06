var currentVideoIndex = 0
var maxVideos = 0
//var maxVideos = 6

function overlayNextVideo() {
    maxVideos = parseInt(document.getElementsByClassName("workout-card").length)
    currentVideoIndex = (currentVideoIndex + 1) % maxVideos
    openPlayerOverlay(currentVideoIndex)
}

function recordLike(user_id, workout_id) {
    var mysql = require('mysql');
    var json = require('../../config/db_config.json');

    var con = mysql.createConnection({
        host: json['mysql_host'],
        user: json['mysql_user'],
        password: json['mysql_password'],
        database: json['mysql_db']
    });

    con.connect(function (err) {
        if (err) throw err;
        console.log("Connected!");
        var sql = "INSERT INTO user_item_interaction (user_id, workout_id) VALUES (" + user_id + ", " + workout_id + ")";
        con.query(sql, function (err, result) {
            if (err) throw err;
            console.log("1 record inserted");
        });
    });
}

function openPlayerOverlay(videoIndex) {
    currentVideoIndex = parseInt(videoIndex)
    ytURL = document.getElementById("video-index-" + videoIndex).textContent
    videoTitle = document.getElementById("workout-title-index-" + videoIndex).textContent
    videoDesc = document.getElementById("workout-text-index-" + videoIndex).innerText
    fbURL = document.getElementById("fb-link-index-" + videoIndex).innerText

    document.getElementById("overlay-video").src = ytURL;
    document.getElementById("overlay-fb-link").href = fbURL;
    document.getElementById("overlay-workout-title").textContent = videoTitle
    document.getElementById("overlay-workout-text").innerText = videoDesc

    document.getElementById("overlay-display").style.display = "block";

}


function closePlayerOverlay() {
    document.getElementById("overlay-video").src = "";
    document.getElementById("overlay-display").style.display = "none";
}