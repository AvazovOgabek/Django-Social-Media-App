$(document).ready(function() {
    // Click event for the close button
    $('#closeChatBtn').on('click', function() {
        // Get the previous URL from the browser's history
        var previousURL = document.referrer;

        // Check if the previous URL contains '/comments/'
        if (previousURL.includes('/comments/')) {
            window.history.go(-2); // Go back two pages (skip the comments page)
        } else {
            window.history.back(); // If not a comments page, go back using history
        }
    });
});