window.onload = function() {
    document.getElementById('send-code').onclick = function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Get the email input value
        var email = document.getElementById('email').value;

        // Get CSRF token
        var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        // Send an AJAX request to the server
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/auth/send_captcha', true);
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
        
        xhr.onload = function() {
            if (xhr.status === 200) {
                showPopup('Code sent successfully!', 'success');
            } else {
                showPopup('Error sending code: ' + xhr.responseText, 'error');
            }
        };

        xhr.send(JSON.stringify({ email: email }));
    };
}

function showPopup(message, type) {
    // Create popup element
    var popup = document.createElement('div');
    popup.className = 'popup ' + type;
    popup.style.cssText = 'position: fixed; top: 20px; right: 20px; padding: 15px 20px; border-radius: 5px; color: white; z-index: 9999; box-shadow: 0 4px 6px rgba(0,0,0,0.1); background-color: ' + (type === 'success' ? '#4CAF50' : '#f44336');
    popup.innerHTML = '<span>' + message + '</span><button onclick="this.parentElement.remove()" style="background: none; border: none; color: white; font-size: 18px; margin-left: 10px; cursor: pointer;">×</button>';
    
    // Add to page
    document.body.appendChild(popup);
    
    // Auto-remove after 5 seconds
    setTimeout(function() {
        if (popup.parentElement) {
            popup.remove();
        }
    }, 2000);
}