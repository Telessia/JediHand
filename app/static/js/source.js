
let dropdownMenu = document.getElementsByClassName('option')[0];

console.log(mySlides);

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
       var str= mySlides[i].getAttribute('command') 
        if((str.includes("launch_a_link"))||(str.includes("launch_a_program"))){
            console.log("LAUNCH COMMAND ", str)
            const words = str.split(" ");
            affectedCommands.push(words[0]);
            mySlides[i].setAttribute('command',words[0])
            argsArray.push(words[1]);
            IdsArray.push(mySlides[i].getAttribute('id'));
            continue
        }
        console.log(mySlides[i].getAttribute('command'))
        console.log(typeof(mySlides[i].getAttribute('command')))
        affectedCommands.push(str);
        IdsArray.push(mySlides[i].getAttribute('id'));
        argsArray.push("");
    }
});

function fill_tableau (_possible_commands){
    for(let i in _possible_commands) {

        let newLine = document.createElement('div');
        newLine.textContent = _possible_commands[i];
    
        newLine.onclick = function () {
            document.querySelector('.textBox').value = this.innerHTML;
            affectedCommands[currentIndex] = this.innerHTML;
            if (this.innerHTML == "launch_a_link" || this.innerHTML == "launch_a_program"){
                textArg.style.display = "block"
            }
            else{
                textArg.style.display = "none"
            }
            mySlides[currentIndex].setAttribute("command",this.innerHTML);
            console.log(mySlides[currentIndex].getAttribute("command"));
        }
    
        dropdownMenu.insertAdjacentElement('beforeend', newLine);
    }
}