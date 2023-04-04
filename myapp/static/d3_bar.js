function createChart(data, containerId, chartTitle, keyField) {
    data.sort((a, b) => b.count - a.count);
  
    const margin = {top: 40, right: 30, bottom: 100, left: 60};
    const width = 400 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;
  
    const svg = d3.select(`#${containerId}`)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

    // Add background rectangle
    svg.append("rect")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", width)
        .attr("height", height)
        .attr("fill", "#ff0000")
        .style("fill", "#EBEBEB");

  
    const x = d3.scaleBand()
        .range([0, width])
        .domain(data.map(d => d[keyField]))
        .padding(0.2);
  
    const y = d3.scaleLinear()
        .range([height, 0])
        .domain([0, d3.max(data, d => d.count)]);
  
    svg.append("g")
        .call(d3.axisLeft(y));
  
    const bars = svg.selectAll(".bar")
        .data(data)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", d => x(d[keyField]))
        .attr("width", x.bandwidth())
        .attr("y", height)
        .attr("height", 0)
        .attr("fill", "#0c6cfc")
        .attr("stroke", "red") // add a border stroke
        .attr("stroke-width", 5) // set the border stroke width
        .on("mouseover", function(event, d) {
        const xPos = x(d[keyField]) + x.bandwidth() / 2;
        const yPos = y(d.count) - 10;
        d3.select(this).attr("fill", "#0c6cfc");
        svg.append("text")
            .attr("id", "tooltip")
            .attr("x", xPos)
            .attr("y", yPos)
            .attr("text-anchor", "middle")
            .text(d.count);
        })
        .on("mouseout", function(event, d) {
        d3.select(this).attr("fill", "#0c6cfc");
        svg.select("#tooltip").remove();
        })
        .transition()
        .duration(1000)
        .delay((d, i) => i * 100)
        .attr("y", d => y(d.count))
        .attr("height", d => height - y(d.count));
        
    svg.append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("transform", "rotate(-45)")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em");
  
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", -50) // adjust this value to move the label to the left or right
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Study Count")
        .style("font-size", "17px");
  
    svg.append("text")
        .attr("x", (width + margin.left) / 2)
        .attr("y", -margin.top / 2)
        .attr("text-anchor", "middle") // center align the text horizontally
        .style("font-size", "17px")
        .text(chartTitle);

    svg.selectAll('.x-axis text')
        .style('font-size', '1em');
    }  

