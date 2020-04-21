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

var colors = {
	"Leslie Knope": "#fcc603",
	"Tom Haverford": "#0f9425",
	"Ron Swanson": "#940f0f",
	"Ben Wyatt": "#184aad",
	"Andy Dwyer": "#1ccaff",
	"Ann Perkins": "#d8b7ed",
	"April Ludgate": "#ba1472",
	"Chris Traeger": "#1b1870",
	"Donna Meagle": "#af1ac9",
	"Jerry Gergich": "#f58331"
}

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

// some dimensions
var faces_width = $("#faces").width();
var faces_height = $("#faces").height();
var circle_dims = (faces_width / (main_chars.length))
var buffer = (0.051 * faces_width);


// using svg patterns with imgs to fill the character avatars
var image_app = d3.select(".vis-right")
		.append("svg")
		.attr("class", "blerb")
		.attr("width", 1)
		.attr("height", 1)

var defs = image_app.append("defs")
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
									.attr("width", circle_dims)
									.attr("height", circle_dims)
									.attr("xlink:href", function(d) {
										return d;
									})

// svg to hold the chatacter avatars
var fsvg = d3.select("#faces")
					.append("svg")
						.attr("class", "peeps")
						.attr("width", faces_width)
						.attr("height", faces_height)


// draw the character avatars
var fcircles = d3.select(".peeps").selectAll("circle")
					.data(main_chars)

	fcircles.enter()
			.append("circle")
				.attr("class", "mug")
				.attr("id", function(d) {
					return d;
				})
				.attr("r", (circle_dims*.93)/2)
				.attr("cx", function(d, i) {
					return (circle_dims*i)+buffer;
				})
				.attr("cy", faces_height/2.4)
				.style("fill", function(d, i) {
					return 'url(#'+ "img_" + i + ")";
				})
				.style("stroke-width", "1px")
				.style("stroke", "gray")
				.on("mouseover", function(d) {
					d3.select(this).transition().duration(200)
													.attr("r", ((circle_dims*.93)/2)+3)

				})
				.on("mouseout", function(d) {
					d3.select(this).transition().duration(300)
												.attr("r", (circle_dims*.93)/2)
				})
				.on("click", function(d) {
					var currid = d;
					d3.selectAll(".underline").style("opacity", function(d) {
						if(currid == d) {
							return 1;
						}
						return 0;
					})
					d3.selectAll(".underline").style("fill", function(d) {
						if(currid == d) {
							return colors[d];
						}
						return "#ccc";
					})
				})

// create the "X" axis to display the names
var xs = d3.scaleBand()
				.domain(main_chars)
				.range([0, faces_width])
var xaxis = d3.axisBottom(xs);
var plotx = d3.select(".peeps").append("g");

plotx.attr("class", "axis")
	.attr("transform", "translate(0," + (faces_height-21) +")")
					.call(xaxis.tickSize(0))
						.call(plotx=>plotx.select(".domain").remove())


// draw the underlines to show which character is selected
var underlines = d3.select(".peeps").append("g").selectAll("rect")
									.data(main_chars)
									.enter()
									.append("rect")
									.attr("class", "underline")
									.attr("id", function(d) {
										return d;
									})
									.attr("width", circle_dims)
									.attr("height", 4)
									.attr("x", function(d, i) {
										return (circle_dims*i);
									})
									.attr("rx", 2)
									.style("fill", function(d) {
										return colors[d];
									})
									.style("opacity", 0)
									.attr("transform", "translate(0," + (faces_height - 6) +")")


