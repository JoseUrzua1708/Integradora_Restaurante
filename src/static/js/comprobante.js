document.addEventListener("DOMContentLoaded", function () {
  const imprimirBtn = document.getElementById("btn-imprimir");
  if (imprimirBtn) {
    imprimirBtn.addEventListener("click", function () {
      window.print();
    });
  }
});