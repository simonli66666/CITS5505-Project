
function getLike(postId) {
    var likeButton = document.querySelector(`#like-icon-${postId}`);
    fetch(`post/like/${postId}/`, { method: 'GET' })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            console.log(data.isLiked)
            if (data.isLiked) {
                likeButton.classList.remove('bi-heart');
                likeButton.classList.add('bi-heart-fill');
            } else {
                likeButton.classList.remove('bi-heart-fill');
                likeButton.classList.add('bi-heart');
            }
        }
    }).catch(error => console.error('Error:', error));

}

function toggleLike(postId) {
    var likeButton = document.querySelector(`#like-icon-${postId}`);
    var likeNum = document.querySelector(".like-num");
    var number = + likeNum.innerText.replace(' Like', '');
    fetch(`/post/like/${postId}/`, { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.isLiked) {
                likeButton.classList.remove('bi-heart');
                likeButton.classList.add('bi-heart-fill');
                var newNumber = number + 1;
                likeNum.innerText = `${newNumber} Like`;
            } else {
                likeButton.classList.remove('bi-heart-fill');
                likeButton.classList.add('bi-heart');
                var newNumber = number - 1;
                likeNum.innerText = `${newNumber} Like`;
            }
            alert(data.message);  // show a message to the user

        }
    })
    .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function() {

    const likeIcon = document.querySelector('.like-heart');
    const postId = likeIcon.id.replace('like-icon-', '');;
    if (likeIcon) {
        getLike(postId);
    }
});