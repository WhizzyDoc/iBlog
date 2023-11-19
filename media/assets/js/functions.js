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
        console.log(data)
        $('.blog-table').empty()
        if(data['status'] == 'success') {
            if(data.data !== undefined) {
                cats = data.data;
                for(var i in cats) {
                    var temp = `<option value="${cats[i].slug}">${cats[i].title}</option>`;
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

function getBlogs() {
    let stat = $('.status-filter').val()
    let feat = $('.feat-filter').val()
    let cat = $('.cat-filter').val()
    let per_p = $('.per-page-filter').val()
    let search = $('#search').val()
    let page = $('#page').val()
    let url = `${base_url}blogs/get_blogs/?page=${page}&per_page=${per_p}&search=${search}&status=${stat}&featured=${feat}`;
    $('.blog-table').empty().html(`<tr>${loader}</tr>`)
    fetch(url, {
        headers: {
            'Accept': 'application/json' 
        }
    })
    .then(res => {
        return res.json()
    })
    .then(data => {
        console.log(data)
        $('.blog-table').empty()
        if(data['status'] == 'success') {
            if(data.data !== undefined) {
                blogs = data.data;
                for(var i in blogs) {
                    let status, featured;
                    let created = new Date(blogs[i].created).toLocaleString()
                    if(blogs[i].status === 'Published') {
                        status = `<a href="#" class="w-text-brown">Unpublish</a>&nbsp;|&nbsp;`
                    }
                    else {
                        status = `<a href="#" class="w-text-green">Publish</a>&nbsp;|&nbsp;`
                    }
                    if(blogs[i].featured === true) {
                        featured = `<i class="fa fa-check-circle" style="color:green;"></i>`
                    }
                    else {
                        featured = `<i class="fa fa-times" style="color:red"></i>`
                    }
                    var temp = `<tr class="w-small">
                                    <td>
                                        <div class="w-bold-x">${blogs[i].title}</div>
                                        <p class="mt-2">
                                            <a href="#" class="w-text-blue">Edit</a>&nbsp;|&nbsp;
                                            <a href="#" class="w-text-red">Delete</a>&nbsp;|&nbsp;
                                            ${status}
                                            <a href="#" class="w-text-blue">Comments</a>
                                        </p>
                                    </td>
                                    <td>${blogs[i].category.title}</td>
                                    <td style="font-size:15px;text-align:center;">
                                        ${featured}
                                    </td>
                                    <td>${created}</td>
                                </tr>`;
                    $('.blog-table').append(temp)
                }
            }
            else {
                var temp = `<tr>
                        <td colspan="4">${data['message']}</td>
                    </tr>`;
                $('.blog-table').append(temp)
            }
        }
        else if(data['status'] == 'error') {
            var temp = `<tr>
                        <td colspan="4">${data['message']}</td>
                    </tr>`;
            $('.blog-table').append(temp)
        }
    })
    .catch(err => {
        console.log(err)
    })
}