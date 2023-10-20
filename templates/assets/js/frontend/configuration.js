HandleFormChange = () => {
    let btn = document.getElementById('submit-btn')

    btn.classList.remove('btn-secondary');
    btn.classList.add('btn-primary');
    btn.removeAttribute('disabled');
    btn.value = 'Save!'
}