document.addEventListener("DOMContentLoaded", function() {
    var image = document.getElementById('user-image');
    
    var colorThief = new ColorThief();
  
    if (image.complete) {
        var dominantColor = colorThief.getColor(image); 
        var boxShadowColor = `rgba(${dominantColor[0]}, ${dominantColor[1]}, ${dominantColor[2]}, 1)`;
        image.style.boxShadow = `0px -86px 150px -80px ${boxShadowColor}`
0
    } else {
        image.addEventListener('load', function() {
            var dominantColor = colorThief.getColor(image);
            var boxShadowColor = `rgb(${dominantColor[0]}, ${dominantColor[1]}, ${dominantColor[2]}, 1)`;
            image.style.boxShadow = `0px -86px 150px -80px ${boxShadowColor}`
        })
    };
});