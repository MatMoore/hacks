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

    var width = $(paper.canvas).width();
    var height = $(paper.canvas).height();

    var topleft = new Corner(50, 50, "#f00");
    var bottomleft = new Corner(50, height-50, "#0f0");
    var topright = new Corner(width-50, 50, "#00f");
    var bottomright = new Corner(width-50, height-50, "#ff0");

    var Grid = function (tl, tr, bl, br) {
        var grid = this;
        this.num_lines = 19;
        this.num_spaces = this.num_lines - 1;
        this.tl = tl;
        this.tr = tr;
        this.bl = bl;
        this.br = br;
        this.debug = false;
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
            var element = paper.path(path);
            element.toBack();
            this.horizontal[this.horizontal.length] = element;
        }
        for (var x = tl.x; x <= tr.x + eps; x += dx) {
            var path = 'M' + x + ',' + tl.y + 'L' + x + ',' + bl.y
            var element = paper.path(path);
            element.toBack();
            this.vertical[this.vertical.length] = element;
        }

        if(this.debug) {
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
    }

    /*
     * Find the vanishing point of vertical grid lines
     */
    Grid.prototype.findVerticalVanishing = function() {
       var vertical_vanishing;

       var leftLine = getLineParams(this.tl.x, this.tl.y, this.bl.x, this.bl.y);
       var rightLine = getLineParams(this.tr.x, this.tr.y, this.br.x, this.br.y);

       if (leftLine === null && rightLine === null) {
           // both vertical lines are actually vertical
           vertical_vanishing = null;
       } else if (leftLine === null) {
           vertical_vanishing = {
               x: this.tl.x,
               y: getVerticalConvergence(this.tl.x, rightLine.m, rightLine.c)
           };
       } else if (rightLine === null) {
           vertical_vanishing = {
               x: this.tr.x,
               y: getVerticalConvergence(this.tr.x, leftLine.m, leftLine.c)
           };
       } else {
           vertical_vanishing = getConvergence(leftLine.m, leftLine.c, rightLine.m, rightLine.c);

       }

       return vertical_vanishing;
    }

    /*
     * Find vanishing point of horizontal gridlines
     */
    Grid.prototype.findHorizontalVanishing = function() {
       var horizontal_vanishing;

       var topLine = getLineParams(this.tl.x, this.tl.y, this.tr.x, this.tr.y);
       var bottomLine = getLineParams(this.bl.x, this.bl.y, this.br.x, this.br.y);

       if (topLine === null && bottomLine === null) {
           horizontal_vanishing = null;
       } else if (topLine === null) {
           horizontal_vanishing = {
               x: this.tl.x,
               y: getVerticalConvergence(this.tl.x, bottomLine.m, bottomLine.c)
           };
       } else if (bottomLine === null) {
           horizontal_vanishing = {
               x: this.tr.x,
               y: getVerticalConvergence(this.tr.x, topLine.m, topLine.c)
           };
       } else {
           horizontal_vanishing = getConvergence(topLine.m, topLine.c, bottomLine.m, bottomLine.c);

       }

       return horizontal_vanishing;
    }

    /*
     * Update the grid lines to reflect the new corner positions
     */
    Grid.prototype.refresh = function() {
       var vertical_vanishing = this.findVerticalVanishing();
       var horizontal_vanishing = this.findHorizontalVanishing();

       if (this.debug && vertical_vanishing !== null) {
           var leftPath = "M" + this.bl.x + "," + this.bl.y + "L" + vertical_vanishing.x + "," + vertical_vanishing.y;
           var rightPath = "M" + this.br.x + "," + this.br.y + "L" + vertical_vanishing.x + "," + vertical_vanishing.y;
           this.leftVanishingPath.attr("path", leftPath);
           this.rightVanishingPath.attr("path", rightPath);
       }

       if(this.debug && horizontal_vanishing !== null) {
           var topPath = "M" + this.tl.x + "," + this.tl.y + "L" + horizontal_vanishing.x + "," + horizontal_vanishing.y;
           var bottomPath = "M" + this.br.x + "," + this.br.y + "L" + horizontal_vanishing.x + "," + horizontal_vanishing.y;
           this.topVanishingPath.attr("path", topPath);
           this.bottomVanishingPath.attr("path", bottomPath);
       }

       var horizon = this.getHorizon(vertical_vanishing, horizontal_vanishing);

       if(this.debug) {
            this.horizon.attr('path', 'M0,' + horizon.c + 'L1000,' + (horizon.m*1000+horizon.c));
       }

       var rightSide = getLineParams(this.tr.x, this.tr.y, this.br.x, this.br.y);
       var leftSide = getLineParams(this.tl.x, this.tl.y, this.bl.x, this.bl.y);
       var topSide = getLineParams(this.tl.x, this.tl.y, this.tr.x, this.tr.y);
       var bottomSide = getLineParams(this.bl.x, this.bl.y, this.br.x, this.br.y);

       if (horizon !== null) {
           horizon = new LineOrVertical(horizon, vertical_vanishing.x);
       }
       rightSide = new LineOrVertical(rightSide, this.tr.x);
       leftSide = new LineOrVertical(leftSide, this.tl.x);
       topSide = new LineOrVertical(topSide, this.tl.x);
       bottomSide = new LineOrVertical(bottomSide, this.bl.x);

       if (horizon === null) {
           // One or both sets of grid lines do not converge.
           // If both do not converge then the grid should be perfectly
           // rectangular/parallelogramish, and we can just divide evenly.
           //
           // In the case where the horizontal lines don't converge, but the
           // vertical ones do, (i.e. a trapezium) then this will be wrong.
           var horizontal = this.divideEqually(this.tl, this.bl, this.tr, this.br);
       } else {
           var horizontal = this.getGridLines(topSide, bottomSide, horizon, horizontal_vanishing);
       }
       this.drawGridLines(leftSide, rightSide, horizontal, this.horizontal);

       if (horizon === null) {
           var vertical = this.divideEqually(this.tl, this.tr, this.bl, this.br);
       } else {
           var vertical = this.getGridLines(leftSide, rightSide, horizon, vertical_vanishing);
       }
       this.drawGridLines(topSide, bottomSide, vertical, this.vertical);
    };

    /*
     * Redraw the horizontal lines based on new line equations
     */
    Grid.prototype.drawGridLines = function(side, matchingSide, lineEqs, paths) {
        for (var i = 0; i < lineEqs.length; i++) {
            var line = lineEqs[i];
            var path = paths[i];
            var start = side.intersect(line);
            var end = matchingSide.intersect(line);

            if (start === null || end === null) {
                console.log('Too squashed');
                continue;
            }

            var newPath = "M" + start.x + "," + start.y + "L" + end.x + "," + end.y;
            path.attr("path", newPath);
        }
    }

    /*
     * Get a list of lines that equally divide two sides
     */
    Grid.prototype.divideEqually = function(sideStart, sideEnd, matchingStart, matchingEnd) {
        var delta = {
            x: (sideEnd.x - sideStart.x) / this.num_spaces,
            y: (sideEnd.y - sideStart.y) / this.num_spaces
        }

        var delta2 = {
            x: (matchingEnd.x - matchingStart.x) / this.num_spaces,
            y: (matchingEnd.y - matchingStart.y) / this.num_spaces
        }

        var results = [];
        for (var i = 0; i < this.num_lines; i++) {
            var startPoint = {x: sideStart.x + i * delta.x, y: sideStart.y + i * delta.y};
            var endPoint = {x: matchingStart.x + i * delta2.x, y: matchingStart.y + i * delta2.y};
            var line = getLineParams(startPoint.x, startPoint.y, endPoint.x, endPoint.y);
            line = new LineOrVertical(line, startPoint.x);
            results.push(line);
        }
        return results;
    }

    /*
     * Get the line equations for the horizontal or vertical grid lines.
     * Where these lines cross the horizon, the spacing is regular, so trace
     * the lines from the horizon back to the vanishing point.
     */
    Grid.prototype.getGridLines = function(side, matchingSide, horizon, vanishingPoint) {
       // Project both sides onto the horizon
       var projectedSide = side.intersect(horizon);
       var projectedMatchingSide = matchingSide.intersect(horizon);
       if (projectedSide === null || projectedMatchingSide === null) {
           // Not sure what's going on here
           console.log('Side is parallel to the horizon');
           console.log(side, matchingSide, horizon, this.tl, this.tr, this.bl, this.br);
           return;
       }
       var topToBottom = {
           x: projectedMatchingSide.x - projectedSide.x,
           y: projectedMatchingSide.y - projectedSide.y
       }
       var dx = topToBottom.x / this.num_spaces;
       var dy = topToBottom.y / this.num_spaces;
       var results = [];
       for (var i = 0; i < this.num_lines; i++) {
           var startPoint = {x: projectedSide.x + i * dx, y: projectedSide.y + i * dy};
           var line = getLineParams(startPoint.x, startPoint.y, vanishingPoint.x, vanishingPoint.y);
           line = new LineOrVertical(line, startPoint.x);
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
        if(vertical_vanishing === null || horizontal_vanishing === null) {
            // No horizon. Either lines converge to a point or they do not
            // converge at all.
            return null;
        }
        var horizon = getLineParams(vertical_vanishing.x, vertical_vanishing.y, horizontal_vanishing.x, horizontal_vanishing.y);

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
        return parallel;
    }

    grid = new Grid(topleft, topright, bottomleft, bottomright);
    grid.refresh();
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

/*
 * Type to represent a line, vertical or otherwise
 */
function LineOrVertical(line, x) {
    this.vertical = (line === null);
    if (this.vertical) {
        this.x = x;
    } else {
        this.m = line.m;
        this.c = line.c;
    }
}

/*
 * Intersection point with another LineOrVertical object
 */
LineOrVertical.prototype.intersect = function(other) {
    if (this.vertical && other.vertical) {
        return null;
    }

    if (this.vertical) {
        return {
            x: this.x,
            y: getVerticalConvergence(this.x, other.m, other.c)
        }
    }

    if (other.vertical) {
        return {
            x: other.x,
            y: getVerticalConvergence(other.x, this.m, this.c),
        }
    }

    return getConvergence(this.m, this.c, other.m, other.c);
}
