console.log("generating character faces...");

var main_chars = [
	"Leslie Knope",
	"Tom Haverford",
	"Ron Swanson",
	"Ben Wyatt",
	"Andy Dwyer",
	"Ann Perkins",
	"April Ludgate",
	"Chris Traeger",
	"Donna Meagle",
	"Jerry Gergich"
]

var faces_width = $("#faces").width();
var faces_height = $("#faces").height();
var circle_dims = (faces_width / (main_chars.length))

var fsvg = d3.select("#faces")
					.append("svg")
						.attr("class", "peeps")
						.attr("width", faces_width)
						.attr("height", faces_height)

var fcircles = d3.select(".peeps").selectAll("circle")
					.data(main_chars)

	fcircles.enter()
			.append("circle")
				.attr("class", "mug")
				.attr("id", function(d) {
					return d;
				})
				.attr("r", "40px")
				.attr("cx", function(d, i) {
					return (circle_dims*i) +45;
				})
				.attr("cy", faces_height/2.5)
				.style("fill", "#f0f0f0")
				.on("mouseover", function(d) {
					d3.select(this).transition().duration(300)
													.attr("r", 43)
													.style("stroke", "gray")
													.style("stroke-width", "1px")
				})
				.on("mouseout", function(d) {
					d3.select(this).transition().duration(300)
													.attr("r", 40)
													.style("stroke", "none")
				})

