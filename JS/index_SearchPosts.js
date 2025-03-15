function searchPosts() {
    var input = document.getElementById("searchInput").value.toLowerCase();
    var articles = document.querySelectorAll("article"); // Using querySelectorAll for better compatibility

    articles.forEach(function(article) {
        var title = article.querySelector("h2").innerText.toLowerCase();
        if (title.includes(input)) {
            article.style.display = "block"; // Ensures that matching articles are shown
        } else {
            article.style.display = "none"; // Hides non-matching articles
        }
    });
}
