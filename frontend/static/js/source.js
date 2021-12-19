
let dropdownMenu = document.getElementsByClassName('option')[0];

fetch("./static/js/simple.json")
.then(response => {
   return response.json();
})
.then(jsondata => {
    possibleCommands = jsondata.possibleCommands;
    possibleFigures = jsondata.possibleFigure;
    //On ajoute la liste des commandes possibles dans le choix du menu dropdown
    fill_tableau(possibleCommands);

    //On assigne les commandes déjà assignés
    let affectedCommandsFigure = jsondata.affectedCommandsFigure;
    for(var item in affectedCommandsFigure) {
        affectedCommands.push(affectedCommandsFigure[item]);
    }
});

console.log(affectedCommands);


function fill_tableau (_possible_commands){
    for(let i in _possible_commands) {

        let newLine = document.createElement('div');
        newLine.textContent = _possible_commands[i];
    
        newLine.onclick = function () {
            document.querySelector('.textBox').value = this.innerHTML;
            affectedCommands[currentIndex].command = this.innerHTML;
            console.log(affectedCommands[currentIndex]);
        }
    
        dropdownMenu.insertAdjacentElement('beforeend', newLine);
    }
}