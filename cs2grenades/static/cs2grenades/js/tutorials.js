const videoDisplay = document.querySelector('.iframe-template');

document.querySelectorAll('.tutorial-card').forEach(card => {
    card.addEventListener('click', function(event) {
        event.preventDefault();
        
        const videoDiv = card.nextElementSibling;
        const video = videoDiv.dataset.iframe

        videoDisplay.innerHTML = video;
        videoDisplay.classList.add('active');

    });
});

window.addEventListener('mousedown', (event) => {
    if(event.target === videoDisplay) {
        videoDisplay.innerHTML = '';
        videoDisplay.classList.remove('active');
    }
});


document.querySelectorAll('.favorite-btn').forEach(button => {
    button.addEventListener('click', async function (event) {
        event.preventDefault();
        event.stopPropagation();

        const is_authenticated = await fetch('/is_authenticated/');
        const authData = await is_authenticated.json();

        if (!authData.authenticated) {
            infoAlert('Faça login ou crie sua conta para conseguir favoritar os posts')
            return;
        }

        const tutorialId = this.getAttribute('data-tutorial-id');

        try {
            const response = await fetch(`/toggle_favorite/tutorial/${tutorialId}`, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });

            const data = await response.json();

            if (!response.ok) {
                console.error('Fetch error:', response.status);
                return;
            }

            if (data.is_favorite) {
                button.classList.add('active')
            } else {
                button.classList.remove('active')
            };

        } catch (error) {
            console.error('Error:', error)
        };

    });
});
