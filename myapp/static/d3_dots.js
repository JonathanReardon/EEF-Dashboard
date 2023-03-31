function drawDotChart(data) {

    // set the dimensions and margins of the graph
    const margin = {top: 40, right: 30, bottom: 100, left: 60};
        width = 400 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // Get the minimum and maximum values for your smd and sesmd data
    const smdValues = data.map(d => +d.smd_value);
    const sesmdValues = data.map(d => +d.sesmd_value);
    const smdMin = d3.min(smdValues);
    const smdMax = d3.max(smdValues);
    const sesmdMin = d3.min(sesmdValues);
    const sesmdMax = d3.max(sesmdValues);

    // append the svg object to the body of the page
    const svg = d3.select("#chart-smd-scatter")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", `translate(${margin.left}, ${margin.top})`)

    // add the styles for the grid lines and labels
    svg.append('style')
    .text(`
        .grid line {
          stroke: lightgrey;
          stroke-opacity: 0.7;
          shape-rendering: crispEdges;
        }
        
        .grid path {
          stroke-width: 0;
        }
        
        .grid text {
          font-size: 10px;
        }
    `);


    const xPadding = Math.abs(smdMax - smdMin) * 0.05;
    const yPadding = Math.abs(sesmdMax - sesmdMin) * 0.05;
    
    const x = d3.scaleLinear()
        .domain([smdMin - xPadding, smdMax + xPadding])
        .range([0, width]);
    
    const y = d3.scaleLinear()
        .domain([sesmdMin - yPadding, sesmdMax + yPadding])
        .range([height, 0]);

    // Update your x and y scales to use the minimum and maximum values
    svg.append("g")
        .attr("class", "myXaxis")   // Note that here we give a class to the X axis, to be able to call it later and modify it
        .attr("transform", `translate(0, ${height})`)
        .call(d3.axisBottom(x))
        .attr("opacity", "0")

    svg.append("g")
        .attr("class", "myYaxis")
        .call(d3.axisLeft(y));

    // add the Y axis label
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("SE (Primary Outcome)");

    // Calculate midpoint of x axis
    const xMidpoint = (x(smdMin) + x(smdMax)) / 2;

    // Add the X axis label
    svg.append("text")
        .attr("transform", `translate(${xMidpoint}, ${height + margin.bottom / 2.4})`)
        .style("text-anchor", "middle")
        .text("SMD (Primary Outcome)");
    svg.append('style')
    .text(`
        .myXaxis text {
        font-size: 12px;
        }
    `);

    const minRadius = .1;
    const maxRadius = 2;
    
    const dataCount = data.length;
    const radiusScale = d3.scaleLinear()
      .domain([1, dataCount])
      .range([minRadius, maxRadius]);
    
    const radius = radiusScale(dataCount);
    
    svg.append('g')
    .selectAll("dot")
    .data(data)
    .enter()
    .append("circle")
    .attr("cx", function (d) { return x(0); } ) // set initial position to 0 on x-axis
    .attr("cy", function (d) { return y(0); } ) // set initial position to 0 on y-axis
    .attr("r", function(d) { 
        // adjust the radius based on number of data points
        return (data.length > 1000) ? 3 : 3;
    })
    .style("fill", "#0c6cfc")
    .style("stroke", "#000") // add a black stroke
    .style("stroke-width", "1px") // set the stroke width
    .transition() // add transition to animate to final positions
    .delay(function(d,i){return(i*3)})
    .duration(100)
    .attr("cx", function (d) { return x(d.smd_value); } )
    .attr("cy", function (d) { return y(d.sesmd_value); } );

        // new X axis
        x.domain([-1, 2])
        svg.select(".myXaxis")
            .transition()
            .duration(100)
            .attr("opacity", "1")
            .call(d3.axisBottom(x));

        // new Y axis
        y.domain([0, .5])
        svg.select(".myYaxis")
            .transition()
            .duration(100)
            .attr("opacity", "1")
            .call(d3.axisLeft(y));

        // Add grey dashed lines at point 0 on the x and y axes
        svg.append("line")
            .attr("x1", x(0))
            .attr("y1", y(0))
            .attr("x2", x(0))
            .attr("y2", 0)
            .attr("stroke", "red")
            .attr("stroke-dasharray", "4");

}
