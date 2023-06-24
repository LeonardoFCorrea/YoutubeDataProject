function animateOpacity() {
    var container = document.getElementById("myContainer");
    var maxOpacity = 1;
    var minOpacity = 0.7;
    var scrollCounter = 0;

    container.style.opacity = minOpacity;

    window.addEventListener("scroll", function () {
        var scrollHeight = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollHeight !== 0 && scrollCounter < 2) {
            scrollCounter++;
        } else if (scrollCounter === 2) {
            container.style.opacity = maxOpacity;
            scrollCounter++;
        }

        if (scrollHeight === 0 && scrollCounter > 2) {
            container.style.opacity = minOpacity;
            scrollCounter = 0;
        }
    });
}

animateOpacity();
