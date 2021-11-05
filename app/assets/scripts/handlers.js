const saveToClipboardOnClickHandler = (btn) => {
    const secretId = btn.getAttribute('secret-id');
    pywebview.api.save_to_clipboard(secretId).then(
        (status) => {
            if (status.ok) {
                displayInfo(status.message);
            } 
            else displayError(status.message);
        }
    );
}

const removeSecretOnClickHandler = (btn) => {
    const secretId = btn.getAttribute('secret-id');
    pywebview.api.remove_secret(secretId).then(
        (status) => {
            if (status.ok) {
                displaySecrets();
                displayInfo(status.message);
            } 
            else displayError(status.message);
        }
    );
}

const makeBackUpOnClickHandler = () => {
    pywebview.api.make_backup().then(
        () => {
            displayInfo("New backup was saved");
        }
    );
}
