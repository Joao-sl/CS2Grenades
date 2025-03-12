const customAlert = document.querySelector('#alert');
const closeAlert = document.querySelector('#close-alert');
const alertContent = document.querySelector('#alert-content');
const alertIcon = document.querySelector('#alert-icon');
const alertTitle = document.querySelector('#alert-title');
const alertMsg = document.querySelector('#show-msg');

function infoAlert(msg) {
    if (alertContent.classList.contains('s-border')) {
        alertContent.classList.remove('s-border')
    }
    if (alertContent.classList.contains('w-border')) {
        alertContent.classList.remove('w-border')
    }
    if (alertContent.classList.contains('e-border')) {
        alertContent.classList.remove('e-border')
    }

    alertContent.classList.add('i-border')
    alertIcon.innerHTML = '<i class="fa-solid fa-info i-check"></i>'
    alertTitle.innerHTML = 'Info'
    alertMsg.innerHTML = msg

    customAlert.classList.add('show-alert');

    if (closeAlert) {
        closeAlert.addEventListener('click', function (event) {
            event.preventDefault();
            customAlert.classList.remove('show-alert');
        });
    }
}

function successAlert(msg) {
    if (alertContent.classList.contains('i-border')) {
        alertContent.classList.remove('i-border')
    }
    if (alertContent.classList.contains('w-border')) {
        alertContent.classList.remove('w-border')
    }
    if (alertContent.classList.contains('e-border')) {
        alertContent.classList.remove('e-border')
    }

    alertContent.classList.add('s-border')
    alertIcon.innerHTML = '<i class="fas fa-solid fa-check s-check"></i>'
    alertTitle.innerHTML = 'Sucesso'
    alertMsg.innerHTML = msg

    customAlert.classList.add('show-alert');

    if (closeAlert) {
        closeAlert.addEventListener('click', function (event) {
            event.preventDefault();
            customAlert.classList.remove('show-alert');
        });
    }
}

function warningAlert(msg) {
    if (alertContent.classList.contains('i-border')) {
        alertContent.classList.remove('i-border')
    }
    if (alertContent.classList.contains('s-border')) {
        alertContent.classList.remove('s-border')
    }
    if (alertContent.classList.contains('e-border')) {
        alertContent.classList.remove('e-border')
    }

    alertContent.classList.add('w-border')
    alertIcon.innerHTML = '<i class="fa-solid fa-exclamation w-check"></i>'
    alertTitle.innerHTML = 'Atenção'
    alertMsg.innerHTML = msg

    customAlert.classList.add('show-alert');

    if (closeAlert) {
        closeAlert.addEventListener('click', function (event) {
            event.preventDefault();
            customAlert.classList.remove('show-alert');
        });
    }
}

function errorAlert(msg) {
    if (alertContent.classList.contains('i-border')) {
        alertContent.classList.remove('i-border')
    }
    if (alertContent.classList.contains('s-border')) {
        alertContent.classList.remove('s-border')
    }
    if (alertContent.classList.contains('w-border')) {
        alertContent.classList.remove('w-border')
    }

    alertContent.classList.add('e-border')
    alertIcon.innerHTML = '<i class="fa-solid fa-xmark e-check"></i>'
    alertTitle.innerHTML = 'Erro'
    alertMsg.innerHTML = msg

    customAlert.classList.add('show-alert');

    if (closeAlert) {
        closeAlert.addEventListener('click', function (event) {
            event.preventDefault();
            customAlert.classList.remove('show-alert');
        });
    }
}

window.addEventListener('mousedown', (event) => {
    if (event.target === customAlert) {
        customAlert.classList.remove('show-alert');
    }
});
