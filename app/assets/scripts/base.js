window.addEventListener('pywebviewready', function() {
    displaySecrets();
});


const displaySecrets = () => {
    pywebview.api.get_secrets().then(
        (secrets) => {
            const block = document.getElementById('secret-block');
            const template = document.getElementById('secret-template');

            block.innerHTML = '';

            for (const ind in secrets) {
                let new_node = template.cloneNode(true);
                new_node.classList.remove('d-none');
                let account = new_node.getElementsByClassName('card-title')[0];
                let order = new_node.getElementsByClassName('card-subtitle')[0];
                let extra = new_node.getElementsByClassName('card-text')[0];
                let clipboardButton = new_node.getElementsByClassName('card-clipboard')[0];
                let removeSecretButton = new_node.getElementsByClassName('card-remove')[0];

                const secret = secrets[ind];
                account.textContent = secret.name
                order.textContent = `ID: ${secret.id}`;
                extra.textContent = secret.extra
                clipboardButton.setAttribute('secret-id', secret.id)
                removeSecretButton.setAttribute('secret-id', secret.id)
                block.appendChild(new_node);
            }
        }
    );
}


const closeBlock = (blockId) => {
    const block = document.getElementById(blockId)
    block.classList.add('d-none');
}

const clearInputs = () => {
    const nameField = document.getElementById('secret-name-field');
    const extraField = document.getElementById('secret-extra-field');

    nameField.value = '';
    extraField.value = '';
}

const displayInfo = (message) => {
    const infoBlock = document.getElementById('info-block');
    const infoText = document.getElementById('info-text');
    infoText.textContent = message;
    infoBlock.classList.remove('d-none');
}

const displayError = (message) => {
    const errorBlock = document.getElementById('error-block');
    const errorText = document.getElementById('error-text');
    errorText.textContent = message;
    errorBlock.classList.remove('d-none');
}


const createSecret = () => {
    const secretName = document.getElementById('secret-name-field').value;
    const extra = document.getElementById('secret-extra-field').value;
    pywebview.api.create_secret(secretName, extra).then(
        (status) => {
            if (status.ok) {
                displayInfo(status.message);
                displaySecrets();
                clearInputs();
            } 
            else displayError(status.message);
        }
    );
}
