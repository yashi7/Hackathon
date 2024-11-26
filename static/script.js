document.addEventListener("DOMContentLoaded", function() {
    const leftDoor = document.querySelector('.left-door');
    const rightDoor = document.querySelector('.right-door');
    const loadingPage = document.querySelector('.loading-page');

    setTimeout(() => {
        leftDoor.style.transform = 'rotateY(-90deg)'; // Open left door to the left
        rightDoor.style.transform = 'rotateY(90deg)'; // Open right door to the right
    }, 500); // Delay before doors start opening

    setTimeout(() => {
        loadingPage.style.opacity = '0'; // Fade out the loading page
        loadingPage.style.visibility = 'hidden'; // Hide the loading page
    }, 2000); // Delay to hide the loading page after doors open
});
