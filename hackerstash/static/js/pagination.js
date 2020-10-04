function paginate(event) {
    const page = event.target.value;

    const search = new URLSearchParams(window.location.search);
    search.set('page', page);
    window.location.search = search.toString();
}
