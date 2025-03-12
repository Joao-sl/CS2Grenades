function getCookie(name) {
    // Adiciona ";" no inicio da lista, caso o cookie desejado esteja no começo.
    const value = `; ${document.cookie}`;
    // Separa os cookies em duas partes e já remove o nome=, [antes_do_cookie, depois_do_cookie].
    const parts = value.split(`; ${name}=`);
    // "pop" pega a ultima parte do array, "split" separa o array, "shift" pega o primeiro valor do array.
    if (parts.length === 2) return parts.pop().split(';').shift();

    return null
}
