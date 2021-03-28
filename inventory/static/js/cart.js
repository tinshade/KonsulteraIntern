const urlget = "/cart/get_items/"
fetch(urlget, {
    method: 'GET',
    headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrftoken,
    }
})
.then((response)=>{
    return response.json();
})
.then((data)=>{
    if(String(window.location.href).includes('cart')){
        document.getElementById('cart_items').innerHTML = data.cart_items
    }else{
        document.getElementById('cart_items').innerHTML = data.cart_items
        console.log(data)
        if(data.items.length>0){
            let dataArray = data.items.split('_')
            dataArray.pop()
            dataArray.map(item =>{
                console.log(item)
                let btnId = "btn_"+item
                let currentBtn = document.getElementById(btnId);
                currentBtn.innerHTML = "ADDED"
                currentBtn.disabled = true
            })
        }
    }
    
});

let removeBtns = document.getElementsByClassName('remove-item')
    for(let i=0; i<removeBtns.length; i++){
        removeBtns[i].addEventListener('click', function(){
            let productId = this.dataset.product
            let counter = this.dataset.counter
            removeItem(productId, counter)
        })
    }


const setValue = (value, maxVal, id) =>{
    let pid = parseInt(id.split('_')[1]);
    if(value > maxVal){
        //document.getElementById(id).value = maxVal;
        updateUserOrder(pid,'custom',parseInt(maxVal))
    }else if(value < 0){
        //document.getElementById(id).value = 0;
        updateUserOrder(pid,'custom',0)
    }else{
        updateUserOrder(pid,'custom',parseInt(value))
    }
}


async function updateUserOrder(productId, action, value=0){
    const urlpost = '/cart/update_item/'
    await fetch(urlpost, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'productId':productId, 'action':action, 'value': value})
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        console.log('Data:', data)
        document.getElementById('cart_items').innerHTML = data.cart_items;
        if(String(window.location.href).includes('cart')){
            document.getElementById('availableQty_'+String(data.response.dataFor)).innerHTML = data.response.availableQty;
            document.getElementById('newTotal_'+String(data.response.dataFor)).innerHTML = data.response.newTotal;
            document.getElementById('grand_total').innerHTML = data.grand_total;
            document.getElementById('grand_items').innerHTML = data.cart_items
        }
    });
}

function removeItem(productId, counter){
    const urldelete = '/cart/remove_item/'
    fetch(urldelete, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'productId': productId})
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        console.log(data)
        document.getElementById('cart_items').innerHTML = data.cart_items;
        document.getElementById('tr_'+String(counter)).style.display= "none";
        document.getElementById('grand_total').innerHTML = data.grand_total;
        document.getElementById('grand_items').innerHTML = data.cart_items
        if(data.cart_items === 0){
            document.getElementById('checkout_div').style.display = "none"
        }else{
            document.getElementById('checkout_div').style.display = "inherit"
        }
    })
}


function deleteItemAdmin(productId, counter){
    const urladmindelete = '/inventory/delete_admin_item/'
    fetch(urladmindelete, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'productId': productId})
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        console.log(data)
        if(data.status === 200)
        document.getElementById('div_'+String(counter)).style.display = 'none';
    })
}