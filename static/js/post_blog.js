// Show popup message function
function showPopup(message, type) {
    const popup = document.createElement('div');
    popup.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        color: white;
        font-weight: bold;
        z-index: 1000;
        ${type === 'success' ? 'background-color: #28a745;' : 'background-color: #dc3545;'}
    `;
    popup.textContent = message;
    document.body.appendChild(popup);
    
    setTimeout(() => {
        popup.remove();
    }, 3000);
}

window.onload = function() {
    const { createEditor, createToolbar, i18nChangeLanguage } = window.wangEditor
    
    // Change language to English before creating editor
    i18nChangeLanguage('en')

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {
        const html = editor.getHtml()
        // console.log('editor content', html)
        // You can sync HTML to <textarea>
        }
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })

    // Handle form submission
    document.getElementById('post-button').onclick = function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Get form data
        const title = document.getElementById('title').value;
        const content = editor.getHtml();
        const category_id = document.getElementById('category-selected').value;

        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Send an AJAX request to the server
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/post', true);
        xhr.setRequestHeader('X-CSRFToken', csrfToken);

        xhr.onload = function() {
            if (xhr.status === 201) {
                const response = JSON.parse(xhr.responseText);
                showPopup('Blog posted successfully!', 'success');
                setTimeout(() => {
                    window.location.href = `/detail/${response.blog_id}`;
                }, 1500);
            } else {
                showPopup('Error posting blog: ' + xhr.responseText, 'error');
            }
        };

        // Send form data instead of JSON
        const formData = new FormData();
        formData.append('title', title);
        formData.append('content', content);
        formData.append('category_id', category_id);
        formData.append('csrfmiddlewaretoken', csrfToken);

        xhr.send(formData);
    }

}
