const loginBtn = document.querySelector('#sign-in');
const registerBtn = document.querySelector('#sign-up');
const authPopup = document.querySelector('#auth-popup');

// Do it later
function socialLogin() { 
    const googleBtn = document.querySelector('#google-btn');
    const youtubeBtn = document.querySelector('#youtube-btn');

    googleBtn.addEventListener('click', () => {
        infoAlert('Disponível em Breve :D')
    })

    youtubeBtn.addEventListener('click', () => {
        infoAlert('Diponivel em Breve :D');
    });
}

function emailValidation(email) {
    const emailRegex = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/i;
    return emailRegex.test(email)
}

function loginAuth() {
    const loginForm = document.querySelector('#auth-form')
    const emailInput = document.querySelector('#auth-email');
    const passwordInput = document.querySelector('#auth-password');
    const displayError = document.querySelector('#error')

    loginForm.addEventListener('submit', (event) => {
        event.preventDefault();
        fetch('/login_auth/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                email: emailInput.value,
                password: passwordInput.value
            })

        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = "/"

            } else {
                displayError.textContent = data.error
            }
        });

    });
};


function addFormDataCheck() {
    const authForm = document.querySelector('#auth-form');
    const displayError = document.querySelector('#error');
    
    if (authForm) {
        // Maybe change to "blur" later
        authForm.addEventListener('submit', (event) => {
            event.preventDefault();
            let validForm = true;
            const passwordInput = document.querySelector('#auth-password');
            const confirmPasswordInput = document.querySelector('#auth-confirm-password');
            const authNameInput = document.querySelector('#auth-name');
            const emailInput = document.querySelector('#auth-email');

            let passwordError = displayError.querySelector("#password-error-msg");
            let nameError = displayError.querySelector("#name-error-msg");
            let emailError = displayError.querySelector("#email-error-msg");

            if (passwordError) {
                passwordError.remove();
            }
            
            if (nameError) {
                nameError.remove();
            }
            
            if (emailError) {
                emailError.remove();
            }

            if (passwordInput.value !== confirmPasswordInput.value) {
                passwordError = document.createElement('p');
                passwordError.innerHTML = 'As senhas não coincidem, por favor verifique'
                passwordError.id = 'password-error-msg';
                displayError.appendChild(passwordError);
                validForm = false;
            }

            if (authNameInput.value.length < 3) {
                nameError = document.createElement('p');
                nameError.innerHTML = 'O nick ou nome deve conter 3 caracteres no mínimo.';
                nameError.id = 'name-error-msg';
                displayError.appendChild(nameError);
                validForm = false;
            }

            if (!emailValidation(emailInput.value)){
                emailError = document.createElement('p');
                emailError.innerHTML = 'E-mail Inválido, por favor verifique';
                emailError.id = 'email-error-msg';
                displayError.appendChild(emailError);
                validForm = false;
            }

            if (validForm) {
                fetch('/register_data/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')  // Envia o CSRFToken
                    },
                    body: JSON.stringify({
                        username: authNameInput.value,
                        email: emailInput.value,
                        password: passwordInput.value,
                        passwordConfirm: confirmPasswordInput.value,
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        successAlert('Conta Criada com sucesso.');
                        loginBtn.click();

                    } else {
                        errorAlert(data.error)
                    }
                })
                .catch(error => {
                    console.error(error);
                })
            };
        });
    };
};

function addSwitchFormListeners() {
    const switchToRegister = document.querySelector('#sign-up-link');
    const switchToLogin = document.querySelector('#sign-in-link');
    const closePopup = document.querySelector('#close-popup');

    if (switchToRegister) {
        switchToRegister.addEventListener('click', (event) => {
            event.preventDefault();
            fetch('/register/', {
                headers: {
                    'X-CS2Grenades-Requested-With': 'FetchRequest'  
                }
            })
            .then(response => response.text())
            .then(html => {
                authPopup.innerHTML = html
                addSwitchFormListeners();
                addFormDataCheck();
                socialLogin();
            });
        });
    };

    if (switchToLogin) {
        switchToLogin.addEventListener('click', (event) => {
            event.preventDefault();
            fetch('/login/', {
                headers: {
                    'X-CS2Grenades-Requested-With': 'FetchRequest'
                }
            })
            .then(response => response.text())
            .then(html => {
                authPopup.innerHTML = html;
                addSwitchFormListeners();
                loginAuth();
                socialLogin();
            });
        });
    };

    closePopup.addEventListener('click', () => {
        authPopup.classList.remove('show');
    });
};

if (loginBtn) {
    loginBtn.addEventListener('click', (event) => {
        event.preventDefault();
        fetch('/login/', {
            headers: {
                'X-CS2Grenades-Requested-With': 'FetchRequest'  
            }
        })
        .then(response => response.text())
        .then(html => {
            authPopup.innerHTML = html;
            authPopup.classList.add('show');
            addSwitchFormListeners();
            loginAuth();
            socialLogin();
        });
    });
}

// if (registerBtn) {
//     registerBtn.addEventListener('click', (event) => {
//         event.preventDefault();
//         fetch('/register/', {
//             headers: {
//                 'X-CS2Grenades-Requested-With': 'FetchRequest'  
//             }
//         })
//         .then(response => response.text())
//         .then(html => {
//             authPopup.innerHTML = html;
//             authPopup.classList.add('show');
//             addSwitchFormListeners();
//             addFormDataCheck();
//             socialLogin();
//         });
//     });
// }

window.addEventListener('mousedown', (event) => {
    if(event.target === authPopup) {
        authPopup.classList.remove('show');
    }
});
