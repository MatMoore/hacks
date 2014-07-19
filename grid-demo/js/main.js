eps = 0.0001;

function setupGrid(paper) {

    var Corner = function(x, y, fill) {
        this.circle = paper.circle(x, y, 10);
        this.circle.attr("fill", fill);
        this.circle.attr("stroke", "#fff");

        // This is kept in sync with the centre when the point is not being
        // dragged.
        this.x = x;
        this.y = y;
        var corner = this;

        // Keep track of the distance moved since the start of the drag.
        // dx, dy are always relative to the start point, not the last move
        // event.
        var moved_x = 0;
        var moved_y = 0;
        var handleMove = function(dx, dy) {
            newdx = dx - moved_x;
            newdy = dy - moved_y;
            this.attr('cx', this.attr('cx') + newdx);
            this.attr('cy', this.attr('cy') + newdy);
            moved_x = dx;
            moved_y = dy;
        };
        var handleStart = function () {};
        var handleEnd = function() {
            moved_x = 0;
            moved_y = 0;
            corner.x = this.attr('cx');
            corner.y = this.attr('cy');
        };
        this.circle.drag(handleMove, handleStart, handleEnd);
    };

    var topleft = new Corner(50, 50, "#f00");
    var bottomleft = new Corner(50, 200, "#0f0");
    var topright = new Corner(200, 50, "#00f");
    var bottomright = new Corner(200, 200, "#ff0");

    var Grid = function (tl, tr, bl, br) {
        var grid = this;
        this.proj_br = paper.circle(300, 300, 5);
        this.num_lines = 19;
        this.num_spaces = this.num_lines - 1;
        this.tl = tl;
        this.tr = tr;
        this.bl = bl;
        this.br = br;
        var refresh = function() {
            grid.refresh();
        };
        this.tl.circle.drag(function() {}, function() {}, refresh);
        this.tr.circle.drag(function() {}, function() {}, refresh);
        this.br.circle.drag(function() {}, function() {}, refresh);
        this.bl.circle.drag(function() {}, function() {}, refresh);

        // Create horizontal and vertical gridlines
        this.horizontal = [];
        this.vertical = [];
        var dy = ((bl.y - tl.y) / this.num_spaces);
        var dx = ((tr.x - tl.x) / this.num_spaces);
        for (var y = tl.y; y <= bl.y + eps; y += dy) {
            var path = 'M' + tl.x + ',' + y + 'L' + tr.x + ',' + y
            this.horizontal[this.horizontal.length] = paper.path(path);
        }
        for (var x = tl.x; x <= tr.x + eps; x += dx) {
            var path = 'M' + x + ',' + tl.y + 'L' + x + ',' + bl.y
            this.vertical[this.vertical.length] = paper.path(path);
        }

        var path = "M" + bl.x + "," + bl.y + "V0";
        this.leftVanishingPath = paper.path(path);
        this.leftVanishingPath.attr("stroke", "#999");

        var path = "M" + br.x + "," + br.y + "V0";
        this.rightVanishingPath = paper.path(path);
        this.rightVanishingPath.attr("stroke", "#999");

        var path = "M" + tl.x + "," + tl.y + "H0";
        this.topVanishingPath = paper.path(path);
        this.topVanishingPath.attr("stroke", "#999");

        var path = "M" + bl.x + "," + bl.y + "H0";
        this.bottomVanishingPath = paper.path(path);
        this.bottomVanishingPath.attr("stroke", "#999");

        var path = "M0,100H1000"
        this.horizon = paper.path(path);
        this.horizon.attr("stroke", "#fff");
    }

    Grid.prototype.findVerticalVanishing = function() {
       var vertical_vanishing;

       var leftLine = getLineParams(this.tl.x, this.tl.y, this.bl.x, this.bl.y);
       var rightLine = getLineParams(this.tr.x, this.tr.y, this.br.x, this.br.y);

       if (leftLine === null && rightLine === null) {
           console.log('both vertical lines are actually vertical');
           vertical_vanishing = null;
       } else if (leftLine === null) {
           console.log('left is vertical');
           vertical_vanishing = {
               x: this.tl.x,
               y: getVerticalConvergence(this.tl.x, rightLine.m, rightLine.c)
           };
       } else if (rightLine === null) {
           console.log('right is vertical');
           vertical_vanishing = {
               x: this.tr.x,
               y: getVerticalConvergence(this.tr.x, leftLine.m, leftLine.c)
           };
       } else {
           vertical_vanishing = getConvergence(leftLine.m, leftLine.c, rightLine.m, rightLine.c);

       }

       if (vertical_vanishing === null) {
           console.log('both lines parallel');
       } else {
           console.log(vertical_vanishing);
       }

       return vertical_vanishing;
    }

    Grid.prototype.findHorizontalVanishing = function() {
       var horizontal_vanishing;

       var topLine = getLineParams(this.tl.x, this.tl.y, this.tr.x, this.tr.y);
       var bottomLine = getLineParams(this.bl.x, this.bl.y, this.br.x, this.br.y);

       if (topLine === null && bottomLine === null) {
           console.log('both vertical lines are actually vertical');
           horizontal_vanishing = null;
       } else if (topLine === null) {
           console.log('left is vertical');
           horizontal_vanishing = {
               x: this.tl.x,
               y: getVerticalConvergence(this.tl.x, bottomLine.m, bottomLine.c)
           };
       } else if (bottomLine === null) {
           console.log('right is vertical');
           horizontal_vanishing = {
               x: this.tr.x,
               y: getVerticalConvergence(this.tr.x, topLine.m, topLine.c)
           };
       } else {
           horizontal_vanishing = getConvergence(topLine.m, topLine.c, bottomLine.m, bottomLine.c);

       }

       if (horizontal_vanishing === null) {
           console.log('both lines parallel');
       } else {
           console.log(horizontal_vanishing);
       }

       return horizontal_vanishing;
    }

    Grid.prototype.refresh = function() {
       var vertical_vanishing = this.findVerticalVanishing();
       var horizontal_vanishing = this.findHorizontalVanishing();
       if (vertical_vanishing === null) {
       } else {
           console.log(vertical_vanishing);
           var leftPath = "M" + this.bl.x + "," + this.bl.y + "L" + vertical_vanishing.x + "," + vertical_vanishing.y;
           var rightPath = "M" + this.br.x + "," + this.br.y + "L" + vertical_vanishing.x + "," + vertical_vanishing.y;
           this.leftVanishingPath.attr("path", leftPath);
           this.rightVanishingPath.attr("path", rightPath);
       }
       if (horizontal_vanishing === null) {
       } else {
           console.log(horizontal_vanishing);
           var topPath = "M" + this.tl.x + "," + this.tl.y + "L" + horizontal_vanishing.x + "," + horizontal_vanishing.y;
           var bottomPath = "M" + this.br.x + "," + this.br.y + "L" + horizontal_vanishing.x + "," + horizontal_vanishing.y;
           this.topVanishingPath.attr("path", topPath);
           this.bottomVanishingPath.attr("path", bottomPath);
       }


       var horizon = this.getHorizon(vertical_vanishing, horizontal_vanishing);
       var rightSide = getLineParams(this.tr.x, this.tr.y, this.br.x, this.br.y);
       var leftSide = getLineParams(this.tl.x, this.tl.y, this.bl.x, this.bl.y);
       var topSide = getLineParams(this.tl.x, this.tl.y, this.tr.x, this.tr.y);
       var bottomSide = getLineParams(this.bl.x, this.bl.y, this.br.x, this.br.y);

       var projected = getConvergence(rightSide.m, rightSide.c, horizon.m, horizon.c)
       this.proj_br.attr('cx', projected.x);
       this.proj_br.attr('cy', projected.y);

       horizontal = this.getHorizontalLines(topSide, bottomSide, horizon, horizontal_vanishing);
       this.drawHorizontalLines(leftSide, rightSide, horizontal);
    };

    /*
     * Redraw the horizontal lines based on new line equations
     */
    Grid.prototype.drawHorizontalLines = function(leftSide, rightSide, lineEqs) {
        for (var i = 0; i < lineEqs.length; i++) {
            var line = lineEqs[i];
            var path = this.horizontal[i];
            if(leftSide === null) {
                var start = getVerticalConvergence(this.tl.x, line.m, line.c);
                start = {x: this.tl.x, y: start};
            } else {
                var start = getConvergence(leftSide.m, leftSide.c, line.m, line.c);
            }

            if(rightSide === null) {
                var end = getVerticalConvergence(this.tr.x, line.m, line.y);
            } else {
                var end = getConvergence(rightSide.m, rightSide.c, line.m, line.c);
            }

            if (start === null || end === null) {
                console.log('Your so called horizontal line is parallel to the left or right side. ABORT');
                continue;
            }

            var newPath = "M" + start.x + "," + start.y + "L" + end.x + "," + end.y;
            path.attr("path", newPath);
        }
    }

    /*
     * Get the line equations for the "horizontal" grid lines.
     * Where these lines cross the horizon, the spacing is regular, so trace
     * the lines from the horizon back to the vanishing point.
     */
    Grid.prototype.getHorizontalLines = function(topSide, bottomSide, horizon, horizontalVanishing) {
       // Project top and bottom sides onto the horizon
       var projectedTop = getConvergence(topSide.m, topSide.c, horizon.m, horizon.c)
       var projectedBottom = getConvergence(bottomSide.m, bottomSide.c, horizon.m, horizon.c)
       var distance = getDistance(projectedTop, projectedBottom);
       if (distance === 0) {
           console.log("Top and bottom overlap, no horizontal lines for you");
           return [];
       }

       var topToBottom = {
           x: projectedBottom.x - projectedTop.x,
           y: projectedBottom.y - projectedTop.y
       }
       var dx = topToBottom.x / this.num_spaces;
       var dy = topToBottom.y / this.num_spaces;
       var results = [];
       for (var i = 0; i < this.num_lines; i++) {
           var startPoint = {x: projectedTop.x + i * dx, y: projectedTop.y + i * dy};
           var line = getLineParams(startPoint.x, startPoint.y, horizontalVanishing.x, horizontalVanishing.y);
           results.push(line);
       }
       return results;
    }

    /*
     * Find a line parallel to the horizon.
     * Make it go through the furthest point from the horizon, so that lines
     * traced from this line to a vanishing point go through the whole grid.
     */
    Grid.prototype.getHorizon = function(vertical_vanishing, horizontal_vanishing) {
        horizon = getLineParams(vertical_vanishing.x, vertical_vanishing.y, horizontal_vanishing.x, horizontal_vanishing.y);

        var furthestFromHorizon = this.tl;
        var distanceToHorizon = getDistanceToLine(horizon, this.tl);
        var toTest = [this.tr, this.bl, this.br];
        $(toTest).each(function () {
            var thisDistance = getDistanceToLine(horizon, this);
            if (thisDistance > distanceToHorizon) {
                distanceToHorizon = thisDistance;
                furthestFromHorizon = this;
            }
        });

        parallel = getParallelLine(horizon, furthestFromHorizon);
        this.horizon.attr('path', 'M0,' + parallel.c + 'L1000,' + (parallel.m*1000+parallel.c));
        return parallel;
    }

    grid = new Grid(topleft, topright, bottomleft, bottomright);
};

