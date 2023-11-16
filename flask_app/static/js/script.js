const swiper = new Swiper(".swiper", {
    // How many slides to show
    slidesPerView: 1,
    // How much space between slides
    spaceBetween: 20,
    // Make the next and previous buttons work
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    // Make the pagination indicators work
    pagination: {
        el: ".swiper-pagination",
    },
    //Responsive breakpoints for how many slides to show at that view
    breakpoints: {
        // 700px and up shoes 2 slides
        700: {
            slidesPerView: 3,
        },
        // 1200px and up shoes 3 slides
        1200: {
            slidesPerView: 5,
        },
    },
});

document.addEventListener('DOMContentLoaded', function () {
    const replyButtons = document.querySelectorAll('.reply-button');
    const replyForms = document.querySelectorAll('.reply-form');

    replyButtons.forEach((button, index) => {
        button.addEventListener('click', function () {
            const replyForm = replyForms[index];
            replyForm.style.display = replyForm.style.display === 'none' ? 'block' : 'none';
        })
    })



});

var articleLikedCount = document.getElementById('article-count').textContent;
console.log(articleLikedCount);
var likeForms = document.querySelectorAll('.likeForm');

likeForms.forEach(function(likeForm){
    likeForm.onsubmit = function (e) {
        e.preventDefault();
        var likedInput = likeForm.querySelector('input[name="liked"]');
        var formData = new FormData(likeForm);
        console.log(likedInput);
        fetch("http://localhost:5000/articles/dashboard/like", { method: 'POST', body: formData })
            .then(response => response.json())
            .then(data => {
                console.log(articleLikedCount);
                var likesCount = likeForm.querySelector('.likes-count');
                var thumbsUp = likeForm.querySelector('.thumb');
                likesCount.textContent = data.likes_count;
                thumbsUp.className = thumbsUp.className === 'fa-solid fa-thumbs-up thumb' ? 'fa-regular fa-thumbs-up thumb': 'fa-solid fa-thumbs-up thumb';
                if(likedInput.value === 'FALSE'){
                    articleLikedCount++;
                }else{
                    articleLikedCount -= 1;
                }
                document.getElementById('article-count').textContent = articleLikedCount;
                console.log('value ', likedInput.value)
                likedInput.value = likedInput.value === 'TRUE' ? 'FALSE' : 'TRUE';
            })
            .catch(err => {console.log(err)})
    }

})



