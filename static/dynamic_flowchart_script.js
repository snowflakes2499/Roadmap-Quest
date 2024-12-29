document.addEventListener("DOMContentLoaded", function() {
    let watchedVideos = [];

    // Load watched videos from the server
    function loadWatchedVideos() {
        return fetch("/watched_videos.json")
            .then(response => response.json())
            .then(data => {
                watchedVideos = data;
            });
    }

    // Save watched videos to the server
    function saveWatchedVideos() {
        fetch('/save_watched_videos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(watchedVideos)
        });
    }

    // Function to draw the flowchart
    function drawFlowchart(data) {
        const canvas = document.getElementById('flowchartCanvas');
        const ctx = canvas.getContext('2d');
        const nodesPerRow = 6;
        const horizontalSpacing = 200;
        const verticalSpacing = 200;
        const numRows = Math.ceil(data.length / nodesPerRow);
        const canvasWidth = nodesPerRow * horizontalSpacing + 100;
        const canvasHeight = numRows * verticalSpacing + 100;
        canvas.width = canvasWidth;
        canvas.height = canvasHeight;

        let start_reverse = 0;
        const flowchartData = data.map((item, index) => {
            let x;
            if (index % nodesPerRow === 0 && start_reverse === 0) {
                start_reverse = 1;
            } else if (index % nodesPerRow === 0 && start_reverse === 1) {
                start_reverse = 0;
            }
            if (start_reverse === 1) {
                x = (index % nodesPerRow) * horizontalSpacing + 50;
            } else {
                x = canvasWidth - (index % nodesPerRow) * horizontalSpacing - 150;
            }
            return {
                id: index + 1,
                x: x,
                y: Math.floor(index / nodesPerRow) * verticalSpacing + 100,
                text: item.label,
                link: item.link,
                connectedTo: index === data.length - 1 ? [] : [index + 2]
            };
        });

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        flowchartData.forEach(node => {
            node.connectedTo.forEach(targetId => {
                const targetNode = flowchartData.find(n => n.id === targetId);
                if (targetNode) {
                    drawArrow(ctx, node.x, node.y, targetNode.x, targetNode.y);
                }
            });

            ctx.beginPath();
            ctx.arc(node.x, node.y, 40, 0, Math.PI * 2);
            ctx.fillStyle = watchedVideos.includes(node.link.split('v=')[1]) ? '#0f0' : '#f00';
            ctx.fill();
            ctx.closePath();

            ctx.fillStyle = '#000';
            ctx.textAlign = 'center';
            ctx.fillText(node.text, node.x, node.y + 60);

            canvas.addEventListener('click', function(event) {
                const rect = canvas.getBoundingClientRect();
                const mouseX = event.clientX - rect.left;
                const mouseY = event.clientY - rect.top;

                if (Math.sqrt((mouseX - node.x) ** 2 + (mouseY - node.y) ** 2) < 40) {
                    window.open(node.link, '_blank');
                    const videoId = node.link.split('v=')[1];
                    if (!watchedVideos.includes(videoId)) {
                        watchedVideos.push(videoId);
                        saveWatchedVideos();
                        drawFlowchart(data); // Redraw to update the watched state
                    }
                }
            });
        });
    }

    function drawArrow(ctx, x1, y1, x2, y2) {
        const dx = x2 - x1;
        const dy = y2 - y1;
        const angle = Math.atan2(dy, dx);
        const length = Math.sqrt(dx ** 2 + dy ** 2);

        const arrowheadLength = 0;
        const nodeRadius = 40;
        const adjustedLength = length - nodeRadius;
        const endX = x1 + Math.cos(angle) * adjustedLength;
        const endY = y1 + Math.sin(angle) * adjustedLength;

        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(endX, endY);
        ctx.strokeStyle = '#000';
        ctx.stroke();
        ctx.closePath();
    }

    fetch('/items.json')
        .then(response => response.json())
        .then(items => {
            loadWatchedVideos().then(() => {
                drawFlowchart(items);
            });
        })
        .catch(error => console.error('Error fetching JSON:', error));
});
