function updateSearch(searchText) {
  var search = searchText.value.toLowerCase();
  console.log(search);
  var stations = document.getElementsByClassName("station");
  for (let i = 0; i < stations.length; i++) {
    if (stations[i].id.toLowerCase().startsWith(search)) {
      stations[i].classList.remove("hidden");
    } else {
      stations[i].classList.add("hidden");
    }
  }
}
