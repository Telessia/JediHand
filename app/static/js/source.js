
let dropdownMenu = document.getElementsByClassName('option')[0];

fetch("./static/js/config.json")
.then(response => {
   return response.json();
})
.then(jsondata => {
    possibleCommands = jsondata.possibleCommands;
    // we add the list of possible commands in the dropdown menu choice
    fill_tableau(possibleCommands);

    // we assign the commands already assigned
    for (let i = 0; i < mySlides.length; i++) {
        var str= mySlides[i].getAttribute('command')
        if (str != null) {
            if((str.includes("launch_a_link"))||(str.includes("launch_a_program"))){
                const words = str.split(" ");
                affectedCommands.push(words[0]);
                mySlides[i].setAttribute('command',words[0])
                argsArray.push(words[1]);
                IdsArray.push(mySlides[i].getAttribute('id'));
                continue
            }
            affectedCommands.push(str);
            IdsArray.push(mySlides[i].getAttribute('id'));
            argsArray.push("");
        }  
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
        }
    
        dropdownMenu.insertAdjacentElement('beforeend', newLine);
    }
}