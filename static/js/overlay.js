var currentVideoIndex = 0
var maxVideos = 0
//var maxVideos = 6

function overlayNextVideo() {
    maxVideos = parseInt(document.getElementsByClassName("workout-card").length)
    currentVideoIndex = (currentVideoIndex + 1) % maxVideos
    openPlayerOverlay(currentVideoIndex)
}

function record(user_id, workout_id) {
    $.ajax({
        url: '/record_like/' + user_id + '/' + workout_id,
        success: function () {
            console.log("liked!!");
        }
    });
}

function openPlayerOverlay(videoIndex) {
    currentVideoIndex = parseInt(videoIndex)
    ytURL = document.getElementById("video-index-" + videoIndex).textContent
    videoTitle = document.getElementById("workout-title-index-" + videoIndex).textContent
    videoDesc = document.getElementById("workout-text-index-" + videoIndex).innerText
    fbURL = document.getElementById("fb-link-index-" + videoIndex).innerText
    workout_id = document.getElementById("startWorkout-index-" + videoIndex).getAttribute("workout_id");

    document.getElementById("overlay-video").src = ytURL;
    document.getElementById("overlay-fb-link").href = fbURL;
    document.getElementById("overlay-workout-title").textContent = videoTitle
    document.getElementById("overlay-workout-text").innerText = videoDesc
    document.getElementById('like').setAttribute("onclick", "record(" + document.getElementById('user_id') + "," + workout_id + ")");



    document.getElementById("overlay-display").style.display = "block";
    console.log(workout_id);
}


function closePlayerOverlay() {
    document.getElementById("overlay-video").src = "";
    document.getElementById("overlay-display").style.display = "none";
}