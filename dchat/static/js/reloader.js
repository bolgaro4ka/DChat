iframe = document.getElementsByTagName('iframe')[0].contentWindow
iframe_doc = document.getElementsByTagName('iframe')[0].contentDocument
normal_iframe = document.getElementsByTagName('iframe')[0]

field = document.getElementById('id_message')
field.autocomplete = 'off'

//toggle = true
//function toggleTheme() {
//    if (toggle) {
//        document.body.style.filter = 'invert(100%)'
//        toggle = false
//    } else {
//        document.body.style.filter = 'invert(0)'
//       toggle = true
//    }
//}
