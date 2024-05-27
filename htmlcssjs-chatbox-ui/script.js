const chatBoxIcon = document.getElementById('chatbox-btn-wrapper')
const chatBoxCloseBtn = document.querySelector('#chatbox .chatbox-close')
const chatBoxWrapper = document.getElementById('chatbox')
const chatBoxTextField = document.getElementById('chatbox-message-field')

chatBoxIcon.addEventListener('click', e =>{
    e.preventDefault()
    if(chatBoxWrapper.classList.contains('show')){
        chatBoxWrapper.classList.remove('show')
    }else{
        chatBoxWrapper.classList.add('show')
        chatBoxIcon.style.display = `none`
    }
})

chatBoxCloseBtn.addEventListener('click', e => {
    e.preventDefault()
    if(chatBoxWrapper.classList.contains('show')){
        if(!chatBoxWrapper.classList.contains('closing'))
            chatBoxWrapper.classList.add('closing');
            setTimeout(()=>{
            chatBoxWrapper.classList.remove('show');
            chatBoxWrapper.classList.remove('closing');
            }, 500)
    }
    chatBoxIcon.removeAttribute('style')
})

const chatBoxTextFieldHeight = chatBoxTextField.clientHeight
chatBoxTextField.addEventListener('keyup', e=>{
    var maxHeight = getComputedStyle(chatBoxTextField).getPropertyValue('--chatbox-max-height')
    chatBoxTextField.removeAttribute('style')
    setTimeout(()=>{
        if(chatBoxTextField.scrollHeight > maxHeight){
            chatBoxTextField.style.height = `${maxHeight}px`
        }else{
            chatBoxTextField.style.height = `${chatBoxTextField.scrollHeight}px`
        }
    },0)
})