document.querySelectorAll('.favorite-btn').forEach(button => {
    button.addEventListener('click', async function (event) {
        event.preventDefault();

        const is_authenticated = await fetch('/is_authenticated/');
        const authData = await is_authenticated.json();

        if (!authData.authenticated) {
            infoAlert('Faça login ou crie sua conta para conseguir favoritar os posts')
            return;
        }

        const guideId = this.getAttribute('data-guide-id');

        try {
            const response = await fetch(`/toggle_favorite/guide/${guideId}`, {
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
