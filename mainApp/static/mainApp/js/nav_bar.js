function loadDoc(id) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("DishChangesJS").innerHTML =
                this.responseText;
        }
    };
    let getUrl = window.location;
    let baseUrl = getUrl.protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[0];
    xhttp.open("GET", baseUrl + id);
    xhttp.send();
}


function showcart() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("DishChangesJS").innerHTML =
                this.responseText;
        }
    };
    let getUrl = window.location;
    let baseUrl = getUrl.protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[0];
    console.log(baseUrl)
    xhttp.open("GET", baseUrl + "cart/");
    xhttp.send();
}

function updateCART() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("cart_len").innerHTML =
                this.responseText;
        }
    };
    let getUrl = window.location;
    let baseUrl = getUrl.protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[0];
    xhttp.open("GET", baseUrl + "cart/update/");
    xhttp.send();
}

function PostForm(id) {
    const xhttp = new XMLHttpRequest();
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let all_ingredients = document.getElementsByName('remove_ingredient');
    let remove_ingredients = Array()
    all_ingredients.forEach((ingredient) => {
        if (ingredient.style.textDecoration === 'line-through') {
            remove_ingredients.push(ingredient.innerText)
        }
    })
    remove_ingredients = remove_ingredients.toString()
    let form_data = new FormData()
    form_data.append("removeingredients", remove_ingredients)
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("DishChangesJS").innerHTML =
                this.responseText;
            updateCART()
        }
    };
    let getUrl = window.location;
    let baseUrl = getUrl.protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[0];
    xhttp.open("POST", baseUrl + "cart/add/" + id + '/');
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send(form_data);
}


function remove_ing(el) {
    if (el.style.textDecoration === 'line-through') {
        el.style.textDecoration = 'none';
    } else {
        el.style.textDecoration = 'line-through';
    }
}


function RemoveDish(id) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("DishChangesJS").innerHTML =
                this.responseText;
            updateCART()
        }
    };
    let getUrl = window.location;
    let baseUrl = getUrl.protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[0];
    xhttp.open("GET", baseUrl + "cart/remove/" + id + '/');
    xhttp.send();
}
