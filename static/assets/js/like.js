function toggleLike(postId) {
    var likeButton = document.querySelector(`#like-icon-${postId}`);
    fetch(`/like/${postId}/`, { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.isLiked) {
                likeButton.classList.remove('bi-heart');
                likeButton.classList.add('bi-heart-fill');
            } else {
                likeButton.classList.remove('bi-heart-fill');
                likeButton.classList.add('bi-heart');
            }
            alert(data.message);  // show a message to the user
        }
    })
    .catch(error => console.error('Error:', error));
}