/*
 * Get the convergence point of two lines, or null if they are parallel.
 */
function getConvergence(m1, c1, m2, c2) {
    if(Math.abs(m1 - m2) < eps) {
        return null;
    }

    result = {x: (c2 - c1) / (m1 - m2)};
    result.y = result.x * m1 + c1;
    return result;
}


/*
 * Get the convergence point of a vertical line with another line
 */
function getVerticalConvergence(x, m1, c1) {
    return m1 * x + c1;
}

/*
 * Draw a line between two points and return the equation
 * of the line.
 * Vertical lines return null.
 */
function getLineParams(x1, y1, x2, y2) {
    var dx = x1 - x2;
    if (Math.abs(dx) < eps) {
        return null;
    }
    m = (y1 - y2) / dx;
    c = y1 - m * x1;
    return {m: m, c: c};
}

/*
 * Get a line parallel to another line that intersects a point
 */
function getParallelLine(line, point) {
    var new_c = point.y - line.m * point.x;
    return {m: line.m, c: new_c};
}

/*
 * Distance from a point to a line
 */
function getDistanceToLine(line, point) {
    var projected = getProjectedPoint(line, point);
    return getDistance(point, projected);
}

/*
 * Project a point onto a line by drawing a perpindicular line from the point
 * to that line.
 */
function getProjectedPoint(line, point) {
    var perpindicular_m = -1 / line.m;
    var perpindicular_c = point.y - perpindicular_m * point.x;
    var x = (line.c - perpindicular_c) / (perpindicular_m - line.m);
    var y = line.m * x + line.c;
    return {x: x, y:y};
}

/*
 * Distance between two points
 */
function getDistance(point1, point2) {
    return Math.sqrt(Math.pow((point1.x - point2.x), 2) + Math.pow((point1.y - point2.y), 2));
}
