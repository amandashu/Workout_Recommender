var currentVideoIndex = 0
var maxVideos = 0
//var maxVideos = 6

function overlayNextVideo() {
    maxVideos = parseInt(document.getElementsByClassName("workout-card").length)
    currentVideoIndex = (currentVideoIndex + 1) % maxVideos
    openPlayerOverlay(currentVideoIndex)
}

function likeButtonOnPressed(video_index, user_id, workout_id) {
    var cur_class = document.getElementById('like').getAttribute("class");
    document.getElementById('like').setAttribute("class", cur_class + " disabled");

    if (document.getElementById('like').text == "Liked") {
        $.ajax({
            url: '/remove_like/' + user_id + '/' + workout_id,
            success: function () {
                console.log("unliked!!");
                document.getElementById('like').setAttribute("class", "btn btn-primary")
                document.getElementById('like').text = "Like"
                document.getElementById('liked-status-' + video_index).style.visibility = "hidden"
            }
        });
    }
    else {
        $.ajax({
            url: '/record_like/' + user_id + '/' + workout_id,
            success: function () {
                console.log("liked!!");
                document.getElementById('like').setAttribute("class", "btn btn-danger")
                document.getElementById('like').text = "Liked"
                document.getElementById('liked-status-' + video_index).style.visibility = ""
            }
        });
    }
}

function openPlayerOverlay(videoIndex, liked) {
    console.log(videoIndex, liked);
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

    if (liked == "True") {
        document.getElementById('like').setAttribute("class", "btn btn-danger")
        document.getElementById('like').text = "Liked"
            }
    else {
        document.getElementById('like').setAttribute("class", "btn btn-primary")
        document.getElementById('like').text = "Like"
    }
    document.getElementById('like').setAttribute("onclick", "likeButtonOnPressed(" + videoIndex + ", " + document.getElementById('like').getAttribute('user_id') + "," + workout_id + ")");

    document.getElementById("overlay-display").style.display = "block";

}


function closePlayerOverlay() {
    document.getElementById("overlay-video").src = "";
    document.getElementById("overlay-display").style.display = "none";
}
