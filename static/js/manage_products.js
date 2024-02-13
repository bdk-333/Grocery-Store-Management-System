const addProductForm = document.getElementById("productForm")
const username = addProductForm.elements.name.value

if (username == "") {
  alert("Please enter product details.")
}

