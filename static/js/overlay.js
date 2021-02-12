var currentVideoIndex = 0
var maxVideos = 0
//var maxVideos = 6

function overlayNextVideo() {
    maxVideos = parseInt(document.getElementsByClassName("workout-card").length)
    currentVideoIndex = (currentVideoIndex + 1) % maxVideos
    openPlayerOverlay(currentVideoIndex)
}

function openPlayerOverlay(videoIndex) {
    currentVideoIndex = parseInt(videoIndex)
    ytURL = document.getElementById("video-index-" + videoIndex).textContent
    videoTitle = document.getElementById("workout-title-index-" + videoIndex).textContent
    videoDesc = document.getElementById("workout-text-index-" + videoIndex).innerText
    fbURL = document.getElementById("fb-link-index-" + videoIndex).innerText
    workout_id = document.getElementById("startWorkout-index-" + videoIndex).getAttribute("workout_id");
    original_url = document.getElementById('like').href;
    

    document.getElementById("overlay-video").src = ytURL;
    document.getElementById("overlay-fb-link").href = fbURL;
    document.getElementById("overlay-workout-title").textContent = videoTitle
    document.getElementById("overlay-workout-text").innerText = videoDesc
    document.getElementById('like').setAttribute("href", original_url.substr(0, original_url.lastIndexOf("/") + 1) + workout_id);
    

    document.getElementById("overlay-display").style.display = "block";
    console.log(workout_id)


    /*
    document.getElementById("startWorkout-index" + videoIndex).addEventListener("click", function () {
        sessionStorage.setItem('workout_id') = document.getElementById("startWorkout").getAttribute("workout_id");

        var original_url = document.getElementById('like').href;

        document.getElementById('like').setAttribute("href", original_url.substr(0, original_url.lastIndexOf("/")) + sessionStorage.getItem('workout_id'));

        console.log(sessionStorage.getItem('workout_id'));
      });
    */
}


function closePlayerOverlay() {
    document.getElementById("overlay-video").src = "";
    document.getElementById("overlay-display").style.display = "none";
}