

$(window).on("load", function(){
	console.log("are we getting this?")
	d3.select(".underline").style("opacity", 1);
	drawIntro("Leslie Knope");

});

$(".mug").on("click", function() {
	var name = this.id
	drawIntro(name);

})

var quotes = {
	"Leslie Knope": "I care. I care a lot. It's kinda my thing.",
	"Tom Haverford": "I have never taken the high road. But I tell other people to 'cause then there's more room for me on the low road.",
	"Ron Swanson": "There’s only one thing I hate more than lying: skim milk. Which is water that’s lying about being milk.",
	"Ben Wyatt": "I have been tense lately. Just thinking about the new Star Wars sequel. I’m worried they’ll rely too heavily on CGI and I’m carrying it all in my shoulders.",
	"Andy Dwyer": "I’m allergic to sushi. Every time I eat more than 80 pieces, I throw up.",
	"Ann Perkins": "Jogging is the worst. I mean, I know it keeps you healthy. But God, at what cost?",
	"April Ludgate": "Time is money, money is power, power is pizza, and pizza is knowledge.",
	"Chris Traeger": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAnn Perkins!",
	"Donna Meagle": "Look I love you like a brother. But right now I hate you. Like my actual brother, Levandrious, who I hate.",
	"Jerry Gergich": "So I go by Terry now. They already had a Larry in the Parks department, and they suggested that they change my name to Terry. I told them my real name was Garry, and they said 'who cares?' What a fun bunch of guys."
}


function drawIntro(char) {
	d3.select("#char-name").html(char)
	d3.select("#char-quote").html('"' + quotes[char] + '"')
}

function drawCharacterVis(data) {

}