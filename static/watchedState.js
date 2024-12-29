// watchedState.js
function getWatchedVideos() {
    return JSON.parse(localStorage.getItem('watchedVideos')) || [];
}

function addWatchedVideo(link) {
    let watchedVideos = getWatchedVideos();
    if (!watchedVideos.includes(link)) {
        watchedVideos.push(link);
        localStorage.setItem('watchedVideos', JSON.stringify(watchedVideos));
    }
}

function isVideoWatched(link) {
    let watchedVideos = getWatchedVideos();
    return watchedVideos.includes(link);
}
