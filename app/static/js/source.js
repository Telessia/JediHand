
let dropdownMenu = document.getElementsByClassName('option')[0];

fetch("./static/js/config.json")
.then(response => {
   return response.json();
})
.then(jsondata => {
    possibleCommands = jsondata.possibleCommands;
    //On ajoute la liste des commandes possibles dans le choix du menu dropdown
    fill_tableau(possibleCommands);

    //On assigne les commandes déjà assignés
    const myElement = document.getElementById('wrapper');
    for (let i = 0; i < myElement.children.length; i++) {
        affectedCommands.push(myElement.children[i].getAttribute('data'));
        IdsArray.push(myElement.children[i].getAttribute('id'));
        console.log(myElement.children[i].getAttribute('data'));
    }
});

function fill_tableau (_possible_commands){
    for(let i in _possible_commands) {

        let newLine = document.createElement('div');
        newLine.textContent = _possible_commands[i];
    
        newLine.onclick = function () {
            document.querySelector('.textBox').value = this.innerHTML;
            affectedCommands[currentIndex] = this.innerHTML;
            console.log(affectedCommands[currentIndex]);
        }
    
        dropdownMenu.insertAdjacentElement('beforeend', newLine);
    }
}