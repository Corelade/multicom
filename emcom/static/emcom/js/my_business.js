document.addEventListener('DOMContentLoaded', ()=>{
    
    let add_business = document.querySelector('#add_business');
    let add_business_div = document.querySelector('#add_business_div');
    let clo = document.querySelector('.clo'); //close button

    add_business.onclick = ()=>{
        add_business_div.style.display = 'block';
    }
    clo.onclick = ()=>{
        add_business_div.style.display = 'none';
    }

})