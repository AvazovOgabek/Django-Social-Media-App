function hideErrorMessage(closeButton) {
    const errorContainer = closeButton.closest('.error');
    if (errorContainer) {
        errorContainer.style.display = 'none';
    }
}

    const closeButtons = document.querySelectorAll('.error__close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            hideErrorMessage(this);
        });
    });