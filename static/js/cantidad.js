function cambio (id, tipo){
  // console.log(id);

  inputnum = document.getElementById(id);


  let activar = "addcarrito" + id;
  addbtn = document.getElementById(activar);

  // console.log(inputnum);

  if (tipo == 1)
  {
    inputnum.value = Number(inputnum.value) + 1;
    addbtn.disabled = false;
  }
  else {
    if (inputnum.value > 0)
    {
      inputnum.value = Number(inputnum.value) - 1;

      if (inputnum.value == 0)
      {
        addbtn.disabled = true;
      }
    }
  }
}