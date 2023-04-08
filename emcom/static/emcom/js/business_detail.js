document.addEventListener('DOMContentLoaded', ()=>{

    let form = document.querySelector('#add_business_item_form');
    let button = document.querySelector('#add_business_item_button');
    let clo = document.querySelector('.clo'); //close button
    let csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    button.onclick = ()=>{
        form.style.display = 'block'
    }
    clo.onclick = ()=>{
        form.style.display = 'none';
    }

    let list_items = document.querySelectorAll('.list_items');
    list_items.forEach(list_item => {
        list_item.onclick = ()=>{        
            
            let form = list_item.querySelector('.edit_form');
            let all_inputs = form.querySelectorAll('input');
            let chosen = list_item.querySelector('.listings');
            let id = list_item.getAttribute('id');
            
            chosen.classList.add('chosen');

            let del_btn = chosen.querySelector('.delete_item');
            let edit_btn = chosen.querySelector('.edit_item');

            edit_btn.onclick = ()=>{
                
                if(edit_btn.innerHTML === 'Cancel'){
                    all_inputs.forEach(input => {
                        if(input.getAttribute('name') !== 'csrfmiddlewaretoken'){
                            input.setAttribute('readonly', true);
                            input.style.border = 'none';
                            edit_btn.innerHTML = 'Edit';
                            del_btn.innerHTML = 'Delete';
                        }
                    })
                }
                else{
                    all_inputs.forEach(input => {
                        if(input.getAttribute('name') !== 'csrfmiddlewaretoken'){
                            input.removeAttribute('readonly');
                            input.style.border = '1px solid gray';
                            edit_btn.innerHTML = 'Cancel';
                            del_btn.innerHTML = 'Save';
                        }
                    })
                }
            }
            del_btn.onclick = ()=>{
                if(del_btn.innerHTML === 'Save'){
                    let newarr = [];

                    all_inputs.forEach(input => {

                        item_id = del_btn.getAttribute('id');
                        if(input.getAttribute('name')==='item_name'){
                            let item_name = input.value;
                            newarr.push(item_name);
                            //console.log(input.value);
                        }
                        if(input.getAttribute('name')==='item_description'){
                            let item_description = input.value;
                            newarr.push(item_description);
                            //console.log(input.value);
                        }
                        if(input.getAttribute('name')==='item_price'){
                            let item_price = input.value;
                            newarr.push(item_price);
                            //console.log(input.value);
                        }

                        input.setAttribute('readonly', true);
                        edit_btn.innerHTML = 'Edit';
                        del_btn.innerHTML = 'Delete';
                    })
                    
                    fetch(`/update/${id}`,{
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken,
                        },
                        body: JSON.stringify({
                            'item_id': id,
                            'item_name' : newarr[0],
                            'item_description' : newarr[1],
                            'item_price' : newarr[2],
                        })
                    })
                    .then(resp => resp.text())
                    .then(data => {
                        if(data === 'OK'){
                            console.log('done');
                        }
                    })
                }
                else{
                    del_btn.parentElement.parentElement.style.display = 'none';
                    
                    fetch(`/delete/${id}`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken,
                        },
                        body: JSON.stringify({
                            'item_id' : id
                        })
                    })
                    .then(resp => resp.text())
                    .then(data => {
                        if(data === 'OK'){
                            console.log('done');
                        }
                    })
                }
            }

        }

    })
})