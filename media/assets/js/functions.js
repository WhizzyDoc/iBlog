const base_url = `http://127.0.0.1:8000/api/v2/`;
const loader = `<div class="loader">
                <div class="ball"></div>
                <div class="ball"></div>
                <div class="ball"></div>
                </div>`;

function getCategories() {
    let url = `${base_url}blogs/get_blog_categories/`;
    fetch(url, {
        headers: {
            'Accept': 'application/json' 
        }
    })
    .then(res => {
        return res.json()
    })
    .then(data => {
        //console.log(data)
        $('.blog-table').empty()
        if(data['status'] == 'success') {
            if(data.data !== undefined) {
                cats = data.data;
                for(var i in cats) {
                    var temp = `<option value="${cats[i].id}">${cats[i].title}</option>`;
                    $('.cat-filter').append(temp);
                }
            }
            else {
                var temp = `<option disabled>${data['message']}</option>`;
                $('.cat-filter').append(temp);
            }
        }
        else if(data['status'] == 'error') {
            var temp = `<option disabled>${data['message']}</option>`;
            $('.cat-filter').append(temp);
        }
    })
    .catch(err => {
        console.log(err)
    })
}

