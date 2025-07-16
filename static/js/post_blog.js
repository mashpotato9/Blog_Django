window.onload = function() {
    const { createEditor, createToolbar, i18nChangeLanguage } = window.wangEditor
    
    // Change language to English before creating editor
    i18nChangeLanguage('en')

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {
        const html = editor.getHtml()
        console.log('editor content', html)
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
}
