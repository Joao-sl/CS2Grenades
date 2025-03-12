const userInfoBtn = document.querySelector('#user-info');
const changePasswordBtn = document.querySelector('#change-password');
const delAccountBtn = document.querySelector('#del-account');
const profileContent = document.querySelector('#profile-content');


function reloadPageAfterCloseAlert() {
    const closeButton = document.querySelector('#close-alert');
    if (closeButton) {
        closeButton.addEventListener('click', () => {
            location.reload();
        });
    }
    window.addEventListener('mousedown', (event) => {
        if (event.target === customAlert) {
            location.reload();
        }
    });
}

function activeButton(button) {
    userInfoBtn.classList.remove('active');
    changePasswordBtn.classList.remove('active');
    delAccountBtn.classList.remove('active');
    button.classList.add('active');
}

async function userImageUpdate() {
    const formData = new FormData();
    const avatarInput = document.querySelector('#user-avatar');
    const submitAvatarBtn = document.querySelector('#submit-avatar-btn');

    submitAvatarBtn.addEventListener('click', async(event) => {
        event.preventDefault();
    
        if(!avatarInput.value) {
            warningAlert('Nenhuma imagem selecionada. Selecione a imagem que deseja usar de avatar.')
            return;
        }

        const avatar = avatarInput.files[0];
        formData.append('avatar', avatar);

        try {
            const response = await fetch('/user_update/', {
                method: 'POST',
                headers: {
                    'X-CS2Grenades-Requested-With': 'FetchRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: formData,
            });

            data = await response.json();

            if (!response.ok) {
                console.error('Fetch error:', response.status);
                errorAlert('Desculpe não foi possível salvar sua imagem tente novamente mais tarde')
                return;
            } 

            if (data.success) {
                successAlert(data.success)
                reloadPageAfterCloseAlert();
            }

            if (!data.success) {
                errorAlert(data.error)
            }


        } catch(error) {
            console.error('Error:', error)
        }
    });
}

async function userUpdate() {
    const nameInput = document.querySelector('#name');
    const usernameInput = document.querySelector('#username');
    const emailInput = document.querySelector('#email');

    const originalName = nameInput.value;
    const originalUsername = usernameInput.value;
    const originalEmail = emailInput.value;

    const sendUpdateBtn = document.querySelector('#save-config-btn');
    sendUpdateBtn.addEventListener('click', async (event) => {
        event.preventDefault();

        if (originalName === nameInput.value && originalUsername === usernameInput.value && originalEmail === emailInput.value) {
            warningAlert('Nenhuma alteração, altere o dado desejando.');
            return;
        }

        const response = await fetch('/user_update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CS2Grenades-Requested-With': 'FetchRequest',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                'name': nameInput.value,
                'username': usernameInput.value,
                'email': emailInput.value
            })
        });

        data = await response.json();

        if (data.success) {
            successAlert(data.successMsg);
            reloadPageAfterCloseAlert();
        }

        if (!data.success) {
            errorAlert(data.error);
        }
    });
};

async function userUpdateLoadLayout() {
    changePasswordBtn.disabled = false;
    delAccountBtn.disabled = false;
    userInfoBtn.disabled = true;

    try {
        const response = await fetch('/user_update/', {
            headers: {
                'X-CS2Grenades-Requested-With': 'FetchRequest'
            }
        })

        if (!response.ok) {
            throw new Error('Erro de conexão servidor, por favor tente novamente mais tarde.')
        }

        const html = await response.text();
        profileContent.innerHTML = html;
        activeButton(userInfoBtn);
     

    } catch (error) {
        errorAlert(error);
        userInfoBtn.disabled = false;
    }

    userUpdate()
    userImageUpdate()
};

