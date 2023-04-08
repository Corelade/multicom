document.addEventListener('DOMContentLoaded', ()=>{

    let first_prompts = document.querySelector('#first_prompts')
    let btns = first_prompts.querySelectorAll('button');
    let form_cover = document.querySelector('#access_forms');
    let afi = document.querySelector('#afi');

    btns.forEach(btn => {
        btn.onclick = ()=>{
            form_cover.style.display = 'block';
            afi.style.display = 'block';
            if(btn.innerHTML == 'Sign up'){
                let individual = document.querySelector('#individual');
                individual.style.display = 'block';
                if(document.querySelector('#login_form').style.display == 'block'){
                    document.querySelector('#login_form').style.display = 'none';
                }
            }
            if(btn.innerHTML == 'Sign in'){
                if(document.querySelector('#individual').style.display == 'block'){
                    document.querySelector('#individual').style.display = 'none'
                }
                document.querySelector('#login_form').style.display = 'block';
            }
        }
    })

})