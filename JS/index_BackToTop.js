// Function to return the page to the beginning smoothly
function scrollToTop() {
    window.scrollTo({
        top: 0, // Scrolls to the top of the page
        behavior: "smooth" // Smooth scroll
    });
}

// Show or hide the back button based on page position
window.onscroll = function() {
    scrollFunction(); // Call scrollFunction on scroll event
};

function scrollFunction() {
    // Check scroll position
    if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
        // Show the button if scrolled more than 500px
        document.getElementById("scrollToTopBtn").style.display = "block";
    } else {
        // Hide the button if scrolled less than 500px
        document.getElementById("scrollToTopBtn").style.display = "none";
    }
}
