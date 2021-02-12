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