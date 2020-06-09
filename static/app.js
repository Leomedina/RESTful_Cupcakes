const BASE_URL = "http://127.0.0.1:5000/api";
const UL = document.querySelector('UL');
const submit = document.querySelector('form')

class Cupcake {
    constructor(baseUrl, ul) {
        this.baseUrl = baseUrl
        this.ul = ul
    }

    cupcakeElement(cupcake) {
        const li = document.createElement('LI');
        const delBtn = this.createDelBtn();
        li.setAttribute("cupcake-id", cupcake.id);
        li.innerText = `${cupcake.flavor} / ${cupcake.size} / Rating: ${cupcake.rating}`;
        li.append(delBtn);
        return li;
    }

    createDelBtn() {
        const btn = document.createElement('button');
        btn.innerText = 'X'
        btn.classList.add('del-btn');
        return btn
    }
    async showCupcakes() {
        const response = await axios.get(`${this.baseUrl}/cupcakes`)
        for (let cupcake of response.data) {
            let newCupcake = this.cupcakeElement(cupcake);
            this.ul.append(newCupcake)
        }
    }

    async addCupcake(flavor, size, rating, image) {
        const response = await axios.post(`${this.baseUrl}/cupcakes`, {
            flavor: flavor,
            size: size,
            rating: rating,
            image: image
        })
        console.log(response)
    }

    clearCupcakes() {
        this.ul.innerHTML = '';
    }

    formHandler(e) {
        e.preventDefault();
        const flavor = document.getElementById("flavor").value;
        const size = document.getElementById("size").value;
        const rating = document.getElementById("rating").value;
        const image = document.getElementById("image_url").value;
        this.addCupcake(flavor, size, rating, image)
        submit.reset()
        this.clearCupcakes()
        this.showCupcakes()
    }
}

const cupcake = new Cupcake(BASE_URL, UL);
cupcake.showCupcakes();

submit.addEventListener('submit', function (e) { cupcake.formHandler(e); });
