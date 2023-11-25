
document.addEventListener('DOMContentLoaded', function () {
    // Array of book images
    const bookImages = [
        'bg2.avif',
        'bg3.jpg',
        'bg2.avif',
        'cover2.avif',
    ];

    // Get the hero section and book image element
    const heroSection = document.getElementById('hero-section');

    // Function to change the background image
    function changeBackgroundImage() {
        const randomImage = bookImages[Math.floor(Math.random() * bookImages.length)];
        const imageUrl = `./images/${randomImage}`;
        heroSection.style.backgroundImage = `url(${imageUrl})`;
    }

    // Change the background image on page load
    changeBackgroundImage();

    // Change the background image every 5 seconds
    setInterval(changeBackgroundImage, 5000);
});
