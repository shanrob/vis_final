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

var img_links = [
	"static/imgs/leslie.jpg",
	"static/imgs/tom.jpg",
	"static/imgs/ron.jpg",
	"static/imgs/ben.jpg",
	"static/imgs/andy.jpg",
	"static/imgs/anne_crop.jpg",
	"static/imgs/april.jpg",
	"static/imgs/chris.jpg",
	"static/imgs/donna.jpg",
	"static/imgs/jerry.jpg"
]


var trying = d3.select(".vis-body")
		.append("svg")
		.attr("class", "blerb")
		.attr("width", 1)
		.attr("height", 1)

var defs = trying.append("defs")
var img_id = function(d) {return "img_" + d;}
var img_url = function(d) {return "url(#img_"+d+")"}

var imgPattern = defs.selectAll("pattern").data(img_links)
						.enter()
							.append("pattern")
								.attr("id", function(d, i) {
									return "img_" + i;
								})
								.attr("width", 1)
								.attr("height", 1)
								.attr("patternUnits", "objectBoundingBox")
								.append("image")
									.attr("x", 0)
									.attr("y", 0)
									.attr("width", 80)
									.attr("height", 80)
									.attr("xlink:href", function(d) {
										return d;
									})


console.log(img_id("Leslie Knope"))
var peep_label = d3.select("#faces").append("div")	
				    .attr("class", "label")				
				    .style("opacity", 0);

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
				.style("fill", function(d, i) {
					console.log('url(#'+ "img_" + i + ")");
					return 'url(#'+ "img_" + i + ")";
				})
				.style("stroke-width", "1px")
				.style("stroke", "gray")
				.on("mouseover", function(d) {
					d3.select(this).transition().duration(300)
													.attr("r", 43)

				})
				.on("mouseout", function(d) {
					d3.select(this).transition().duration(300)
													.attr("r", 40)
				})

var xs = d3.scaleBand()
				.domain(main_chars)
				.range([0, faces_width])
var xaxis = d3.axisBottom(xs);
var plotx = d3.select(".peeps").append("g");

plotx.attr("class", "axis")
	.attr("transform", "translate(0," + (faces_height-25) +")")
					.call(xaxis.tickSize(0))
						.call(plotx=>plotx.select(".domain").remove())


