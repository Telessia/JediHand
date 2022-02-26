
let dropdownMenu = document.getElementsByClassName('option')[0];
var mySlides = document.getElementById('wrapper').children;

fetch("./static/js/config.json")
.then(response => {
   return response.json();
})
.then(jsondata => {
    possibleCommands = jsondata.possibleCommands;
    //On ajoute la liste des commandes possibles dans le choix du menu dropdown
    fill_tableau(possibleCommands);

    //On assigne les commandes déjà assignés
    for (let i = 0; i < mySlides.length; i++) {
        affectedCommands.push(mySlides[i].getAttribute('command'));
        IdsArray.push(mySlides[i].getAttribute('id'));
        console.log(mySlides[i].getAttribute('id'));
    }
});

function fill_tableau (_possible_commands){
    for(let i in _possible_commands) {

        let newLine = document.createElement('div');
        newLine.textContent = _possible_commands[i];
    
        newLine.onclick = function () {
            document.querySelector('.textBox').value = this.innerHTML;
            affectedCommands[currentIndex] = this.innerHTML;
            mySlides[currentIndex].setAttribute("command",this.innerHTML);
            console.log(mySlides[currentIndex].getAttribute("command"));
        }
    
        dropdownMenu.insertAdjacentElement('beforeend', newLine);
    }
}