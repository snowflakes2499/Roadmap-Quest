document.addEventListener("DOMContentLoaded", function() {
    const itemsContainer = document.getElementById('items');
    let player;
    let currentItemElement;

    // Create the YouTube player when the API is ready
    function onYouTubeIframeAPIReady() {
        player = new YT.Player('iframe', {
            height: '390',
            width: '640',
            videoId: '', // Initial video ID can be empty
            events: {
                'onReady': onPlayerReady,
                'onStateChange': onPlayerStateChange
            }
        });
    }

    function onPlayerReady(event) {
        // Player is ready
    }

    function onPlayerStateChange(event) {
        if (event.data == YT.PlayerState.PLAYING) {
            // Check every second if the video is almost finished
            const intervalId = setInterval(function() {
                const currentTime = player.getCurrentTime();
                const duration = player.getDuration();
                if (currentTime / duration > 0.95) { // If 95% of the video is watched
                    if (currentItemElement) {
                        const videoId = player.getVideoData().video_id;
                        markVideoAsWatched(videoId);
                        currentItemElement.style.backgroundColor = 'green';
                        let watchedVideos = JSON.parse(localStorage.getItem('watchedVideos')) || [];
                        if (!watchedVideos.includes(videoId)) {
                            watchedVideos.push(videoId);
                            localStorage.setItem('watchedVideos', JSON.stringify(watchedVideos));
                        }
                    }
                    clearInterval(intervalId);
                }
            }, 1000);
        }
    }

    function markVideoAsWatched(videoId) {
        let watchedVideos = JSON.parse(localStorage.getItem('watchedVideos')) || [];
        if (!watchedVideos.includes(videoId)) {
            watchedVideos.push(videoId);
            localStorage.setItem('watchedVideos', JSON.stringify(watchedVideos));
        }
    }

    function checkAndMarkWatchedItems() {
        let watchedVideos = JSON.parse(localStorage.getItem('watchedVideos')) || [];
        document.querySelectorAll('.item').forEach(itemElement => {
            const videoId = itemElement.getAttribute('data-video-id');
//            console.log("VIDEO ID: " + videoId)
            if (watchedVideos.includes(videoId)) {
                console.log("WATCHED VIDEO ID: " + videoId)
                itemElement.style.backgroundColor = 'green';
            }
        });
    }

    // Fetch items from JSON file
    fetch("/items.json")
        .then(response => response.json())
        .then(items => {
            // Create clickable items
            items.forEach(item => {
                const itemElement = document.createElement('div');
                itemElement.classList.add('item');
                itemElement.textContent = item.label;
                itemElement.setAttribute('data-video-id', item.link.split('v=')[1]); // Store video ID in a data attribute
                itemElement.addEventListener('click', function() {
                    const videoId = itemElement.getAttribute('data-video-id');
//                    console.log("VIDEO ID: " + videoId)
                    if (player && player.loadVideoById) {
                        player.loadVideoById(videoId);
                        currentItemElement = itemElement;
                    } else {
                        console.error('Player is not ready');
                    }
                });
                itemsContainer.appendChild(itemElement);
            });
            // Check and mark watched items after creating them
            checkAndMarkWatchedItems();
        })
        .catch(error => {
            console.error('Error fetching items:', error);
        });

    // Ensure the API is loaded
    var tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    // Expose the onYouTubeIframeAPIReady function to the global scope
    window.onYouTubeIframeAPIReady = onYouTubeIframeAPIReady;
});