async function passwordUpdate() {
    const currentPasswordInput = document.querySelector('#current_password');
    const newPasswordInput = document.querySelector('#password');
    const newPasswordConfirmInput = document.querySelector('#password_confirm');

    const sendUpdateBtn = document.querySelector('#save-config-btn');
    sendUpdateBtn.addEventListener('click', async (event) => {
        event.preventDefault();
        
        const currentPassword = currentPasswordInput.value;
        const newPassword = newPasswordInput.value;
        const newPasswordConfirm = newPasswordConfirmInput.value;

        if(newPassword === '' || newPasswordConfirm === '') {
            warningAlert('Preencha todos os campos.');
            return;
        }

        if(currentPassword === newPassword) {
            warningAlert('A senha atual e a nova senha não podem ser iguais');
            return;
        }
        if(newPassword != newPasswordConfirm) {
            warningAlert('Verifique a confirmação da senha, elas não coincidem')
        }

        const response = await fetch('/password_update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CS2Grenades-Requested-With': 'FetchRequest',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                'currentPassword': currentPassword,
                'newPassword': newPassword,
                'newPasswordConfirm': newPasswordConfirm,
            })
        });

        data = await response.json();

        if(data.success) {
            successAlert('Senha alterada com sucesso.');
            reloadPageAfterCloseAlert();
        };

        if(!data.success) {
            errorAlert(data.error);
        };
    });
};

async function passwordUpdateLoadLayout() {
    userInfoBtn.disabled = false;
    delAccountBtn.disabled = false;
    changePasswordBtn.disabled = true;

    try {
        const response = await fetch('/password_update/', {
            headers: {
                'X-CS2Grenades-Requested-With': 'FetchRequest'
            } 
        })

        if (!response.ok) {
            throw new Error('Erro de conexão com servidor, por favor tente novamente mais tarde.');
        }

        const html = await response.text();

        profileContent.innerHTML = html;
        activeButton(changePasswordBtn);
        

    } catch (error) {
        errorAlert(error);
        changePasswordBtn.disabled = false;
    }

    passwordUpdate();
};

async function deleteAccountLoadLayout() {
    userInfoBtn.disabled = false;
    changePasswordBtn.disabled = false;
    delAccountBtn.disabled = true;


    try {
        const response = await fetch('/delete_user/', {
            headers: {
                'X-CS2Grenades-Requested-With': 'FetchRequest'
            }
        })
        
        if(!response.ok) {
            throw new Error('Erro de conexão com o servidor, por favor tente novamente mais tarde')
        }

        const html = await response.text();
        console.log(html)
        profileContent.innerHTML = html
        activeButton(delAccountBtn);

    } catch(error) {
        errorAlert(error)
        delAccountBtn.disabled = false;
    }

    const deleteBtn = document.querySelector('#delete-account-btn');
    const deleteContainer = document.querySelector('#delete-container');
    const confirmBtn = document.querySelector('#confirm-btn');
    const cancelBtn = document.querySelector('#cancel-btn');
    const deleteInput = document.querySelector('#delete');

    deleteBtn.addEventListener('click', () => {
        deleteContainer.classList.add('active')

        confirmBtn.addEventListener('click', async (event) => {
            event.preventDefault();

            if(deleteInput.value.toLowerCase() == 'deletar') {
                const response = await fetch('/delete_user/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CS2Grenades-Requested-With': 'FetchRequest',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({'confirmation': deleteInput.value.toLowerCase()})
                });

                data = await response.json();

                if(data.success) {
                    window.location.href = '/';
                }
                if(!data.success) {
                    error(data.error)
                }

            } else {
                warningAlert('Digite deletar corretamente.')
            };
        })

        cancelBtn.addEventListener('click', () => {
            deleteContainer.classList.remove('active')
        })
    })
}

delAccountBtn.addEventListener('click', deleteAccountLoadLayout);
changePasswordBtn.addEventListener('click', passwordUpdateLoadLayout);
userInfoBtn.addEventListener('click', userUpdateLoadLayout);
userInfoBtn.click();
