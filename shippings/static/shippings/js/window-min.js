function abrirNovaJanela(url) {
    let novaJanela = window.open(url, "_blank", "toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, width=800, height=500");
    novaJanela.focus();
  }