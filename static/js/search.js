function go_search(){
            var search_title = document.getElementById('search').value;
            window.location.href="/shop/search_result?search_title="+search_title;
        }