function toggleLike() {
    var likeButton = document.querySelector('.like-button i');
    if (likeButton.classList.contains('bi-heart')) {
        likeButton.classList.remove('bi-heart');
        likeButton.classList.add('bi-heart-fill');
    } else {
        likeButton.classList.remove('bi-heart-fill');
        likeButton.classList.add('bi-heart');
    }
}