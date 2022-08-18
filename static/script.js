const nextBtn = document.getElementById("next-btn");
const spotifyEmbed = document.getElementById("spotify-embed");

nextBtn.addEventListener("click", function() {
    fetch("/api/track")
        .then(res => res.json())
        .then(data => {
            spotifyEmbed.src = `https://open.spotify.com/embed/track/${data.trackId}`;
        }
    );
});