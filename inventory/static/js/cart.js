let updateBtns = document.getElementsByClassName('update-cart')


for(let i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        let productId = this.dataset.product
        let action = this.dataset.action
        if(action === "cart_add"){
            let btnId = "btn_"+productId.toString()
            let currentBtn = document.getElementById(btnId);
            currentBtn.innerHTML = "ADDED"
            currentBtn.disabled = true
        }
        updateUserOrder(productId, action)
    })
}


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
        //console.log(data)
        try {
            document.getElementById('cart_items').innerHTML = data.cart_items
            if(data.items.length>0){
                let dataArray = data.items.split('')
                dataArray.map(item =>{
                    console.log(item)
                    let btnId = "btn_"+item
                    let currentBtn = document.getElementById(btnId);
                    //TODO: Change into CSS class
                    currentBtn.innerHTML = "ADDED"
                    currentBtn.disabled = true
                })
            }
        } catch (error) {
           console.log("In cart") 
        }
        
    });

    
const setValue = (value, maxVal, id) =>{
        if(value > maxVal){
            document.getElementById(id).value = maxVal;
        }else if(value < 0){
            document.getElementById(id).value = 0;
        }
    }
function updateUserOrder(productId, action){
    const urlpost = '/cart/update_item/'
    
    fetch(urlpost, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        console.log('Data:', data)
        document.getElementById('cart_items').innerHTML = data.cart_items
    });
}

